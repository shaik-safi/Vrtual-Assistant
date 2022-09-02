import news
import link
import system_status
import speech_recognition as sr
import pyttsx3
import pyautogui
import datetime
import pyjokes
import pywhatkit as kit
import os
import time
import cv2
import webbrowser
from covid import Covid
import wolframalpha
from selenium import webdriver
import wikipedia
import weathercom
import smtplib
import json
import subprocess
from tkinter import *
from PIL import ImageTk, Image

num = 1
def speak(output, my_lang = "en-uS"):
    engine = pyttsx3.init()
    engine.say(output)
    engine.runAndWait()

def virtual_listen():

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
        return

def listen():

    rObject = sr.Recognizer()
    audio = ''

    with sr.Microphone() as source:
        pyautogui.press('caplock')
        audio = rObject.listen(source, phrase_time_limit = 5)
    pyautogui.press('caplock')

    try:
        text = rObject.recognize_google(audio, language ='en-US')
        return text
    except:
        speak("Could not understand your audio, PLease try again !")
        text = None
        return text

def ai(text):
    try:
        try:
            app_id = "UH868R-2GYA3Y5V5J"
            client = wolframalpha.Client(app_id)
            res = client.query(text)
            answer = next(res.results).text
            return answer
        except:
            speak("I can search the Wikipedia for you, Do you want to continue?")
            answer = virtual_listen()
            if answer == "yes" or answer == "yea":
                answer = wikipedia.summary(text, sentences=2)
                speak("Answer from Wikipedia:")
                return answer
            else:
                return "Ok"
    except:
        return

def weather_report(city):
    weatherDetails = weathercom.getCityWeatherDetails(city)
    humidity = json.loads(weatherDetails)["vt1observation"]["humidity"]
    temp = json.loads(weatherDetails)["vt1observation"]["temperature"]
    phrase = json.loads(weatherDetails)["vt1observation"]["phrase"]
    answer = "currently in " + city + "  temperature is " + str(temp) + " degree celsius, " + "humidity is " + str(humidity) + " percent and sky is " + phrase
    return answer

def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak(Time)
    return Time

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    date_now = f'{date} {month} {year}'
    speak(date_now)
    return date_now

def wishme():
    speak("Hello I am NOVA")
    speak("The current time is")
    time()
    speak("The current date is")
    date()
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Good Afternon")
    elif hour >= 18 and hour < 24:
        speak("Good Evening")
    else:
        speak("Good Night")

def whatsapp_message():
    speak("Turning on Message mode")
    driver = webdriver.Chrome(executable_path=r"C:\Users\shaik\Desktop\Final\NOVA\chromedriver.exe")
    driver.get("https://web.whatsapp.com/")
    driver.maximize_window()
    speak("scan QR code")
    while(1):
        audio = virtual_listen()
        if audio == None:
            continue

        if "exit" in str(audio) or "stop" in str(audio) or "nothing" in str(audio) or "turn off" in str(audio):
            speak("Turning off Message mode")
            try:
                driver.find_element_by_xpath("//*[@id='side']/header/div[2]/div/span/div[3]/div").click()
                driver.find_element_by_xpath("//*[@id='side']/header/div[2]/div/span/div[3]/span/div/ul/li[7]").click()
                break
            except:
                break

        if "send" in audio or "Send" in audio:
            speak("whom shall i send:")
            audio = virtual_listen()
            if audio!=None:
                name = audio.lower()
                dic={'vishnu':'vishnu',
                    'harsha':'Harsha vardhan Dsu',
                    'srihari':'Srihari'}
                if name in dic:
                    contact_name=dic[name]
                    while(1):
                        speak("What should I send")
                        msg=virtual_listen()
                        if msg == None:
                                speak("Try again")
                                break
                        else:
                            user = driver.find_element_by_xpath("//span[@title='{}']".format(contact_name))
                            user.click()
                            msg_box = driver.find_element_by_xpath('''//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]''')
                            msg_box.send_keys(msg)
                            driver.find_element_by_xpath('''//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span''').click()
                            speak("whant to send another message")
                            answer = virtual_listen()
                            if answer == "yes":
                                continue
                            else:
                                break

                    else:
                        speak("No such contact found")
            else:
                speak("Try Again")
                continue
        else:
            continue

