# Reddit_ETL_Project

This project will extract the data from Reddit and send to Kafka.

## How to run

**Step 1**. install all the packages using requirements.txt

`pip install -r requirements.txt`

Step 2. Create a kafka topic on Confluent Cloud.  
Step 3. Create your reddit client id and and client secret from reddit website.  
Step 4. Create a .env where you will add the environment variables for this project  

```FERNET_ENCRYPTION_KEY=<your FERNET KEY>
REDDIT_CLIENT_ID=<YOUR_REDDIT_CLIENT_KEY>
REDDIT_CLIENT_SECRET=<YOUR_REDDIT_CLIENT_SECRET>
REDDIT_USER_AGENT=<YOUR_REDDIT_USER_AGENT>
SUBREDDIT_NAME=<YOUR_SUBREDDIT_NAME>
KAFKA_BOOTSTRAP_SERVER=<YOUR_KAFKA_BOOTSTRAP_SERVER>
KAFKA_SASL_USERNAME=<YOUR_KAFKA_SASL_USERNAME>
KAFKA_SASL_PASSWORD=<YOUR_KAFKA_SASL_PASSWORD>
```
 
 
Step 5. Run the extract_data_reddit.py file.  
