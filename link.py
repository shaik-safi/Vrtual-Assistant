
import speech_recognition as sr
import pyautogui
import os
import requests
from bs4 import BeautifulSoup
import re
import webbrowser
import urllib.parse
from urllib.parse import urlparse
import pyttsx3

def speak(output, my_lang = "en-uS"):
    engine = pyttsx3.init()
    engine.say(output)
    engine.runAndWait()

def virtual_listen():

    rObject = sr.Recognizer()
    audio = ''

    with sr.Microphone() as source:

        audio = rObject.listen(source, phrase_time_limit = 5)

    try:
        text = rObject.recognize_google(audio, language ='en-US')
        return text
    except:
        speak("Could not understand your audio, PLease try again !")
        text = None
        return text

def googleSearch(query):
    links = [ ]
    url = f"https://google.com/search?q={query}"
    webbrowser.open(url)
    try:
            html = requests.get(url)
            if html.status_code==200:
                soup = BeautifulSoup(html.text, 'lxml')
                anchors = soup.find_all('a')
                for i in anchors:
                    k = i.get('href')
                    try:
                        m = re.search("(?P<url>https?://[^\s]+)", k)
                        n = m.group(0)
                        rul = n.split('&')[0]
                        domain = urlparse(rul)
                        if(re.search('google.com', domain.netloc)):
                            continue
                        else:
                            links.append(rul)
                    except:
                        continue
    except:
        pass

    finally:
        return links
def search_web(search):
    links = googleSearch(search)
    speak("Do you want to open any link?")
    answer = virtual_listen()
    print(answer)
    if 'yes' in answer or 'yeah' in answer or 'open link' in answer:
        while(1):
            speak("Which link do you want to open")
            name = virtual_listen()
            print(name)
            if name == 0:
                continue
            else:
                break
        name = name.replace(" ","")
        done = list()
        for n in links:
            if name.lower() in n and n not in done:
                webbrowser.open(n)
                speak("Is this link Right?")
                condition = virtual_listen()
                if "no" in condition:
                    done.append(n)
                    pyautogui.hotkey("ctrl","w",interval=0.1)
                    continue
                else:
                    break
    else:
        return
