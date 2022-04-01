from xml.etree.ElementTree import TreeBuilder
import gspread
import tweepy
import random
import time, schedule

def twitterquotes():
    #Goolge Spreadsheet API credentials
    gc = gspread.service_account('credentials.json')

    #Twitter API credentials 
    access_token = 'xxxxxxxxxxxxxxxx'
    access_token_secret = 'xxxxxxxxxxxxxxxx'
    consumer_key = 'xxxxxxxxxxxxxxxx'     #API Key
    consumer_secret = 'xxxxxxxxxxxxxxxx'  #API Key Secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    public_tweets = api.home_timeline()

    #Open google sheet
    wks = gc.open("Twitter-Quotes").sheet1

    #Get all values from the first column
    list_of_quotes = wks.col_values(1)

    #Shuffle values
    random.shuffle(list_of_quotes)

    #Get the first value in list
    get_one_quote = list_of_quotes[1]


    #Post to twitter. If duplicate status error -> shuffle quotes again and post. Otherwise, post tweet
    try:
        api.update_status(get_one_quote)
    except tweepy.TweepError as error:
        if error.api_code == 187:
            random.shuffle(list_of_quotes)
            api.update_status(get_one_quote)
        else:
            api.update_status(get_one_quote)

#Set time for function to run
schedule.every(.25).minutes.do(twitterquotes)

#Check whether the scheduler has a pending function to run or not
while True:
    schedule.run_pending()
    time.sleep(1)

