from bs4 import BeautifulSoup
from datetime import datetime
import feedparser
import requests
import json
import logging
import boto3
import os 

# Adapted from: https://timothybramlett.com/recieving_notifications_of_rss_feeds_matching_keywords_with_Python.html

# Just some sample keywords to search for in the title
key_words = ['cost','price','optimize','optimization','costs','prices','pricing','advisor', 'graviton','CFM','financial','finops','finance']

# Slack Webhook for Publishing Target
webhook = os.environ['WEBHOOK']

bucket_name = os.environ['BUCKET_NAME']

# RSS Feed
rss = 'https://aws.amazon.com/about-aws/whats-new/recent/feed/'

def lambda_handler(event, context):

    try:
        # View list of previously shared URLs
        s = s3_download()
        f = open('/tmp/viewed_urls.txt', 'r')
        urls = f.readlines()
        urls = [url.rstrip() for url in urls] # remove the '\n' char
        f.close()

        date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
        logging.info(date + " Logging script execution")

        feed = feedparser.parse(rss)
        for key in feed["entries"]:
            url = key['links'][0]['href']
            title = key['title']
            rawDescription = key['description']
            description = BeautifulSoup(rawDescription, 'html.parser')

            if contains_wanted(title.lower()) and url_is_new(url,urls):
                print('{} - {} - {}'.format(title, url, description.get_text()))

                #msgtitle = title
                #msg = '{}\n{}'.format(title, url, description)

                body = {
                    "title": title,
                    "description": description.get_text(),
                    "url": url,
                }
                logging.info(title)
                jsonData = json.dumps(body)
                response = requests.post(webhook, jsonData)

                        # recording URLs to file
                with open('/tmp/viewed_urls.txt', 'a') as f:
                    f.write('{}\n'.format(url))
                    f.close()
        s3_upload()
                
    except Exception as e:
        # Send some context about this error to Lambda Logs
        logging.warning("%s" % e)

def contains_wanted(in_str):
    # returns true if the in_str contains a keyword
    # we are interested in. Case-insensitive
    for wrd in key_words:
        if wrd.lower() in in_str:
            return True
    return False

def url_is_new(urlstr, urls):
    # returns true if the url string does not exist
    # in the list of strings extracted from the text file
    if urlstr in urls:
        return False
    else:
        return True

def s3_download():
    try:
        s3_client = boto3.client('s3')
        s3_client.download_file(
            Bucket=bucket_name,
            Key='cfm_rss_webhook/viewed_urls.txt',
            Filename='/tmp/viewed_urls.txt')
        
    except Exception as e:
        logging.warning("Welcome! you have no viwed file so we will make one for you")
        with open('/tmp/viewed_urls.txt', 'w') as f:
            f.write('\n')

def s3_upload():
    try:
        s3_client = boto3.client('s3')
        s3_client.upload_file(
        Bucket=bucket_name,
        Key='cfm_rss_webhook/viewed_urls.txt',
        Filename='/tmp/viewed_urls.txt')
        s3_client.upload_file(f'/tmp/viewed_urls.txt', bucket_name, f"cfm_rss_webhook/viewed_urls.txt")
        print(f"Data in {bucket_name}")
    except Exception as e:
        logging.warning("%s" % e)