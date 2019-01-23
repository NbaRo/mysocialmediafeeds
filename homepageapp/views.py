from django.shortcuts import render

from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler

# for insta scrap
import requests
from bs4 import BeautifulSoup
import re

from random import shuffle

# Create your views here.

def home(request):
    access_token = '1086516275273175040-eemeflmfD2L3udS8dMLKEL65hZQl5z'
    access_token_secret = 'XrzkJtMHAQ3OaukAbZA5gZHCrS4YQ6wmcvqLEh4UETT91'
    consumer_key = 'oO2Uk782AkKsFgkUCsjWYPnlW'
    consumer_secret = 'ETvrZYxbZXbjwMj2W9ab6ydO5fwqfG1nF62BlGGuf87FyGZTne'

    #### TWITTER CLIENT ####
    class TwitterClient():
        def __init__(self, twitter_user=None):
            self.auth = TwitterAuthenticator().authenticate_twitter_app()
            self.twitter_client = API(self.auth)

            self.twitter_user = twitter_user

        def get_twtitter_client_api(self):
            return self.twitter_client

        def get_user_timeline_tweets(self, num_tweets):
            tweets = []
            for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
                tweets.append(tweet)
            return tweets

        def get_friend_list(self, num_friends):
            friend_list = []
            for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
                friend_list.append(friend)
            return friend_list

        def get_home_timeline_tweets(self, num_tweets):
            home_timeline_tweets = []
            for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
                home_timeline_tweets.append(tweet)
            return home_timeline_tweets

    #### TWITTER AUTHENTICATER ####
    class TwitterAuthenticator():

        def authenticate_twitter_app(self):
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            return auth

    twitteracclist = ['realDonaldTrump', 'ArianaGrande', 'katyperry', 'justinbieber', 'BarackObama', 'rihanna', 'taylorswift13', 'ladygaga', 'TheEllenShow', 'Cristiano', 'jtimberlake', 'KimKardashian', 'ddlovato', 'selenagomez']

    twitter_client = TwitterClient()

    api = twitter_client.get_twtitter_client_api()

    twittdict = {}


    for tw in twitteracclist:
        tweets = api.user_timeline(screen_name=tw, count=5)
        profileinfo = api.get_user(screen_name=tw)
        twitlist = []
        num = 0
        num1 = 0
        for t in tweets:
            if t.favorite_count:
                if t.favorite_count < num:
                    pass
                elif t.favorite_count > num:
                    num = t.favorite_count
                    num1 = t

        twitlist.append(num1.user.name)
        twitlist.append(num1.user.screen_name)
        num1.created_at = num1.created_at.strftime("%H:%M")
        twitlist.append(num1.created_at)
        twitlist.append(num1.id)
        twitlist.append(num1.text)
        if num1.favorite_count == 0:
            twitlist.append(num1.retweeted_status.favorite_count)
        else:
            twitlist.append(num1.favorite_count)
        twitlist.append(num1.retweet_count)
        twitlist.append(profileinfo.profile_image_url)
        if 'media' in num1.entities:
            for image in num1.entities['media']:
                twitlist.append(image['media_url'])

        twittdict[tw] = twitlist

    valueslist = list(twittdict.values())
    shuffle(valueslist)


    #insta scrap :

    instaacctlistg = ['kyliejenner', 'beyonce', 'taylorswift', 'neymarjr', 'leomessi', 'kendalljenner', 'nickiminaj', 'natgeo', 'khloekardashian', 'jlo', 'nike', 'mileycyrus', 'katyperry', 'kourtneykardash', 'fcbarcelona']

    instaacctslistdict = {}
    for iw in instaacctlistg:
        ilink = "https://www.instagram.com/" + iw
        page = requests.get(ilink)
        bsoup = BeautifulSoup(page.content, 'html.parser')

        instinf = bsoup.find_all('script')
        atst = str(instinf)
        xxx = re.search('shortcode', atst)
        insta_link = str(instinf)[xxx.span()[0] + 12:xxx.span()[1] + 14]

        instapagelink = 'https://www.instagram.com/p/' + insta_link
        pagesecond = requests.get(instapagelink)
        bsoupsecond = BeautifulSoup(pagesecond.content, 'html.parser')

        contenttext = ''
        instaimage = ''
        likesinsta = ''
        for tag in bsoupsecond.find_all("meta"):
            if tag.get("property", None) == "og:title":
                contenttext = tag.get("content", None)
            elif tag.get("property", None) == "og:image":
                instaimage = tag.get("content", None)
            elif tag.get("property", None) == "og:description":
                likesinstaa = tag.get("content", None)
                likesinsta = likesinstaa[:5]
                if len(likesinsta) >= 5:
                    likesinsta = likesinsta + 'k'

        instauserat = ilink[26:]
        instaacctslistdict[iw] = [ilink, instapagelink, contenttext, instaimage, likesinsta, instauserat]
    instaacctslist = list(instaacctslistdict.values())
    shuffle(instaacctslist)

    return render(request, 'homepageapp/home.html', {'valueslist' : valueslist, 'instaacctslist':instaacctslist})



