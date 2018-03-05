import os, sys, requests, tweepy
from bs4 import BeautifulSoup
from datetime import datetime

import logging
logger = logging.getLogger()
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
frmt = logging.Formatter('%(asctime)s - %(name)s:%(levelname)s - %(message)s')
ch.setFormatter(frmt)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

def get_forecast(city_url="https://www.yr.no/place/United_Kingdom/Scotland/Edinburgh/forecast.xml"):
    """Gets forecast data dict for city_url (from https://www.yr.no/.*/forecast.xml)"""
    logger.info("Getting yr.no data")
    r = requests.get(city_url)
    r.raise_for_status()
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
    logger.info("Got data")
    return data

def get_tweet(forecast):
    logger.info("Formatting tweet")
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

def tweet_weather():
    try:
        tweet = get_tweet(get_forecast())
        logger.info("Connecting to twitter api")
        auth = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['API_SECRET'])
        auth.set_access_token(os.environ['TOKEN'], os.environ['TOKEN_SECRET'])
        api = tweepy.API(auth)

        logger.info("Posting tweet")
        api.update_status(tweet)
        logger.info("Tweet successfully posted")
    except Exception as e:
        logger.exception(e)

if __name__ == '__main__':
    tweet_weather()
