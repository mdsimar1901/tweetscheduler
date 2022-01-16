import gspread
import tweepy
from dotenv import load_dotenv
from datetime import datetime,timedelta
from os import environ
import time
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN_KEY = environ['ACCESS_TOKEN_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_SECRET)

api = tweepy.API(auth)
gc = gspread.service_account(filename='credentials.json')

sh = gc.open_by_key('1UvVOPBLJjK4k-bXfIhDjwwMUns6vcdLVkklsDom4g_0')
worksheet = sh.sheet1

INTERVAL = int(environ['INTERVAL'])
DEBUG = environ['DEBUG'] =='1'

def main():
    while True:
        tweet_records = worksheet.get_all_records()
        current_time = datetime.utcnow() +timedelta(hours=5,minutes=30)
        logger.info(f'{len(tweet_records)} tweets found at {current_time.time()}')
        for idx,tweet in enumerate(tweet_records,start =2):
            msg = tweet['message']
            time_str = tweet['time']
            done = tweet['done']
            date_time_obj = datetime.strptime(time_str,'%Y-%m-%d %H:%M:%S')
            if not done:
                now_time_inr = datetime.utcnow() +timedelta(hours=5,minutes=30)
                if date_time_obj < now_time_inr:
                    logger.info('this should be tweeted')
                    try:
                        api.update_status(msg)
                        worksheet.update_cell(idx,3,1)   
                    except Exception as e:
                        logger.warning(f'exception during tweet!{e}')
                
        time.sleep(INTERVAL)
         


if __name__ == '__main__':
    main()