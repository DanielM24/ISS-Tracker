import requests
import os
from map import Map
from datetime import datetime

SUNSET_SUNRISE_ENDPOINT = "https://api.sunrise-sunset.org/json"
GEOCODE_ENDPOINT = "https://api.radar.io/v1/geocode/forward"
ISS_ENDPOINT = "http://api.open-notify.org/iss-now.json"
UTC_OFFSET = 2

geo_header = {
"Authorization": os.environ['RADAR_API_KEY']
}


def utc_to_local(utc_hour):
    utc_hour += UTC_OFFSET
    if UTC_OFFSET > 0:
        if utc_hour > 23:
            utc_hour -= 24
    elif UTC_OFFSET < 0:
        if utc_hour < 0:
            utc_hour += 24
    return utc_hour


def user_lat_lon(location):
    geo_parameter = {'query': location}
    geo_response = requests.get(GEOCODE_ENDPOINT, params=geo_parameter, headers=geo_header)
    user_latitude = geo_response.json()["addresses"][0]["latitude"]
    user_longitude = geo_response.json()["addresses"][0]["longitude"]
    return user_longitude, user_latitude


def check_hour(cord: tuple):
    time_now = datetime.now()
    sunset_sunrise_parameters = {"lat": cord[1], "lng": cord[0], "formatted": 0}
    sunset_response = requests.get(SUNSET_SUNRISE_ENDPOINT, params=sunset_sunrise_parameters)

    sunrise = int(sunset_response.json()['results']['sunrise'].split("T")[1].split(":")[0])
    sunset = int(sunset_response.json()['results']['sunset'].split("T")[1].split(":")[0])

    if time_now.hour >= utc_to_local(sunset) or time_now.hour <= utc_to_local(sunrise):
        return 'night'
    else:
        return 'day'


def check_iss_position():
    iss_response = requests.get(ISS_ENDPOINT)

    iss_longitude = float(iss_response.json()["iss_position"]["longitude"])
    iss_latitude = float(iss_response.json()["iss_position"]["latitude"])
    return iss_longitude, iss_latitude


def iss_above_head(time, user_cord, iss_cord):
    if time == 'night':
        if user_cord[0] - 5 <= iss_cord[0] <= user_cord[0] + 5 and user_cord[1] - 5 <= iss_cord[1] <= user_cord[1] + 5:
            print(f"Subject: Look up! 👆🛰\nThe ISS 🛰 is above you.")
            return False
        return True
    return True


world_map = Map()
user_location = world_map.screen.textinput("Location", "Please enter your location:")
user_cord = user_lat_lon(user_location)

map_type = check_hour(user_cord)
world_map.choose_background(map_type)
world_map.position_home(user_cord)

iss_cord = check_iss_position()

while iss_above_head(map_type, user_cord, iss_cord):
    iss_cord = check_iss_position()
    world_map.position_iss(iss_cord)

world_map.screen.mainloop()
