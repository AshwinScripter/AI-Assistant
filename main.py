import pyttsx3 
import datetime
import requests
import json
import speech_recognition as sr
import pyautogui
import webbrowser as wb
import wikipedia
import openai 
from time import sleep
import pywhatkit # for youtube video
from newsapi.newsapi_client import NewsApiClient
#import random
import clipboard
import os # Not working till now need to be implemented
import cv2
import pyjokes
import time as tt
import json
import spotipy
import webbrowser
import psutil 
from geolocation import*
#import nltk


engine = pyttsx3.init()
# This function is responsible give audio to the text
def give_audio(audio):
  engine.say(audio)
  rate = engine.getProperty('rate')
  engine.setProperty('rate', rate+1)
  engine.runAndWait()
 
# This is the way to switch either Peter or Peri
def change_voice(voice):
    voices = engine.getProperty('voices')
    if voice == 1:
      engine.setProperty('voice',voices[0].id)
      give_audio("Hello MindSync this side")
    if voice == 2:
      engine.setProperty('voice',voices[1].id)
      give_audio("Hello  MindSync this side")
    
    
# This function will give you tell you about the time 
def time(Region,City):
      response = requests.get('https://timeapi.io/api/Time/current/zone?timeZone={0}/{1}'.format(Region,City))
      python_data= json.loads(response.text)
      time = python_data.get('time')
      date = python_data.get('dateTime')
      audio = "The date of {0} is{1} and time is {2}".format(City,date,time)
      give_audio(audio)


def greeting():
  hour = datetime.datetime.now().hour
  if hour >= 6 and hour <12:
    give_audio("Good Morning Sir/Mam")
  elif hour >=12 and hour < 16:
    give_audio("Good Afternoon Sir/Mam")
  elif hour >=16 and hour < 22:
    give_audio("Good Evening Sir/Mam")
  else:
    give_audio("Good Night Sir/Mam")
    
def greet():
  give_audio("I hope you are having a great time")
  
def spotify():
    username = '312bbtvlmtk5wqnoaekqngq4gzcu'
    clientID = 'de1e825ee6844b91bb2e67c54cbbaad6'
    clientSecret = '1f0851e424d449718a206eb9b8bdefac'
    redirectURI = 'http://google.com/' 
    oauth_object = spotipy.SpotifyOAuth(clientID,clientSecret,redirectURI)
    token_dict = oauth_object.get_access_token()
    token = token_dict['access_token']
    spotifyObject = spotipy.Spotify(auth=token)
    user = spotifyObject.current_user()
    json.dumps(user,sort_keys=True, indent=4)
    while True:
        give_audio("Choose 0 if you want to  Exit")
        give_audio("Choose 1 if you want to search for a Song")
        give_audio("Your Choice: ")
        choice = int(takeCommandMic())
        if choice == 1:
        # Get the Song Name.
            give_audio("Say Song Name")
            searchQuery = takeCommandMic()
        # Search for the Song.
            searchResults = spotifyObject.search(searchQuery,1,0,"track")
        # Get required data from JSON response.
            tracks_dict = searchResults['tracks']
            tracks_items = tracks_dict['items']
            song = tracks_items[0]['external_urls']['spotify']
        # Open the Song in Web Browser
            webbrowser.open(song)
            print('Song has opened in your browser.')
        elif choice == 0:
            break
        else:
            print("Enter valid choice.")

def gpt3(s):
  openai.api_key = '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'
  response = openai.Completion.create(
    model="text-curie-001",
    prompt=s,
    temperature=0.2,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0
  )
  name = response['choices'][0].text
  print(name)
  give_audio(name)
  
def wishme(name):
    give_audio("Welcome back Friend")
    give_audio("How may I help you")
    return
    
"""def take_cmd():
  query = input("How may I help you?")
  return query"""


def takeCommandMic():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    print("Listening .....")
    audio = r.record(source,duration=3)
  try:
    print("recognizing ...")
    query = r.recognize_google(audio,language="en-IN")
    print(query)
  except Exception as e:
     print(e)
     give_audio("Say  that again Please......")
     return 'None'
  return query
  
def sendwhatappmsg(ph_no,msg):
  Message = msg
  wb.open('https://web.whatsapp.com/send?phone='+ph_no+'&text='+Message)
  sleep(10)
  pyautogui.press('enter')
  
