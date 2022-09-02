import speech_recognition as sr
import pyttsx3
import os
import webbrowser as web
from GoogleNews import GoogleNews
import nltk
from newspaper import Article

num = 1
def speak(output, my_lang = "en-uS"):
    engine = pyttsx3.init()
    engine.say(output)
    engine.runAndWait()

def listen():

    rObject = sr.Recognizer()
    audio = ''

    with sr.Microphone() as source:
        pyautogui.press('numlock')
        audio = rObject.listen(source, phrase_time_limit = 5)
    pyautogui.press('numlock')

    try:
        text = rObject.recognize_google(audio, language ='en-US')
        return text
    except:
        speak("Could not understand your audio, PLease try again !")
        return

def text(link):
    #Get the article
    url = link
    article = Article(url)
    # Do some NLP
    article.download() #Downloads the link’s HTML content
    article.parse() #Parse the article
    nltk.download('punkt')#1 time download of the sentence tokenizer
    article.nlp()# Keyword extraction wrapper
    #Get a summary of the article
    speak(article.summary)



def get_news(info):
    googlenews = GoogleNews()
    googlenews.search(info)
    news = googlenews.result()
    links = list()
    for new in news:
        for ne in new.items():
            if ne[0] == "link":
                links.append(ne[1])
            else:
                continue
    web.open(links[0])
    text(links[0])

if __name__ == "__main__":
    speak("What kind of news would u like")
    info = listen()
    get_news(info)
