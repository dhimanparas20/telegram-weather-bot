from dotenv import load_dotenv
from os import path,system,environ
from requests import get as rget
from datetime import datetime
import requests, json 
from time import sleep
import os

# Downloads the Config.env file
CONFIG_FILE_URL = environ.get('CONFIG_FILE_URL')
try:
    if len(CONFIG_FILE_URL) == 0:
        raise TypeError
    try:
        res = rget(CONFIG_FILE_URL)
        if res.status_code == 200:
            with open('config.env', 'wb+') as f:
                f.write(res.content)
        else:
            log_error(f"Failed to download config.env {res.status_code}")
    except Exception as e:
        log_error(f"CONFIG_FILE_URL: {e}")
except:
    pass       
  
# Loading Config Vars from Config.env file
load_dotenv('config.env', override=True)
def getConfig(name: str):
    return environ[name]
 
OPEN_WEATHER_API = ""    
OPEN_WEATHER_API = getConfig("OPEN_WEATHER_API")    
base_url = "https://api.openweathermap.org/data/2.5/weather?q="

def weather(city):
  url = f"{base_url}{city}&appid={OPEN_WEATHER_API}&units=metric"
  response = requests.get(url)
  if response.status_code == 200 :
    x = response.json()  
    print("-------------------------------| Weather JSON |-------------------------------")
    print(x)
    print("------------------------------------------------------------------------------")
    rise = x['sys']['sunrise']
    set = x['sys']['sunset']
    a = datetime.fromtimestamp(rise)
    b = datetime.fromtimestamp(set) 
    try:
        gnd_lvl = x['main']['grnd_level']
    except:
        gnd_lvl = "null"    
    return(        
      f"-------------|🏙️ {city} ({x['sys']['country']}) |---------------"+
      f"\n\n🌡️Current Temperature: {x['main']['temp']}°C"+
      f"\n🏝️Description:                 {x['weather'][0]['description']}"+
      f"\n🍃Wind Speed:                {x['wind']['speed']} m/s"+
      f"\n🌎Latitude:                       {x['coord']['lat']}°"+
      f"\n🌍Longitude:                    {x['coord']['lon']}°"+
      f"\n🍾Pressure:                      {x['main']['pressure']} mmHg"+
      f"\n🛬Ground Level:               {gnd_lvl} m"+
      f"\n👀Visibility:                       {x['visibility']} m"+
      f"\n🌅Sunrise(IST):                 {a} Am"+
      f"\n🌆Sunset(IST):                  {b} Pm"+
      f"\n-----------------------------------------------------"
    )  
  elif response.status_code == 404 :
    return f"City: {city} Not Found🙁. Please check the name or spelling."
  elif response.status_code == 401 :
    return "Invalid API🙁. Please get one form 'https://openweathermap.org/' ."
  elif response.status_code == 429 :
    return "API Limit exceeded 🙁 Current Plan. Please wait untill limit renewal."
  else :
    return "Unknown error occurred. Please try again"
    