def email(input):
    input = "shaik"
    email_address = os.environ.get("email_address")
    email_password = os.environ.get('email_password')
    dic={'shaik':'shaiksafi2001@gmail.com'}
    if input in dic:
        receiver_email=dic[input]

        speak("what is subject?")
        subject = virtual_listen()
        speak("what is body?")
        body = virtual_listen()
        print(subject,body)


        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(email_address, email_password)
            msg = f"Subject: {subject}\n\n{body}"
            smtp.sendmail(email_address, receiver_email, msg)
            speak("email sent")
    else:
        speak("No email adress found")

def covid_status(country):
    covid = Covid(source="worldometers")
    try:
        covid_cases = covid.get_status_by_country_name(country)
        for x, y in covid_cases.items():
            info = x,y
            info_replace=info[0].replace("_"," ")
            speak(info_replace)
            speak(str(info[1]))
        return
    except:
        speak("No such country found")

def shortcut(input):
    dic={'open new tab':'ctrl+t',
        'reopen last tab':'ctrl+shift+t',
        'close tab':'ctrl+w',
        'open first tab':'ctrl+1',
        'open second tab':'ctrl+2',
        'open third tab':'ctrl+3',
        'open fourth tab':'ctrl+4',
        'open fifth tab':'ctrl+5',
        'open sixth tab':'ctrl+6',
        'open seventh tab':'ctrl+7',
        'open eight tab':'ctrl+8',
        'open last tab':'ctrl+9',
        'open next tab':'ctrl+tab',
        'open previous tab':'ctrl+shift+tab',
        'open new window':'ctrl+n',
        'opena new incognito window':'ctrl+shift+n',
        'close window':'ctrl+shift+w',
        'enter':'enter',
        'down':'down',
        'up':'up',
        'left':'left',
        'right':'right',
        'play':'playpause',
        'stop':'playpause',
        'scroll down':'pagedown',
        'scroll up':'pageup',
        'jump to beginning':'home',
        'jump to end':'end',
        'zoom in':'ctrl+=',
        'zoom out':'ctrl+-',
        'set zoom to normal':'ctrl+0',
        'full screen on':'f11',
        'full screen off':'f11',
        'video in fullscreen':'f',
        'come out of fullscreen':'f',
        'mute video':'m',
        'unmute video':'m',
        'reload tab':'ctrl+r',
        'jump to home':'alt+home',
        'jump to previous page':'alt+left',
        'jump to next page':'alt+right',
        'open history':'ctrl+h',
        'open downloads':'ctrl+j'}
    if input in dic:
        c=dic[input]
        ec=c.split('+')
        if len(ec) == 1:
            pyautogui.hotkey(ec[0],interval=0.1)
        if len(ec) == 2:
            pyautogui.hotkey(ec[0],ec[1],interval=0.1)
        if len(ec) == 3:
            pyautogui.hotkey(ec[0],ec[1],ec[2],interval=0.1)

def change_window():
    pyautogui.hotkey("ctrl","Alt","Tab")
    while(1):
        while(1):
            next = virtual_listen()
            if None == next:
                continue
            elif "ok" in next or "next" in next or "previous" in next:
                break
            else:
                continue
        if "ok" in next:
            pyautogui.press("enter")
            break
        elif "next" in next:
            pyautogui.press("right")
            continue
        elif "previous" in next:
            pyautogui.press("left")
            continue
        else:
            continue

def editing(input):
    dic={'copy':'ctrl+c',
        'cut':'ctrl+x',
        'select all':'ctrl+a',
        'paste':'ctrl+v',
        'save':'ctrl+s',
        'new file':'ctrl+n',
        'down':'down',
        'up':'up',
        'left':'left',
        'right':'right',
        'enter':'enter'}
    if input in dic:
        c=dic[input]
        ec=c.split('+')
        if len(ec) == 1:
            pyautogui.hotkey(ec[0],interval=0.1)
        if len(ec) == 2:
            pyautogui.hotkey(ec[0],ec[1],interval=0.1)
        if len(ec) == 3:
            pyautogui.hotkey(ec[0],ec[1],ec[2],interval=0.1)

    elif "type" in input or "write" in input:
        speak("what should I type")
        type = virtual_listen()
        if type != None:
            pyautogui.write(type)
        else:
            speak("try again")

    elif "ok" in input:
        pyautogui.press("enter")

    elif "change window" in input:
        change_window()

