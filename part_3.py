'''
Created on Jun 12, 2013

@author: Administrator
'''
import json,os
from part_1 import inverse_index

TWEET_PATH = 'C:/Users/Administrator/workspace/670_hw_1/mars_tweets_medium.json'
TWEET_TEXT_PATH = 'C:/Users/Administrator/workspace/670_hw_1/tweet/'

  
def get_tweet_text():
    if not os.path.exists(TWEET_TEXT_PATH):
        os.mkdir(TWEET_TEXT_PATH)
    wf = open(TWEET_PATH,'r')
    i = 0
    for line in wf:
        encoded_string = line.strip().decode('utf-8')
        tweet = json.loads(encoded_string)
        tweet_text = tweet['text'].encode('utf-8').lower()
        # print tweet_text
        f = open(TWEET_TEXT_PATH + '/' + str(i),'w')
        f.write(tweet_text)
        f.close()
        i += 1

if __name__ == '__main__':
    #get_tweet_text()
    inverse_index('tweet','tweet_index.json')