
def strconvert(str1):
    
    strfin=str()
    for j in str1:
        if j.isspace():
            k='+'
            strfin=strfin+'+'
            
        elif j.isalpha():
            strfin+=j
            
        elif j.isdigit():
            strfin+=j
            
        else:
            k='%2C'
            strfin+=k
            
            
    return(strfin)

import pyttsx3
engine = pyttsx3.init()
def give_audio(audio):
  engine.say(audio)
  rate = engine.getProperty('rate')
  engine.setProperty('rate', rate+1)
  engine.runAndWait()
import speech_recognition as sr
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
  
import requests
import json
import webbrowser
import os
import osmapi as osm



apikeyHERE='FxqQgO0TcW0jDSuqYZsGGH9P7pBtUMVRsHCtseHICz8'

def geocoder(location):

    geodata1= requests.get('''https://geocode.search.hereapi.com/v1/geocode?q={}&apiKey={}'''.format(strconvert(location),apikeyHERE))
   
    
    for j in geodata1.json()['items']:
        return(j['position'])

def call():
    give_audio("Enter your present Location: ")
    curr_loc = takeCommandMic()
    give_audio("Enter your destination location: ")
    dest_loc =takeCommandMic()
    try:
        
        precision= 3
    
    except TypeError as e:
        print(e)
    
    
    if (precision>=1 and precision<=5):
        
    
        curr_dest_coor= geocoder(curr_loc)
        dest_loc_coor= geocoder(dest_loc)
    
        fdir=open(r'C:\Users\sharm\Desktop\AI-Assistant-\Directions.txt','w')
    
        direction_req= requests.get('https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248c7a32d7041a74717955795c64a764975&start={},{}&end={},{}'.format(curr_dest_coor['lng'],curr_dest_coor['lat'],dest_loc_coor['lng'],dest_loc_coor['lat']))


        for j in direction_req.json()['features'][0]['properties']['segments'][0]['steps']:
        
            if j['type']==1 or j['type']==0:
                fdir.write(j['instruction']+' after '+str(j['distance'])+'m\n')
            
            elif j['type']==10:
                fdir.write(j['instruction'])
            
            else:
                fdir.write(j['instruction']+' for '+str(j['distance'])+'m\n')
            
            

    
        api_id_route='AphwXYEtEeiCtwNztr61INL9X2TIvciykQ52ndCvkz6zoefafNs2eBCRkcw2ysgw'
    
    
        webbrowser.open('https://dev.virtualearth.net/REST/v1/Imagery/Map/Road/Routes?wp.0={};64;1&wp.1={};66;2&mapsize=3840,3840&key={}'.format(curr_loc,dest_loc,api_id_route))
    
    
        req= requests.get('http://router.project-osrm.org/route/v1/driving/{},{};{},{}?alternatives=false&annotations=nodes'.format(curr_dest_coor['lng'],curr_dest_coor['lat'],dest_loc_coor['lng'],dest_loc_coor['lat']))
    
    
        for k in req.json()['routes']:
        
            for j in k['legs']:
            
                nodlist=(j['annotation']['nodes'])
            
            
        a=len(nodlist)//(10*precision)
    
        coorlist=[]
    

    
    
        for j in range(10*precision):
        
            api=osm.OsmApi()
        
            node=api.NodeGet(nodlist[a*j])
        
            coorlist.append([node['lon'],node['lat']])
        
        f1=open(r'C:\Users\LENOVO\Desktop\Jarvis\sam\WEATHERUPDATE.txt','w')
    
        ct=1
    
        for j in coorlist:
            url = "https://trueway-geocoding.p.rapidapi.com/ReverseGeocode"
    
            querystring = {"location":"","language":"en"}
       
            querystring['location']='{},{}'.format(j[1],j[0])
    
            headers = {
            'x-rapidapi-key': "3eee248b85msh0f86b28523b503ep1e5e0cjsn8e799f3be69e",
            'x-rapidapi-host': "trueway-geocoding.p.rapidapi.com"
            }
    
    
            response = requests.request("GET", url, headers=headers, params=querystring)
        

            for l in response.json()['results']:
        
                if l['location_type']=='centroid':
                    f1.write(str(ct)+') '+l['address']+':\n')
                
                    ct+=1
                    break
            
                else:
                
                    f1.write(str(ct)+') '+l['address']+':\n')
                
                    ct+=1
                    break
            
            
        
            apikeyweather='f7e1687a0d052b9da768a4b12055265f'
        
            reqweather=requests.get('https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=hourly,daily,minutely&appid={}'.format(j[1],j[0],apikeyweather))
        
            for l in reqweather.json()['current']['weather']:
            
                f1.write(l['description']+':\n')
            
            
            f1.write("TEMPERATURE(in C):{} \n".format(int(reqweather.json()['current']['temp'])-273))
        
            f1.write('FEELS LIKE:(in C) {}\n'.format(int(reqweather.json()['current']['feels_like'])-273))
        
            f1.write('Humidity %: {}\n'.format(reqweather.json()['current']['humidity']))
        
            if 'alerts' in reqweather.json():
            
                f1.write('Visibility(in meters): {}\n'.format(reqweather.json()['current']['visibility']))
                f1.write('ALERTS (courtesy {}): {}\n\n\n'.format(reqweather.json()['alerts'][0]['sender_name'],reqweather.json()['alerts'][0]['description']))


            else:
                f1.write('Visibility(in meters): {}\n\n\n'.format(reqweather.json()['current']['visibility']))
        
        f1.close()
    
        fdir.close()

        os.startfile('WEATHERUPDATE.txt')
    
        os.startfile('Directions.txt')
        
    
    else:
        print('Invalid detail value. Pls recheck and try again!')
