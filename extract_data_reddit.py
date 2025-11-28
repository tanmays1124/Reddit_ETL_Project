import praw
from praw.models import MoreComments
import json
from kafka import KafkaProducer
import os
from dotenv import load_dotenv
import Reddit_ETL_Project.encryption as encryption
import Reddit_ETL_Project.decryption as decryption


# loading the environment to the code
load_dotenv()

#===========================================================================
# setting up connection with reddit
#===========================================================================
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
    )

#===========================================================================
# Setting up connection with kafka to produce the messages
#===========================================================================
producer = KafkaProducer(
    bootstrap_servers=[os.getenv('KAFKA_BOOTSTRAP_SERVER')],
    security_protocol="SASL_SSL",
    sasl_mechanism="PLAIN",
    sasl_plain_username=os.getenv('KAFKA_SASL_USERNAME'), 
    sasl_plain_password=os.getenv('KAFKA_SASL_PASSWORD'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8'), # Serializing the dictionary to json received from reddit
    key_serializer=lambda v: v.encode('utf-8'), 
    enable_idempotence= True,
    retries=3, # retries 
    acks='all'
)



data ={}
#===========================================================================
# Retreiving all the required data from subreddit using PRAW
#===========================================================================
for submission in reddit.subreddit(os.getenv('SUBREDDIT_NAME')).new(limit=1):

    submission.comments.replace_more(limit=0) # loading all teh comments

    data = {
    'postAuthor' : submission.author.name,
    'postComments' : [comment.body for comment in list(submission.comments)], # listing all the comments in list
    'isEdited' : submission.edited,
    'postId' : submission.id,
    'numberOfComments' : submission.num_comments,
    'isNSFW' : submission.over_18,
    'postScore' : submission.score,
    'isSpoiler' : submission.spoiler,
    'postTitle' : submission.title,
    'postUpvoteRatio' : submission.upvote_ratio,
    'postContent' : submission.selftext
    }

#===========================================================================
# defining key for partitioning in kafka topic and value for kafka messages
#===========================================================================
key = data['postId']
value = data

#===========================================================================
# Decrypting the last seen id file
#===========================================================================
decryption.decryptFile(os.getenv('LAST_SEEN_ID_FILE')) # Decrypting the last seen id file


#================================================================================
# Read the data from decrypted file and forma a list of all the ids already seen
#================================================================================
with open(os.getenv('LAST_SEEN_ID_FILE'),'r') as id_file:
    
    post_ids = id_file.read()
    print(post_ids)
    post_ids_list = list(post_ids.split('\n'))
    print(post_ids_list)


#================================================================================
# Compare the ids from list and if not present in the list the produce the 
# respective values to kafka
#================================================================================
if key not in post_ids_list:
    with open(os.getenv('LAST_SEEN_ID_FILE'),'a') as id_file:
        try:
            producer.send('redditTopic',key=key,value=value)
            id_file.write(f"\n{key}")
            print("new messqage added",key)
        except Exception as e:                                # Raise Exceptions if any
            raise Exception(e,'Error occured')
        
#===========================================================================
# Encrypting the last seen id file
#===========================================================================
    encryption.encryptFile(os.getenv('LAST_SEEN_ID_FILE'))
else:
    print('no new post')
    encryption.encryptFile(os.getenv('LAST_SEEN_ID_FILE'))


producer.flush()
producer.close()