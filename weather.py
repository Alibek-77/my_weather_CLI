import requests
from dotenv import load_dotenv
import os
from pathlib import Path
import json
import sys
load_dotenv()
weather_api_key=os.getenv("OPENWEATHER_API_KEY")
if not weather_api_key:
    raise ValueError("OPENWEATHER_API_KEY не найден в .env файле")
while True:
    print("=== Menedger of weather ===\n1.Show a weather of any city in current time\n2.Show your history\n3.Exit")
    punkt=int(input())
    if punkt>3 or punkt<=0:
        print("Incorrect number! Try again")
    match punkt:
        case 1:
           city=input("Enter a city: ")
           try:
                response=requests.get("https://api.openweathermap.org/data/2.5/weather",
                        params={
                            "q":city,
                            "appid":weather_api_key,
                            "units":"metric",
                            "lang":"ru"
                        },
                        timeout=10
                )
                response.raise_for_status()
                data=response.json()
                temp=data["main"]["temp"]
                feels_like=data["main"]["feels_like"]
                description=data["weather"][0]["description"]
                humidity=data["main"]["humidity"]
                wind_speed=data["wind"]["speed"]
                visibility=data["visibility"]
                weather={
                        "city":city,
                        "temp":temp,
                        "feels_like":feels_like,
                        "description":description,
                        "humidity":humidity,
                        "wind_speed":wind_speed,
                        "visibility":visibility
                    }
                path=Path("weather_CLI")/"history"/"log.json"
                path.parent.mkdir(exist_ok=True)
                try:
                   if path.exists():
                    history=json.loads(path.read_text(encoding='utf-8'))
                   else:
                    history=[]
                except json.JSONDecodeError :
                    print("Error of history!")
                history.append(weather)
                history=history[-10:]
                path.write_text(json.dumps(history,indent=2,ensure_ascii=False),encoding='utf-8')
                print(f"🌤 Weather in {city}\n──────────────────")
                print(f"Temperature: {temp}^C(Feels like {feels_like}^C)")
                print(f"Weather: {description}")
                print(f"Humidity: {humidity}")
                print(f"Wind: {wind_speed} m/s")
                print(f"Visibility: {visibility/1000:.1f} m ")
           except requests.Timeout:
                print("Server doesn't asnwer in 10 sec")
           except requests.ConnectionError:
                print("Not have connection!")
           except requests.HTTPError as e:
                if e.response.status_code==401:
                    print("Incorrect API key")
                elif e.response.status_code==404:
                    print("Not found!")
                else: 
                    print(f"Error server: {e.response.status_code}")
        case 2:
            path=Path("weather_CLI")/"history"/"log.json"
            data=json.loads(path.read_text(encoding='utf-8'))
            for i in data:
                print(f"City: {i["city"]}")
                print(f"Temperature: {i["temp"]}")
                print(f"Weather: {i["description"]}")
                print(f"Humidity: {i["humidity"]}")
                print(f"Wind speed: {i["wind_speed"]} m/s") 
                print(f"Visisbility: {i["visibility"]/1000:.1f} km")
                print("-----------------------")
            pass
        case 3:
            print("Good bye!")
            sys.exit()
    


