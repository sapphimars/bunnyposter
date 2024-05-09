from instagrapi import Client
import tweepy
import tweepy.client
import pinterest
import requests

from dotenv import load_dotenv
import os
import asyncio
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs



load_dotenv()

'''
class uploadMedia:
    def __init__(self, path, caption, location = None, tags = None, altText = None):
        self.path = path
        self.caption = caption

        self.location = location
        self.tags = tags
        self.altText = altText
'''
#----------DEFINE VARS-----------------------------
myPath = r"./mykotest.jpeg"
myCaption = "cat :3 (api test)"

IG_CREDS = {"username" : os.getenv("IG_USERNAME"), 
            "password" : os.getenv("IG_PASSWORD")}

X_CREDS = {"X_APIKEY" : os.getenv("X_APIKEY"),
           "X_APIKEYSECRET" : os.getenv("X_APIKEYSECRET"),
           "X_ACCESSTOKEN" : os.getenv("X_ACCESSTOKEN"),
           "X_ACCESSTOKENSECRET" : os.getenv("X_ACCESSTOKENSECRET")}

DRIBBBLE_CREDS = {"DRIBBBLE_CLIENTID" : os.getenv("DRIBBBLE_CLIENTID"),
                  "DRIBBBLE_CLIENTSECRET" : os.getenv("DRIBBBLE_CLIENTSECRET"),
                  "DRIBBBLE_AUTHCODE" : os.getenv("DRIBBBLE_AUTHCODE"),
                  "DRIBBLE_ACCESSTOKEN" : os.getenv("DRIBBBLE_ACCESSTOKEN")
}


#----------INSTAGRAM-----------------------------
async def postToInstagram(IG_CREDS, myPath, myCaption):
    ig_cl = Client()
    ig_cl.login(IG_CREDS["username"], IG_CREDS["password"])
    ig_user_id = ig_cl.user_id_from_username(IG_CREDS["username"])


    media = ig_cl.photo_upload(myPath, myCaption)




#----------TWITTER-----------------------------
async def postToX(X_CREDS, myPath, myCaption):
    x_cl = tweepy.Client(consumer_key=X_CREDS["X_APIKEY"], consumer_secret=X_CREDS["X_APIKEYSECRET"], 
                        access_token=X_CREDS["X_ACCESSTOKEN"], access_token_secret=X_CREDS["X_ACCESSTOKENSECRET"])


    x_auth = tweepy.OAuth1UserHandler(X_CREDS["X_APIKEY"], X_CREDS["X_APIKEYSECRET"])
    x_auth.set_access_token(X_CREDS["X_ACCESSTOKEN"], X_CREDS["X_ACCESSTOKENSECRET"])
    x_API = tweepy.API(x_auth)

    x_media = x_API.media_upload(filename=myPath)
    x_mediaID = x_media.media_id


    x_cl.create_tweet(text = myCaption, media_ids=[x_mediaID])



async def postToDribbble(DRIBBBLE_CREDS, myPath, myCaption):
    DRIBBBLE_CLIENTID = DRIBBBLE_CREDS["DRIBBBLE_CLIENTID"]
    DRIBBBLE_CLIENTSECRET = DRIBBBLE_CREDS["DRIBBBLE_CLIENTSECRET"]
    DRIBBBLE_CODE = DRIBBBLE_CREDS["DRIBBBLE_AUTHCODE"]
    DRIBBBLE_ACCESSTOKEN = DRIBBBLE_CREDS["DRIBBLE_ACCESSTOKEN"]

    params = {
        "client_id" : DRIBBBLE_CLIENTID,
        "scope" : "upload public"
    }

    if DRIBBBLE_ACCESSTOKEN == None:
        r = requests.get("https://dribbble.com/oauth/authorize", params=params, allow_redirects=True)
        
        driver = webdriver.Chrome()
        driver.get(r.url)
        try:
            elem = WebDriverWait(driver, 360).until(EC.url_contains("google")) 
        finally:
            url = driver.current_url
            driver.quit()
        print(url)
        parsed_url = urlparse(url)
        DRIBBBLE_CODE = parse_qs(parsed_url.query)['code'][0]
        #print(DRIBBBLE_CODE)

        params = {
            "client_id" : DRIBBBLE_CLIENTID,
            "client_secret" : DRIBBBLE_CLIENTSECRET,
            "code" : DRIBBBLE_CODE
        }
        r = requests.post("https://dribbble.com/oauth/token", params = params)
        data = r.json()
        DRIBBBLE_ACCESSTOKEN = data["access_token"]
        print(DRIBBBLE_ACCESSTOKEN)
        #print(json.dumps(data))

    #img = open(myPath, "rb")
    headers = { "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                 "Referer" : "https://api.dribbble.com/",
                 "content-type" : "image/jpeg"}
    params = {"title" : myCaption}
              #"image" : Image.open(myPath)}
    
    files = {"image" : open(myPath, "rb")}

    r = requests.post("https://api.dribbble.com/v2/shots?access_token="+DRIBBBLE_ACCESSTOKEN,
                      files=files, 
                      headers=headers,
                      params=params)
    print(r.json())
    print(r)
    #print(myPath)
    
    #print(r.text)




#asyncio.run(postToX(X_CREDS, myPath, myCaption))
#asyncio.run(postToInstagram(IG_CREDS, myPath, myCaption))
asyncio.run(postToDribbble(DRIBBBLE_CREDS, myPath, myCaption))
