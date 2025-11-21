""""

from flask import Flask,jsonify, abort, render_template, request, redirect
import requests

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def get_weather():
    if request.method=='GET':
        api_url=f"https://api.openweathermap.org/data/2.5/weather?q=rabat&units=metric&appid=214d19ef5ad16169fd6dc7e2b2e9ae28"
        response = requests.get(api_url)
        data = response.json()
        data['main']['temp']=round(data['main']['temp'])
    else:
        city=request.form.get("cityname")
        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=214d19ef5ad16169fd6dc7e2b2e9ae28"
        response = requests.get(api_url)
        data = response.json()
        data['main']['temp']=round(data['main']['temp'])
    return render_template('mainpage.html',data=data)


if __name__=='__main__':
    app.run(debug=True)

"""