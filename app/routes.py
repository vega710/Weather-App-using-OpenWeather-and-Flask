from flask import Blueprint, render_template, request
import requests
from flask import current_app as app

main = Blueprint('main',__name__)

@main.route("/",methods=['GET','POST'])
def get_weather():
    city='rabat'
    
    if request.method=='POST':
        city=request.form.get("cityname")
    api_key= app.config["OPENWEATHER_API_KEY"]
    api_url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"

    response = requests.get(api_url)
    data=response.json()
    data["main"]["temp"]=round(data["main"]["temp"])
    data["wind"]["speed"]= round(data["wind"]["speed"]*3.6,1)
    icon = data["weather"][0]["icon"]
    icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"

    return render_template('mainpage.html',data=data,icon_url=icon_url)