from flask import Flask, redirect, url_for, render_template, request, session
import requests



app = Flask(__name__)
app.config['SECRET_KEY'] = "hello"
@app.route("/search")
def home():
    return render_template("weatherFrontPg1.html")
@app.route("/", methods=["POST","GET"])
def search():
    if request.method == "POST":
       cityname = request.form["nm"]
       url = "https://geo-services-by-mvpc-com.p.rapidapi.com/cities/findcitiesfromtext"

       querystring = {"sort": "population,desc", "language": "en", "q": cityname}

       headers = {
           'x-rapidapi-key': "d4a0225a37msh5ce9a8a7ed4b1a0p14605djsn678d50412bdc",
           'x-rapidapi-host': "geo-services-by-mvpc-com.p.rapidapi.com"
       }
       response = requests.request("GET", url, headers=headers, params=querystring)
       data = (response.json())
       dataDic = (data["data"])

       try:
           totalCityInfo = dataDic[0]

       except:
           session["cityname"] = "Toronto"
       else:
           session["cityname"] = totalCityInfo["name"]
           session["cityPopulation"] = totalCityInfo["population"]
           session["cityTimezone"] = totalCityInfo["timezone"]
           session["cityLong"] = totalCityInfo["longitude"]
           session["cityLat"] = totalCityInfo["latitude"]

       api_key = "c16c863ce5c92dda1d2ec048c19f3560"
       base_url = "https://api.openweathermap.org/data/2.5/weather?"
       city_name = session["cityname"]
       complete_url = base_url + "appid=" + api_key + "&q=" + city_name



       response = requests.get(complete_url)
       x = response.json()
       totalWeatherInfo = x["main"]
       session["tempNow"] =round(totalWeatherInfo["temp"] - 273.15)
       session["tempFeelsLike"] = round(totalWeatherInfo["feels_like"] - 273.15)
       session["tempMin"] = round(totalWeatherInfo["temp_min"] - 273.15)
       session["tempMax"] = round(totalWeatherInfo["temp_max"] - 273.15)
       session["tempHumidity"] = round(totalWeatherInfo["humidity"])
       return redirect(url_for("city"))
    else:
        return render_template("weatherFrontPg1.html")
@app.route("/city")
def city():
    infoCityName = session["cityname"]
    infoCityPopulation = session["cityPopulation"]
    infoCityTimezone = session["cityTimezone"]
    infoCityLong = session["cityLong"]
    infoCityLat = session["cityLat"]
    infoTempNow = session["tempNow"]
    infoTempFeelsLike = session["tempFeelsLike"]
    infoMin = session["tempMin"]
    infoMax = session["tempMax"]
    infoHumidity =  session["tempHumidity"]

    return render_template("base.html", citynameTitle = infoCityName, cityPopulation = infoCityPopulation , cityTimezone = infoCityTimezone, long = infoCityLong, lat = infoCityLat, tempNow=infoTempNow, feelsLike = infoTempFeelsLike, min = infoMin, max = infoMax, humitity = infoHumidity )
if __name__ == "__main__":
    app.run(debug=True)