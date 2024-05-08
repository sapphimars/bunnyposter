from instagrapi import Client
import tweepy
import tweepy.client
from dotenv import load_dotenv
import os
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

IG_USERNAME=os.getenv("IG_USERNAME")
IG_PASSWORD=os.getenv("IG_PASSWORD")

X_APIKEY = os.getenv("X_APIKEY")
X_APIKEYSECRET = os.getenv("X_APIKEYSECRET")
X_ACCESSTOKEN = os.getenv("X_ACCESSTOKEN")
X_ACCESSTOKENSECRET = os.getenv("X_ACCESSTOKENSECRET")


#----------INSTAGRAM-----------------------------
'''
ig_cl = Client()
ig_cl.login(IG_USERNAME, IG_PASSWORD)
ig_user_id = cl.user_id_from_username(IG_USERNAME)


media = ig_cl.photo_upload(myPath, myCaption)
'''



#----------TWITTER-----------------------------

x_cl = tweepy.Client(consumer_key=X_APIKEY, consumer_secret=X_APIKEYSECRET, 
                     access_token=X_ACCESSTOKEN, access_token_secret=X_ACCESSTOKENSECRET)


x_auth = tweepy.OAuth1UserHandler(X_APIKEY, X_APIKEYSECRET)
x_auth.set_access_token(X_ACCESSTOKEN, X_ACCESSTOKENSECRET)
x_API = tweepy.API(x_auth)

x_media = x_API.media_upload(filename=myPath)
x_mediaID = x_media.media_id


x_cl.create_tweet(text = myCaption, media_ids=[x_mediaID])