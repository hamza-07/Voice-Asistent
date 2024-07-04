import pyttsx3
import time
import datetime
import speech_recognition as sr
import pyaudio
import wikipedia
import webbrowser
import os
import requests
import ctypes

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your personal assistant. How can I help you?")

def takeCommand():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        speak("Sorry, the service is unavailable. Please try again later.")
        return ""
    except Exception as e:
        print(e)
        return "None"
    return query

def set_volume(volume):
    devices = ctypes.windll.winmm.waveOutGetNumDevs()
    ctypes.windll.winmm.waveOutSetVolume(devices - 1, volume)

reminders = []

def add_reminder(reminder):
    reminders.append(reminder)
    speak("Reminder added.")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:  #if wikipedia found in the query then this block will be executed
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=1) 
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif "hello" in query:
            speak("Hello! How can I assist you today?")
        elif "how are you" in query:
            speak("I am just a program, but thank you for asking!")
        elif "what is your name" in query:
            speak("I am Hamza, your personal assistant.")
        elif "time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current_time}")
        elif "date" in query:
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            speak(f"Today is {current_date}")
        elif 'open youtube' in query:
            webbrowser.open("https://youtube.com")
        elif 'open google' in query:
            webbrowser.open("https://google.com")
        elif 'open linkedin' in query:
            webbrowser.open("https://linkedin.com")
        elif 'open indeed' in query:
            webbrowser.open("https://indeed.com")
        elif 'open code' in query:
            codePath = "C:\\Users\\ADMIN\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif "good bye" in query:
            speak("Goodbye! Have a great day.")
            exit()
        elif 'shutdown' in query:
            speak("Shutting down the system")
            os.system("shutdown /s /t 1")
        elif 'restart' in query:
            speak("Restarting the system")
            os.system("shutdown /r /t 1")
        elif 'sleep' in query:
            speak("Putting the system to sleep")
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif 'set volume' in query:
            speak("To what percentage?")
            volume_percentage = int(takeCommand().replace('%', ''))
            set_volume(volume_percentage * 65535 // 100)
            speak(f"Volume set to {volume_percentage}%")
        elif 'play music' in query:
            music_dir = 'E:\\DOWNLOAD\\Cheri Cheri Lady'
            try:
                songs = os.listdir(music_dir)
                if songs:
                    speak("Playing music")
                    os.startfile(os.path.join(music_dir, songs[0]))
                else:
                    speak("No songs found in the music directory.")
            except FileNotFoundError:
                speak("The specified music directory does not exist.")
            except Exception as e:
                speak("An error occurred while trying to play music.")
        elif 'set reminder' in query:
            speak("What is the reminder?")
            reminder = takeCommand()
            add_reminder(reminder)
        elif 'show reminders' in query:
            if reminders:
                speak("Here are your reminders:")
                for reminder in reminders:
                    speak(reminder)
            else:
                speak("You have no reminders.")
        else:
            speak("I am sorry, I didn't catch that. Could you please repeat?")
