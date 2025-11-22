from flask import Blueprint, render_template, request
import requests
from flask import current_app as app

main = Blueprint('main',__name__)

@main.route("/",methods=['GET','POST'])
def get_weather():
    data,img,icon_url=None,None,None
    if request.method=='POST':
        city=request.form.get("cityname")
        if city:
            api_key= app.config["OPENWEATHER_API_KEY"]
            api_url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
            response = requests.get(api_url)
            response_state_code = response.status_code
            if response.status_code==200:
                data=response.json()
                data["main"]["temp"]=round(data["main"]["temp"])
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
            

        #icon = data["weather"][0]["icon"]
        #icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"
            
    return render_template('mainpage.html',data=data,icon_url=icon_url)