def searchgoogle():
  give_audio("what should I search for?")
  search = takeCommandMic()
  wb.open('https://www.google.com/search?q={}'.format(search ))
  
def news(new):
  news_api = NewsApiClient(api_key = '3b048370cf9e498d98e27301a2ea9f0b')
  data = news_api.get_top_headlines(q = new,language = 'en',page_size =5)
  newsdata = data['articles']
  for x,y in enumerate(newsdata):
    print(f'{x}{y["description"]}')
    give_audio(f'{x}{y["description"]}')
  give_audio("That's it for now I'll update you in some time")
def texttospeech():
  text = clipboard.paste()
  print(text)
  give_audio(text)
  
def capturepic():
  cam = cv2.VideoCapture(0)
  cv2.namedWindow("Python Webcam Screenshot App")
  
  img_counter =0
  while True:
    ret,frame  = cam.read()
    if not ret:
      print("Failed to grab frame")
      break
    cv2.imshow("test",frame)
    k = cv2.waitKey(1)
    if k%256 == 27:
      print("Escape hit closing the app")
      break
    elif k%256 == 32:
      img_name = "opencv_frame_{}.png".format(img_counter)
      cv2.imwrite(img_name,frame)
      print("screenshot taken")
      img_counter+=1
  cam.release()
  cam.destroyAllWindows()
      
      
  cam.release()
  cam.destroyAllWindows()
  
def screenshots():
  name_img = tt.time()
  name_img =  'C:\\Users\\sharm\\Pictures\\Screenshots\\{}.png'.format(name_img)
  img = pyautogui.screenshot(name_img)
  img.show()
def cpu():
  usage = str(psutil.cpu_percent())
  give_audio('CPU is at'+usage)
  battery = psutil.sensors_battery()
  give_audio("Battery is at")
  give_audio(battery.percent)


if __name__ == "__main__":
    change_voice(1)
    """give_audio("What your name Sir")
    name = takeCommandMic()"""
    wishme("Rupesh")
    greet()
    while True:
      query = takeCommandMic().lower()
      if 'current' in query:
        time('Asia','Calcutta')
      elif 'time' in query :
        give_audio("Say Region")
        region = takeCommandMic()
        give_audio("Say City")
        City = takeCommandMic()
        time(region,City)
      elif 'greet' in query:
        greeting()
        
      elif 'message' in query:
        user_name = {"Rupesh":"+91 8882126868","BU Riyuuuuu":"+91 8279705881","Avni Gupta BU":"+91 7972052184","Ashwin":"+91 9412424002"
                      }
        try:
          give_audio("To whom you want to send the Whats app message")
          name = takeCommandMic()
          ph_no = user_name[name]
          give_audio("What is the message?")
          message = takeCommandMic()
          sendwhatappmsg(ph_no,message)
          give_audio("Message has been send")
        except Exception as e:
          print(e)
          give_audio("unable to send the message")
          
      elif 'wikipedia' in query:
        give_audio("searching on wikipeida...")
        query = query.replace("wikipedia","")
        result = wikipedia.summary(query,sentences = 2)
        print(result)
        give_audio(result)
      elif 'google' in query:
        searchgoogle()
        
      elif 'youtube' in query:
        give_audio("what should I search for on youtube?")
        topic = takeCommandMic()
        
        pywhatkit.playonyt(topic)
      elif 'weather' in query:
        city = query.replace("what is the weather of","")
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid=dc1bd9d9718ec49bb299a339416ac853'
        res = requests.get(url)
        data = res.json()
        weather = data['weather'][0]['main']
        temp = data['main']['temp']
        temp = round((temp-32)*5/9)
        des = data['weather'][0]['description']
        print(weather)
        print(temp)
        print(des)
        give_audio(f'weather in {city} city is like')
        give_audio("Temperature:{} degree celcius".format(temp))
        give_audio("weather is {}".format(des))
        
      elif 'news' in query:
        new = query.replace("what's the news about","")
        news(new)
      elif 'read' in query:
        texttospeech()
      elif "picture" in query:
        capturepic()
      elif "document" in query:
        codepath = 'explorer C://{}'.format(query.replace('Open',''))
        os.system(codepath)
      elif "joke" in query:
        give_audio(pyjokes.get_joke())
        
      elif "screenshot" in query:
        screenshots()
        
      elif "song" in query:
        spotify()
      elif "location" in query:
        call()
      elif "cpu" in query:
        cpu()
      else:
        gpt3(query)
        break

  
