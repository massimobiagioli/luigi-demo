from dataclasses import dataclass
from typing import List

import requests
from bs4 import BeautifulSoup

LANGUAGE = 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
BASE_URL = 'https://www.google.com/search?q=weather+{}'


@dataclass
class WeatherForecast:
    city: str
    province: str
    temperature: str
    precipitation: str
    humidity: str
    wind: str


def get_weather_data(cities: List[str]) -> List[WeatherForecast]:
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE

    result = []
    for city in cities:
        html = session.get(BASE_URL.format(city))
        soup = BeautifulSoup(html.text, "html.parser")
        region = soup.find("div", attrs={"id": "wob_loc"}).text.split(' ')
        result.append(WeatherForecast(
            city=region[0],
            province=region[1],
            temperature=soup.find("span", attrs={"id": "wob_tm"}).text,
            precipitation=soup.find("span", attrs={"id": "wob_pp"}).text,
            humidity=soup.find("span", attrs={"id": "wob_hm"}).text,
            wind=soup.find("span", attrs={"id": "wob_ws"}).text,
        ))
    return result
