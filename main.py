from instagrapi import Client
import tweepy
import tweepy.client
from dotenv import load_dotenv
import os
import asyncio

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
myPath = "./mykotest.jpg"
myCaption = "cat :3 (api test)"

IG_CREDS = {"username" : os.getenv("IG_USERNAME"), 
            "password" : os.getenv("IG_PASSWORD")}

X_CREDS = {"X_APIKEY" : os.getenv("X_APIKEY"),
           "X_APIKEYSECRET" : os.getenv("X_APIKEYSECRET"),
           "X_ACCESSTOKEN" : os.getenv("X_ACCESSTOKEN"),
           "X_ACCESSTOKENSECRET" : os.getenv("X_ACCESSTOKENSECRET")}


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

#asyncio.run(postToX(X_CREDS, myPath, myCaption))
#asyncio.run(postToInstagram(IG_CREDS, myPath, myCaption))