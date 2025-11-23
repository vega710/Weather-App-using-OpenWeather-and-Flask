from flask import Blueprint, render_template, request
import requests
from flask import current_app as app
from datetime import datetime
#for local testing
from local_config import OPENWEATHER_API_KEY

main = Blueprint('main',__name__)

@main.route("/",methods=['GET','POST'])
def get_weather():
    data,img,icon_url,forcast,sunrise,sunset=None,None,None,None,None,None
    if request.method=='POST':
        city=request.form.get("cityname")
        if city:
            api_key=OPENWEATHER_API_KEY
            #api_key= app.config["OPENWEATHER_API_KEY"]
            api_url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
            response = requests.get(api_url)
            if response.status_code==200:
                data=response.json()
                data["main"]["temp"]=round(data["main"]["temp"])
                data["main"]["temp_min"]=round(data["main"]["temp_min"])
                data["main"]["temp_max"]=round(data["main"]["temp_max"])
                data["wind"]["speed"]= round(data["wind"]["speed"]*3.6,1)

                weather_state=data["weather"][0]["main"]
                if weather_state=='Clouds':
                    img='clouds.png'
                elif weather_state=='Drizzle':
                    img='drizzle.png'
                elif weather_state=='Rain':
                    img='rain.png'
                elif weather_state=='Snow':
                    img='snow.png'
                elif weather_state=='Clear':
                    img='clear.png'
                elif weather_state=='Mist':
                    img='mist.png'
                icon_url = f"../static/images/icons/{img}"

            else:
                data={"error":"City Not Found"}
            

            api_url=f"https://api.openweathermap.org/data/2.5/forecast?q={city}&cnt=1&units=metric&appid={api_key}"
            response = requests.get(api_url)
            if response.status_code==200:
                forcast=response.json()
                sunrise_utc_time = datetime.fromtimestamp(forcast["city"]["sunrise"])
                sunrise = sunrise_utc_time.strftime("%H:%M")
                sunset_utc_time = datetime.fromtimestamp(forcast["city"]["sunset"])
                sunset = sunset_utc_time.strftime("%H:%M")
                
                
            

        #icon = data["weather"][0]["icon"]
        #icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"
            
    return render_template('mainpage.html',data=data,icon_url=icon_url,forcast=forcast,sunrise=sunrise,sunset=sunset)