import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_forecast():
    r = requests.get("https://www.yr.no/place/United_Kingdom/Scotland/Edinburgh/forecast.xml")
    soup = BeautifulSoup(r.text, "lxml")
    forecast = soup.findAll('time')
    data = {}
    for i in range(4): ## Change depending on time of pull (range(1,5) for 6AM today till 6AM tomorrow?)
        x = forecast[i]
        date_from = datetime.strptime(x['from'], "%Y-%m-%dT%H:%M:%S")
        date_to = datetime.strptime(x['to'], "%Y-%m-%dT%H:%M:%S")
        date = "{}".format(date_from.strftime("%H:%M"))
        data[date] = {
            'symbol': x.find('symbol')['name'],
            'precip': x.find('precipitation')['value'],
            'temp': x.find('temperature')['value'],
            'wind': x.find('windspeed')['name'],
            'pressure': x.find('pressure')['value']
        }
    return data

def get_tweet(forecast):
    results = []
    for date in forecast:
        tweet = ""
        data = forecast[date]
        tweet += "{} - {}°C, {}".format(date, data['temp'], data['symbol'])
        if float(data['precip']) > 0: tweet += " ({}mm)".format(data['precip'])
        extra_info = ", {} hPa".format(data['pressure'])
        if len(tweet) + len(extra_info) < 70:
            tweet += extra_info
        extra_info = ", {}".format(data['wind'])
        if len(tweet) + len(extra_info) < 70:
            tweet += extra_info
        results.append(tweet)
    return "\n".join(results)
