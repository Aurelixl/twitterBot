"""
@version 1.0
@author Aurelius
"""
#!/usr/bin/env python3
import wikipedia
import tweepy
from wikipedia_API import *
from credentials import*
import time
import datetime
import re
import sys
import logging

auth = tweepy.OAuthHandler(API_key, API_secret_key)
auth.set_access_token(Access_token, Access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

step = True
File = 'last_tweets.txt'
FileN = "number.txt"

def date():
    date = datetime.date.today()
    timenow = datetime.datetime.now()
    timenow = timenow.strftime("%H:%M:%S")

    return [date,timenow]

now = date()
logging.root.handlers = []
logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)-5.5s]  %(message)s",
                    handlers=[logging.FileHandler("logs/{}.log".format(now[0]))])

def read_last_tweets(File):                         #Methode mit Parameter File in der die letzte Tweet ID gespeichert wurde
    file_read = open(File, "r")                     #öffnen der .txt Datei zum Lesen
    last_tweets_id = int(file_read.read().strip())  #initialisieren der Variable last_tweets_id aus der .txt Datei
    file_read.close()                               #schließen der Datei
    return last_tweets_id                           #Zurückgeben der ID


def store_last_tweets(File, last_tweets_id):    #Methode zum Speichern der letzten Tweet ID
    file_write = open(File, "w")                #öffnen der .txt Datei zum Schreiben
    file_write.write(str(last_tweets_id))       #ID Schreiben
    file_write.close()                          #schließen der Datei
    return

def get_Number(FileN):
    file_read = open(FileN, "r")
    currNumber = int(file_read.read().strip())
    file_read.close()
    return currNumber

def set_Number(FileN, currNumber):
    file_write = open(FileN, "w")
    file_write.write(str(currNumber))
    file_write.close()
    return

def reply():
    now = date()
    print("{}: checking for mentions...".format(now[1]))
    logging.info("{}: checking for mentions...".format(now[1]))
    tweets = api.mentions_timeline(                     #die Tweets der eigenen Timeline werden aufgerufen
        read_last_tweets(File), tweet_mode="extended")  #Überprüfung, welche Tweets schon bearbeitet wurden
    for tweet in reversed(tweets):                      #schleife in der tweets aus der Timeline vom ersten,
                                                            #noch nicht bearbeiteten Tweet an gelesen werden
                text = tweet.full_text                                              #alle Wörter, die nicht auf Wikipedia gesucht werden sollen werden

                search = ''.join([ word for word in text.split() if not word.startswith('@') ])
                print("{}: search for:".format(now[1]) + search)
                logging.info("{}: search for:".format(now[1]) + search)
                list = wiki_API(search)                               #list ist ein Array dessen Inhalt die Rückgabe der Methode wiki_API beinhaltet
                response = list[0]                                    #Antworttext von Wikipedia
                url = list[1]

                print("{}: ".format(now[1]) + str(tweet.id) + " - " + tweet.full_text +       #Verfassen einer Antwort mit Text von Wikipedia und der URL
                      " from " + tweet.user.screen_name)
                logging.info("{}: ".format(now[1]) + str(tweet.id) + " - " + tweet.full_text +       #Verfassen einer Antwort mit Text von Wikipedia und der URL
                      " from " + tweet.user.screen_name)
                print("{}: tweeting...".format(now[1]), end='', flush=True)
                logging.info("{}: tweeting...".format(now[1]))

                if len(tweet.user.screen_name) + len(response) + len(url) + 3 > 280:    #wenn die Länge des Tweets insgesamt zu lang ist obwohl nur
                    response = " Artikel ist für Twitter zu lang. Hier der Link: "      #der erste Satz von Wikipedia genommen wurde
                api.update_status("@" + tweet.user.screen_name +                        #Verfassen der Antwort mit URL und Wiki-Text
                                  " " + response + " #{}".format(get_Number(FileN)) + "\n" + url, tweet.id)
                status = api.get_status(tweet.id)                                       #der Rest ist Gleich zu den Anderen Beispielen wie "Hallo"
                favorited = status.favorited
                if favorited == False:
                    api.create_favorite(tweet.id)
                time.sleep(2)
                print("success.")
                logging.info("success, content: " + response)
                store_last_tweets(File, tweet.id)
                currNumber = get_Number(FileN)
                currNumber += 1
                set_Number(FileN, currNumber)
                #main()                                                 #zurückkehren zur main Methode, um Schleife zu durchbrechen
                return

def follow():
    now = date()
    print("{}: checking for new followers...".format(now[1]))
    logging.info("{}: checking for new followers...".format(now[1]))
    for follower in tweepy.Cursor(api.followers).items():   #Aufrufen der Follower über Tweepy
        if not follower.following:                          #wenn einem Follower nicht gefolgt wird, dann:
            follower.follow()                                   #wird er zurückgefolgt
            print("followed " + follower.screen_name)       #Ausgabe des Namens des Followers
            logging.info("followed " + follower.screen_name)

def timer():
    timer = 0
    while timer != 12:
        time.sleep(1)
        timer += 1
        print("* ", end="", flush=True)
    print("\n", end = "")
    return True

def main():
    timer15min = 900
    step = True
    now = date()
    print("{}: running...".format(now[1]))
    logging.info("{}: running...".format(now[1]))
    while step:
        if timer():
            reply()
            if timer15min==900:
                follow()
                timer15min = 0
            timer15min += 12

if __name__ == "__main__":
    main()
