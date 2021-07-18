"""
@version 1.0
@author Aurelius
"""
#!/usr/bin/env python3
import wikipedia
import tweepy
from credentials import*
import time
import datetime
import re
#from googletrans import Translator

auth = tweepy.OAuthHandler(API_key, API_secret_key)
auth.set_access_token(Access_token, Access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

exit = True
step = True
timer = 90
i = 89
j = 0
date = datetime.datetime.now()

File = 'last_tweets.txt'

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


def wiki_API(search):
    wikipedia.set_lang("de")
    try:
        try:
            print("1")
            text = wikipedia.summary(search, sentences=10)
            url0 = wikipedia.page(search)
        except:
            print("2")
            #searchlist = wikipedia.search(search)
            #search = searchlist[0]
            text = wikipedia.summary(search, sentences=10, auto_suggest=False)
            url0 = wikipedia.page(search,auto_suggest=False)
        text = bracket(text)
    except:
        url="https://www.wikipedia.de/"
        text="Leider nichts gefunden. Gegebenenfalls auf die Rechtschreibung achten."

    if len(text) > 200:
        subText = text[0:200]
        text = subText +"..."
    try:
        url = url0.url
    except:
        pass

    return [text, url]

def bracket(text):
    string=text
    result = ''
    result1=''
    paren= 0
    for ch in string:
        if ch == '(':
            paren =paren+ 1
            result = result + '(...'

        elif (ch == ')') and paren:
            result = result + ')'
            paren =paren- 1

        elif not paren:
            result += ch
    paren= 0
    for ch in result:
        if ch == '[':
            paren =paren+ 1
            result1 = result1 + '[...'

        elif (ch == ']') and paren:
            result1 = result1 + ']'
            paren =paren- 1

        elif not paren:
            result1 += ch

    return(result1)

def reply():
    print("checking for mentions...")
    tweets = api.mentions_timeline(                     #die Tweets der eigenen Timeline werden aufgerufen
        read_last_tweets(File), tweet_mode="extended")  #Überprüfung, welche Tweets schon bearbeitet wurden
    for tweet in reversed(tweets):                      #schleife in der tweets aus der Timeline vom ersten,
                                                            #noch nicht bearbeiteten Tweet an gelesen werden
                text = tweet.full_text                                              #alle Wörter, die nicht auf Wikipedia gesucht werden sollen werden
                try:
                    search = text.replace("@WikiBotpy ", "")
                except:
                    search = text.replace("@WikiBotpy", "")
                print("search for:" + search)
                list = wiki_API(search)                               #list ist ein Array dessen Inhalt die Rückgabe der Methode wiki_API beinhaltet
                response = list[0]                                    #Antworttext von Wikipedia
                url = list[1]
                print(str(tweet.id) + " - " + tweet.full_text +       #Verfassen einer Antwort mit Text von Wikipedia und der URL
                      " from " + tweet.user.screen_name)
                print("tweeting...", end='')
                if len(tweet.user.screen_name) + len(response) + len(url) + 3 > 280:    #wenn die Länge des Tweets insgesamt zu lang ist obwohl nur
                    response = " Artikel ist für Twitter zu lang. Hier der Link: "      #der erste Satz von Wikipedia genommen wurde
                api.update_status("@" + tweet.user.screen_name +                        #Verfassen der Antwort mit URL und Wiki-Text
                                  " " + response + " \n " + url, tweet.id)
                status = api.get_status(tweet.id)                                       #der Rest ist Gleich zu den Anderen Beispielen wie "Hallo"
                favorited = status.favorited
                if favorited == False:
                    api.create_favorite(tweet.id)
                time.sleep(2)
                print("success.")
                store_last_tweets(File, tweet.id)
                main()                                                 #zurückkehren zur main Methode, um Schleife zu durchbrechen

def follow():
    print("checking for new followers...")
    for follower in tweepy.Cursor(api.followers).items():   #Aufrufen der Follower über Tweepy
        if not follower.following:                          #wenn einem Follower nicht gefolgt wird, dann:
            follower.follow()                                   #wird er zurückgefolgt
            print("followed " + follower.screen_name)       #Ausgabe des Namens des Followers


def main():
    timer = 90              #ein Timer, der 15 min. zählt (90x(5+5))/ 60= 15
    i = 89                  #als Variable, die alle 10 sek. zählt
    step = True
    print("running...")
    while step:
        i = i+1
        reply()             #Methode zum Verfassen von Tweets und Überprüfung von Erwähnungen
        time.sleep(10)       #5 sek. warten, da Twitter ein "rate limit" festgelegt hat
        print("*")
        if i == 45:
            print("waiting...")
        if i == timer:      #wenn 15 min. um, dann Überprüfung auf neue Follower (rate limit)
            follow()        #Methode zum Zurückfolgen
            i = 0
        time.sleep(5)       #erneut warten

if __name__ == "__main__":
    main()
