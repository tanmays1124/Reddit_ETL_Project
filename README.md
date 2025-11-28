# Reddit_ETL_Project

This project will extract the data from Reddit and send to Kafka.

## How to run

**Step 1**. install all the packages using requirements.txt

`pip install -r requirements.txt`

**Step 2**. Create a kafka topic on Confluent Cloud.  
**Step 3**. Create your reddit client id and and client secret from reddit website.  
**Step 4**. Create a text file (tracker file) that will keep track of post ids from reddit so that there is no duplication.  
**Step 5**. Generate encryption key using **Fernet** library of python which will be used to encrypt and decrypt the tracker file
**Step 6**. Create a .env where you will add the environment variables for this project  

```FERNET_ENCRYPTION_KEY=<your FERNET KEY>
REDDIT_CLIENT_ID=<YOUR_REDDIT_CLIENT_KEY>
REDDIT_CLIENT_SECRET=<YOUR_REDDIT_CLIENT_SECRET>
REDDIT_USER_AGENT=<YOUR_REDDIT_USER_AGENT>
SUBREDDIT_NAME=<YOUR_SUBREDDIT_NAME>
KAFKA_BOOTSTRAP_SERVER=<YOUR_KAFKA_BOOTSTRAP_SERVER>
KAFKA_SASL_USERNAME=<YOUR_KAFKA_SASL_USERNAME>
KAFKA_SASL_PASSWORD=<YOUR_KAFKA_SASL_PASSWORD>
LAST_SEEN_ID_FILE=<TRACKER_FILE_NAME>
FILE_TO_ENCRYPT_DECRYPT=<YOUR_FILE_TO_ENCRYPT_DECRYPT>
```

**Step 4**. Make sure the tracker file should have 1 random id (like 'id54367') present before running, else the code might not work properly.  
**Step 5**. Once the random id is added encrypt the file using `python encryption.py <file_name>` in terminal.  
**Step 6**. Run the extract_data_reddit.py file.  

## Few changes you can do

In extract_data_reddit.py at line number 45 you can chnage the limit to any number, 1 means it will only take first post i.e, latest post from 'new' category, 2 means it will tale first two posts.  
You can also replace the new() with hot(), best(), top(), rising() to get the post from respective category.