def process_text(input):
    try:
        if "covid" in input:
            speak("which country")
            country = listen()
            covid_status(country)

        elif "control mode" in input:
            speak("turning on control mode")
            while(1):
                audio = virtual_listen()
                if audio!=0:
                    if audio == None:
                        continue
                    if audio!=0:
                            text = audio
                    else:
                        continue
                    if "exit" in str(text) or "control mode off" in str(text) or "turn off" in str(text):
                        speak("Turning off control mode")
                        break
                    text = audio
                    if text == None:
                        continue
                    shortcut(text.lower())

                else:
                    continue

        elif "editing mode" in input:
            speak("turning on editing mode")
            while(1):
                audio = virtual_listen()
                if audio!=0:
                    if audio == None:
                        continue
                    if audio!=0:
                            text = audio
                    else:
                        continue
                    if "exit" in str(text) or "control mode off" in str(text) or "turn off" in str(text):
                        speak("Turning off control mode")
                        break
                    text = audio
                    if text == None:
                        continue
                    editing(text.lower())

                else:
                    continue

        elif "email" in input:
            try:
                speak("name?")
                receiver = virtual_listen()
                email(receiver.lower())
            except:
                return(0)

        elif "time" in input:
            speak("The current time is")
            time()

        elif "system status" in input:
            speak("Showing system status in console")
            # subprocess.run(r'python C:\Users\shaik\Desktop\Final\NOVA\system_status.py')
            system_status.status()

        elif "date" in input:
            speak("The current date is")
            date()

        elif "message mode" in input:
            whatsapp_message()

        elif "take screenshot" in input:
            speak("In what name should I save?")
            while True:
                pic = virtual_listen()
                if pic != None:
                    file =f"C:\\Users\\shaik\\Desktop\\Final\\NOVA\\screenshot\\{pic}.png"
                    img = pyautogui.screenshot(file)
                    os.startfile(file)
                    break
                else:
                    continue

        elif "news" in input:
            speak("What kind of news would u like")
            info = listen()
            news.get_news(info)

        elif "weather" in input:
            speak("which city?")
            city = listen()
            answer = weather_report(city)
            speak(answer)

        elif "change window" in input:
            change_window()

        elif "open" in input:
            app_name = input.replace("open", "")
            if app_name != None:
                pyautogui.press("win")
                pyautogui.write(app_name)
                pyautogui.press("enter")


            else:
                speak("try again")

        elif "open start" == input or "close start" == input:
            pyautogui.press("win")

        elif "minimize window" in input or "minimise window" in input:
            pyautogui.keyDown('win')
            pyautogui.press('down')
            pyautogui.press('down')
            pyautogui.press('down')
            pyautogui.keyUp('win')

        elif "maximize window" in input or "maximise window" in input:
            pyautogui.keyDown('win')
            pyautogui.press('up')
            pyautogui.press('up')
            pyautogui.press('up')
            pyautogui.press('down')
            pyautogui.press('up')
            pyautogui.keyUp('win')

        elif "mute" in input:
            pyautogui.press("volumemute")

        elif "volume up" in input:
            pyautogui.press("volumeup")

        elif "volume down" in input:
            pyautogui.press("volumedown")

        elif "scroll down" in input:
            pyautogui.press("pagedown")

        elif "scroll up" in input:
            pyautogui.press("pageup")

        elif "play" == input or "resume" == input:
            pyautogui.press("playpause")

        elif "pause" == input or "stop" == input:
            pyautogui.press("playpause")

        elif "close window" in input:
            pyautogui.hotkey("alt","f4")

        elif 'play' in input or "in youtube" in input or "on youtube" in input:
            if "play" in input[:4]:
                if "play"==input:
                    speak("please try again")
                    return
                else:
                    inp = input.replace("play", "")
                    kit.playonyt(inp)
                    return
            elif "in youtube" in input[-10:] or "on youtube" in input[-10:]:
                inp = input.replace("in youtube"or"on youtube" , "")
                web.open("https://youtube.com/search?q=%s" % inp)
                return
            else:
                link.search_web(input)
                return

        elif "what is " in input[:8] or "who is " in input[:7]:
            inp=input.replace("who is " or "what is ", "")
            link.search_web(inp)
            return

        elif 'search' in input:
                if "search"==input:
                    speak("please try again")
                    return
                else:
                    inp = input.replace("search ", "")
                    link.search_web(inp)
                    return

        elif "where is " in input or "locate" in input:
            location = input.replace("where is" or "locate", "")
            speak(location)
            input = location
            web.open("https://maps.google.com/maps?q=%s" % input)
            return

        elif "who are you" in input or "define yourself" in input or "your name" in input or "what is your name" in input:
            answer = '''Hello, I am Nova. Your personal Assistant.
            I am here to make your life easier.'''
            speak(answer)
            return

        elif "who made you" in input or "created you" in input:
            speak("I have been created by Shaik Safi and his team.")
            return

        elif 'joke' in input:
            speak(pyjokes.get_joke())
            return

        elif "who i am" in input or "who am i" in input:
            speak("If you talk then definately your human.")
            return

        elif "write a note" in input:
            speak("What should i write")
            note = listen()
            file = open(r'C:\Users\shaik\Desktop\Nova.txt', 'w+')
            file.write(note)
            file.close()

        elif "say my note" in input:
            speak("Showing Notes")
            file = open(r"C:\Users\shaik\Desktop\Nova.txt", "r+")
            read= file.read()
            speak(read)

        else:
            answer = ai(input)
            speak(answer)

    except:
        speak("I don't understand, I can search the web for you, Do you want to continue?")
        ans = listen()
        if 'yes' in str(ans) or 'yeah' in str(ans):
            pass
            link.search_web(input)
        else:
            return

