import flask
import pyowm.commons.exceptions
from pyowm import OWM
from flask import Flask, render_template, request

app = Flask(__name__)


def weather(city):
    try:
        owm = OWM('5dfdd607d0c33f12e428ca24dce76755')
        mgr = owm.weather_manager()

        obs = mgr.weather_at_place(city)
        w = obs.weather

        status = w.detailed_status
        wind = f"{w.wind()['speed']} km/h"
        humidity = f'{w.humidity}%'
        temp = f'{w.temperature("celsius")["temp"]}°'
        max_temp = w.temperature('celsius')["temp_max"]
        min_temp = w.temperature('celsius')["temp_min"]

        min_max = f"{max_temp}° - {min_temp}°"

        return status, wind, humidity, temp, min_max

    except (pyowm.commons.exceptions.NotFoundError, pyowm.commons.exceptions.APIRequestError):
        return render_template("result.html",
                               city="Not Found")

@app.route('/', methods=["GET"])
def entry():
    return render_template("entry.html")


@app.route('/result', methods=["POST"])
def result():
    city = request.form['city']

    status, wind, humidity, temp, min_max = weather(city)


    return render_template("result.html",
                           city=city.title(),
                           status=status.title(),
                           wind=wind,
                           humidity=humidity,
                           temp=temp,
                           temp_min_max=min_max)


if __name__ == '__main__':
    app.run(debug=True)
