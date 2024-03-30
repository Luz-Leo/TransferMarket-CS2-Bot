from selenium import webdriver 
from bs4 import BeautifulSoup
import pandas as pd
import json
import tweepy
import time
import csv
import config

client = tweepy.Client(
    consumer_key=config.key['consumer_key'], 
    consumer_secret=config.key['consumer_secret'],
    access_token=config.key['access_token'], 
    access_token_secret=config.key['access_token_secret']
)

driver = webdriver.Chrome() 

old_index = 0
transfers = []
driver.get('https://www.hltv.org/transfers')

content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")

#Get the new list of transfers
for element in soup.findAll('div', class_='transfer-text'):
    transfer = element.find('div', class_='transfer-movement')
    transfers.append(transfer.text)


with open('transfers.csv', 'r') as f:
    reader = csv.reader(f)
    transfers_csv = list(reader)
    old_transfer = transfers_csv[0]
    print(old_transfer[0])

#Find the index of last posted transfer in the new list
for idx, x in enumerate(transfers):
    if old_transfer[0] == x:
        old_index = idx
        print(old_index)
        break

#Posting all new transfers (Oldest to newest)
while old_index != 0:
    old_index = old_index -1

    response = client.create_tweet(
    text=transfers[old_index]
    )
    print(f"https://twitter.com/user/status/{response.data['id']}")
    time.sleep(20)


df = pd.DataFrame(transfers)
df.to_csv('transfers.csv', header=False, index=False, encoding='utf-8')