def virtual():
    while(1):
        audio = virtual_listen()
        if audio!=0:
            if audio == None:
                continue

            if "nova" in audio or "Nova" in audio:
                speak("Listening")
                audio = virtual_listen()
                if audio!=0:
                        text = audio
                else:
                    continue

                if "exit" in str(text) or "turn off" in str(text):
                    speak("Turning off virtual mode")
                    break
                text = audio
                if text == None:
                    speak("try again")
                    continue
                process_text(text.lower())
            else:
                continue

class Widget:
    def __init__(self):
        root = Tk()

        root.title("NOVA ASSISTANT")
        root.geometry('1000x600')
        root.iconbitmap(r'C:\Users\shaik\Desktop\Final\NOVA\pictures\icon.ico')

        img=ImageTk.PhotoImage(Image.open(r"C:\Users\shaik\Desktop\Final\NOVA\pictures\NOVA.png"))
        panel=Label(root, image=img, bg="#2d2d2d")
        panel.pack(side="right", fill="both", expand="no")

        self.compText=StringVar()
        self.userText=StringVar()

        self.userText.set("Real Mode: This Mode runs your command once after you click this button.\nVirtual Mode: This mode takes your voice command many times until you mention 'EXIT' in your command.")

        userFrame=LabelFrame(root,text="User",font=("Black ops one",10, "bold"),fg="white",bg="#2d2d2d")
        userFrame.pack(fill="both",expand="yes")

        left=Message(userFrame,textvariable=self.userText,bg="#1F1F1F",fg="white")
        left.config(font=("Courier",20,"bold"))
        left.pack(fill="both",expand="yes")

        compFrame=LabelFrame(root,text="Nova",font=("Black ops one",10, "bold"),fg="white",bg="#2d2d2d")
        compFrame.pack(fill="both",expand="yes")

        left2=Message(compFrame,textvariable=self.compText,bg="#1F1F1F",fg="white")
        left2.config(font=("Courier",20,"bold"))
        left2.pack(fill="both",expand="yes")


        self.compText.set("Hello I am Nova")

        btn1=Button(root,text="Real Mode",font=("Black ops one",10, "bold"),bg="#353535",fg="white", command=self.real).pack(fill="both",expand="no")
        btn1=Button(root,text="Virual Mode",font=("Black ops one",10, "bold"),bg="#353535",fg="white", command=self.virtual).pack(fill="both",expand="no")
        btn2=Button(root,text="Exit",font=("Black ops one",10, "bold"),bg="#353535",fg="white", command=root.destroy).pack(fill="both",expand="no")

        root.mainloop()

    def virtual(self):
        answer = "Turning on virtual mode"
        self.compText.set("Turning on virtual mode")
        speak(answer)
        virtual()
        self.compText.set("Turning off virtual mode")

    def real(self):
        speak("Listening...")
        text=listen()
        if text == None:
            return
        else:
            self.userText.set(text)
            input = text.lower()

        try:
            if "covid" in input:
                speak("which country")
                country = virtual_listen()
                covid_status(country)
                self.compText.set(country)

            elif "system status" in input:
                speak("Showing system status in console")
                subprocess.run(r'python C:\Users\shaik\Desktop\Final\NOVA\system_status.py')
                self.compText.set("Showing system status in console")

            elif "time" in input:
                speak("The current time is")
                answer = time()
                self.compText.set(answer)

            elif "date" in input:
                speak("The current date is")
                answer = date()
                self.compText.set(answer)

            elif "news" in input:
                speak("What kind of news would u like")
                info = virtual_listen()
                news.get_news(info)
                self.compText.set("Getting News")

            elif "weather" in input:
                speak("which city?")
                city = virtual_listen()
                answer = weather_report(city)
                self.compText.set(answer)
                speak(answer)

            elif 'play' in input or "in youtube" in input or "on youtube" in input:
                if "play" in input[:4]:
                    if "play"==input:
                        speak("please try again")
                        self.compText.set("please try again")
                        return
                    else:
                        inp = input.replace("play", "")
                        kit.playonyt(inp)
                        self.compText.set("Playing")
                        return
                elif "in youtube" in input[-10:] or "on youtube" in input[-10:]:
                    inp = input.replace("in youtube"or"on youtube" , "")
                    web.open("https://youtube.com/search?q=%s" % inp)
                    self.compText.set("opening on youtube")
                    return
                else:
                    link.search_web(input)
                    self.compText.set("")
                    return


            elif "what is " in input[:8] or "who is " in input[:7]:
                inp=input.replace("who is " or "what is ", "")
                link.search_web(inp)
                self.compText.set("searching")
                return

            elif 'search' in input or 'open' in input or "please search" in input:
                if input[:4] == "open":
                    if "open"==input:
                        speak("please try again")
                        self.compText.set("please try again")
                        return
                    else:
                        inp = input.replace("open ", "")
                        link.search_web(inp)
                        self.compText.set("opening")
                        return
                elif input[:13] == "please search":
                    if "please search"==input:
                        speak("please try again")
                        self.compText.set("please try again")
                        return
                    else:
                        inp = input.replace("please search ", "")
                        link.search_web(inp)
                        self.compText.set("searching")
                        return
                elif input[:6] == "search":
                    if "search"==input:
                        speak("please try again")
                        self.compText.set("please try again")
                        return
                    else:
                        inp = input.replace("search ", "")
                        link.search_web(inp)
                        self.compText.set("searching")
                        return
                else:
                    link.search_web(input)
                    return


            elif "where am i" in input or "see my location" in input or "where i am" in input:
                speak("sorry  i can't")
                self.compText.set("sorry I can't")
                return

            elif "where is " in input or "locate" in input:
                location = input.replace("where is" or "locate", "")
                speak(location)
                input = location
                self.compText.set(input)
                webbrowser.open("https://maps.google.com/maps?q=%s" % input)
                return

            elif "who are you" in input or "define yourself" in input or "your name" in input or "what is your name" in input:
                answer = '''Hello, I am Nova. Your personal Assistant.\nI am here to make your life easier.'''
                speak(answer)
                self.compText.set(answer)
                return

            elif "who made you" in input or "created you" in input:
                answer = "I have been created by Shaik Safi and his team."
                speak(answer)
                self.compText.set(answer)
                return

            elif 'joke' in input:
                answer = pyjokes.get_joke()
                speak(answer)
                self.compText.set(answer)
                return

            elif "who i am" in input or "who am i" in input:
                speak("If you talk then definately your human.")
                self.compText.set("If you talk then definately your human")
                return

            elif "write a note" in input:
                speak("What should i write")
                note = virtual_listen()
                file = open(r'C:\Users\shaik\Desktop\Nova.txt', 'w+')
                file.write(note)
                file.close()
                self.compText.set(note)

            elif "show my note" in input or "see my note" in input:
                speak("Showing Notes")
                file = open(r"C:\Users\shaik\Desktop\Nova.txt", "r+")
                read= file.read()
                self.compText.set(read)
                speak(read)

            elif 'reason for you' in input or "why are you here" in input:
                speak("I was created as a Minor project by Shaik Safi")
                self.compText.set("I was created as a Minor project by Shaik Safi")
                return

            elif "nova" == input or "hello nova" == input or "hey nova" == input:
                answer = "I'm listening "
                self.compText.set(answer)
                speak("I'm listening ")
                return

            else:
                answer = ai(input)
                self.compText.set(answer)
                speak(answer)
                return

        except :
            speak("I don't understand, I can search the web for you, Do you want to continue?")
            ans = virtual_listen()
            if 'yes' in str(ans) or 'yeah' in str(ans):
                pass
                link.search_web(input)
            else:
                return

if __name__=='__main__':
    speak('INITIATING NOVA')
    #wishme()
    e = Widget()
