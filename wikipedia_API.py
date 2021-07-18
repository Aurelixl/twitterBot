from bs4 import BeautifulSoup
import wikipedia
import re
exit =True

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


wikipedia.set_lang("de")
search = input("suche:")
print(search)

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

if len(text) > 200:                                 #wenn Zusammenfassung zu lang ist, wird nur der erste Satz genommen
    subText = text[0:200]
    text = subText +"..."                      #Emittlung der URL des Artikels
try:
    url = url0.url
except:
    pass

print(text)
print(url)
