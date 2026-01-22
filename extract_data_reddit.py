import praw
from praw.models import MoreComments
import json
from kafka import KafkaProducer
import os
from dotenv import load_dotenv
from typing import Dict, Any

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
try:
    subreddit = reddit.subreddit(os.getenv('SUBREDDIT_NAME'))
    for submission in subreddit.stream.submissions():

        submission.comments.replace_more(limit=0) # loading all the comments

        data: Dict[str,Any] = {
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
        print(data)
        
        try:
        #===========================================================================
        # Send to Kafka immediately using producer
        #===========================================================================
            producer.send('redditTopic', key=key, value=value)
            print(f"Sent post: {data['postId']}")
                    
        except Exception as e:
            print(f"Error processing post {getattr(submission, 'id', 'unknown')}: {e}")
            continue
            
except KeyboardInterrupt:
    print("Stream interrupted")
finally:
    producer.flush()
    producer.close()
    print("Producer closed")
