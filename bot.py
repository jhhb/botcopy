__author__ = 'jamesboyle'

import sys
import json
import tweepy
import ssl
import random
import time

import datetime



CONSUMER_KEY =  ''
CONSUMER_SECRET = ''
ACCESS_TOKEN_KEY =  ''
ACCESS_TOKEN_SECRET = ''#removed keys

SW_LONG = -74.061584
SW_LAT =  40.582671
NE_LONG = -73.719635
NE_LAT = 40.830437

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        if CustomStreamListener.checkLocation(self, status) is True:
            if CustomStreamListener.checks_keywords(self, status) is True:
                CustomStreamListener.retweet(self, status)

    def checkLocation(self, status):

        myList = ['brooklyn', 'nyc', 'new york city', 'harlem', 'queens', 'bronx', 'the bronx', 'tribeca', 'soho', 'east village',
                  'manhattan', 'new york, new york', 'new york, ny', 'new york', 'staten island', 'lower east side', 'flushing', 'midtown',
                  'new york city, ny', 'nyc, ny', 'upper east side', 'upper west side', 'morningside heights', 'hamilton heights',
                  'washington heights', 'brooklyn heights', 'dumbo', 'williamsburg', 'park slope', 'astoria', 'midwood']

        userLocation = status.user.location.lower()
        inNewYork = False

        for i in range(0, len(myList)):

            if myList[i] == userLocation or myList[i] in userLocation:
                inNewYork = True
                return inNewYork

        listLoc = ['chinatown', 'china town', 'chelsea', 'upper east side', 'upper west side', 'soho','tribeca', 'flushing']
        listSpecific = ['ny', 'nyc', 'new york', 'manhattan', 'queens',]
        Loc = False
        Specific = False

        for n in range(0, len(listLoc)):
            if listLoc[n] == userLocation or listLoc[n] in userLocation:
                Loc = True
                break

        for z in range(0, len(listSpecific)):
            if listSpecific[z] == userLocation or listSpecific[z] in userLocation:
                Specific = True
                break

        if Loc is True and Specific is True:
            inNewYork = True
            return inNewYork

        myPlace = str(status.place)
        myPlace = myPlace.lower()

        for i in range(0, len(myList)):
            if myList[i] in myPlace:
                inNewYork = True
                return inNewYork


        if status.coordinates is not None:
            inNewYork = CustomStreamListener.parse_coordsforgeo(self, status)

        return inNewYork

    def parse_coordsforgeo(self, status):

        if status.coordinates is not None:

            coords = str(status.coordinates)

            firststart = 0

            for i in range(0, len(coords)):
                if coords[i] is '[':
                    firststart = i+1
                    break

            firstend = firststart

            while coords[firstend] is not ',':
                firstend = firstend+1

            secondstart = firstend + 1
            if coords[secondstart] is '' or ' ':
                secondstart = secondstart + 1

            secondend = secondstart

            while coords[secondend] is not ']':
                secondend = secondend + 1

            long = coords[firststart:firstend]
            longitude = float(long)
            lat = coords[secondstart:secondend]
            latitude = float(lat)

            if (SW_LONG < longitude < NE_LONG) and (SW_LAT <latitude < NE_LAT):
                return True

        return False

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

    def checks_keywords(self, status):      #retweets if at least one keyword from both sets is matched

        listAction = ['locked out', 'forgot my keys', 'left my keys', 'lost my keys', 'left the keys', 'lost the keys', 'forgot the keys']
        listLocation = ['apartment', 'house', 'apt', 'condo']
        actionBool = False
        locationBool = False

        for n in range(0, len(listAction)):
            if listAction[n] in status.text.lower():
                actionBool = True
                break

        for z in range(0, len(listLocation)):
            if listLocation[z] in status.text.lower():
                locationBool = True
                break

        if actionBool is True and locationBool is True:         ##THIS WORKS
            if 'RT' not in status.text:
                return True

        return False

    def retweet(self, status):

                reply = CustomStreamListener.random_response(self, status)

                if len(reply) > 140:
                    reply = reply[0:137]


                print "*************************"
                print status.user.screen_name
                print status.user.location
                print status.place
                print status.text
                print time.localtime()
                print status.id
                print "************************"

                current_time = datetime.datetime.now().hour

                if(8<= current_time < 24):
                    api.update_status(status = reply, ID = status.user.id_str)

    def editName(self, status):

        name = status.user.name

        for i in range(0, len(name), 1):
            if name[i] == ' ':
                return name[0:i]

        return name

    def random_response(self, status):        #selects one from 5 or 6 random statuses

        myRandom = random.randrange(1, 6)       ##gives a random number 1-5
        mySecondRandom = random.randrange(1, 6)

        if myRandom is 1:
            twitGreeting = 'Hello '

        elif myRandom is 2:
            twitGreeting = 'Hey there '

        elif myRandom is 3:
            twitGreeting = 'Hi '

        elif myRandom is 4:
            twitGreeting = 'Yo '

        elif myRandom is 5:
            twitGreeting = 'Hey '

        if mySecondRandom is 1:
            twitMessage = "if you're locked out still and want help, call us: 702-751-5625 http://flatironlocksmith.com"

        elif mySecondRandom is 2:
            twitMessage = "if you need help, dial our number! 702-751-5625 http://flatironlocksmith.com"

        elif mySecondRandom is 3:
            twitMessage = "we'd like to help if you're locked out. Give us a ring at 702-751-5625 http://flatironlocksmith.com"

        elif mySecondRandom is 4:
            twitMessage = "we can give you locksmithing. We'd love to help. Give us a ring: 702-751-5625 http://flatironlocksmith.com"

        elif mySecondRandom is 5:
            twitMessage = "if you're still locked out, call us at 702-751-5625 for help. http://flatironlocksmith.com"


        screenName = status.user.screen_name            ##status.user.screen_name.lower()
        personName = CustomStreamListener.editName(self, status)    ### status.user.name
        response =  twitGreeting + personName +', ' + twitMessage   ## 'drink up, ' + personName

        reply = '@' + screenName + ' ' + response

        return reply

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
sapi.filter(track = ['locked out', 'forgot my keys', 'left my keys', 'the keys', 'lost my keys', 'left the keys', 'lost the keys', 'forgot the keys'])    ##locations=[-180, -90, 180, 90])
##sapi.filter(locations=[-75, 40, -73, 41])
