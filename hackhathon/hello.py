import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random
import webbrowser
import wikipedia
import pywhatkit as kit
import smtplib
import sys
import time
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime, QDate, Qt, QThread
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QMainWindow, QApplication
from ak1 import Ui_MainWindow
import openai

# OpenAI API Setup
client = openai.OpenAI(api_key="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")  # Replace with your actual API key

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    """Convert text to speech."""
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def chat_with_gpt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except openai.OpenAIError as e:
        return f"OpenAI API error: {str(e)}"
    except Exception as e:
        return f"General error: {str(e)}"

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good morning, sir.")
    elif hour < 18:
        speak("Good afternoon, sir.")
    else:
        speak("Good evening, sir.")
    speak("I am Ciri. How can I assist you today?")

def sendEmail(to, content):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("your_email@gmail.com", "your_password")  # Use app password
        server.sendmail("your_email@gmail.com", to, content)
        server.close()
        speak("Email has been sent successfully.")
    except Exception as e:
        speak("Sorry, I couldn't send the email.")

def news():
    try:
        response = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=your_news_api_key").json()
        articles = response.get("articles", [])
        for i, article in enumerate(articles[:5]):
            speak(f"News {i+1}: {article['title']}")
    except Exception as e:
        speak("Sorry, I couldn't fetch the news.")

class mainthread(QThread):
    def __init__(self):
        super(mainthread, self).__init__()

    def run(self):
        self.TaskExecution()

    def takecommand(self):    
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            try:
                audio = r.listen(source, timeout=3, phrase_time_limit=8)
            except sr.WaitTimeoutError:
                speak("Listening timed out. No speech detected.")
                return "none"
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Could not understand. Please say that again.")
            return "none"
        except sr.RequestError:
            speak("Internet issue detected.")
            return "none"
    
    def TaskExecution(self):
        wish()
        while True:
            query = self.takecommand()
            if "open notepad" in query:
                os.startfile("C:\\Windows\\notepad.exe")
            elif "open command prompt" in query:
                os.system("start cmd")
            elif "open camera" in query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow("Webcam", img)
                    if cv2.waitKey(50) == 27:
                        break
                cap.release()
                cv2.destroyAllWindows()
            elif "play music" in query:
                music_dir = "C:\\music"
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, random.choice(songs)))
            elif "ip address" in query:
                ip = requests.get("https://api.ipify.org").text
                speak(f"Your IP address is {ip}")
            elif "wikipedia" in query:
                speak("Searching Wikipedia...")
                results = wikipedia.summary(query.replace("wikipedia", ""), sentences=2)
                speak("According to Wikipedia")
                speak(results)
            elif "open youtube" in query:
                webbrowser.open("www.youtube.com")
            elif "open google" in query:
                speak("What should I search?")
                cm = self.takecommand()
                webbrowser.open(f"https://www.google.com/search?q={cm}")
            elif "write an email" in query:
                speak("What should I say?")
                content = self.takecommand()
                sendEmail("recipient_email@gmail.com", content)
            elif "tell me news" in query:
                speak("Fetching the latest news.")
                news()
            elif "chat with me" in query or "talk to gpt" in query:
                speak("What do you want to ask ChatGPT?")
                user_input = self.takecommand().lower()
                if user_input and user_input != "none":
                    chat_response = chat_with_gpt(user_input)
                    speak(chat_response)
                    print("ChatGPT:", chat_response)
            elif "you can sleep" in query:
                speak("Goodbye, sir.")
                sys.exit()
            speak("Do you have any other work, sir?")

startExecution = mainthread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QMovie("gif1.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        self.ui.textBrowser.setText(current_date.toString(Qt.ISODate))
        self.ui.textBrowser_2.setText(current_time.toString("hh:mm:ss"))

app = QApplication(sys.argv)
ciri = Main()
ciri.show()
exit(app.exec_())
