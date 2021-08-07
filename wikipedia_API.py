#!/usr/bin/env python3
import wikipedia

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

    print("3")
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
