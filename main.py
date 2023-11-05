from datetime import datetime
import requests
import smtplib
import math
import time
from dotenv import load_dotenv
import os


def configure():
    load_dotenv()


configure()

MY_LAT = os.getenv("MY_LAT")
MY_LONG = os.getenv("MY_LONG")
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0
}
# Sunrise and Sunset time API
response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
time_data = response.json()

# Sunrise/Sunset hour and Current hour of the day
sunrise = int(time_data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(time_data["results"]["sunset"].split("T")[1].split(":")[0])
time_now = datetime.now()
time_hour = time_now.hour

# ISS location API
response = requests.get(url="http://api.open-notify.org/iss-now.json", params=parameters)
response.raise_for_status()
iss_data = response.json()

# ISS current location
iss_latitude = float(iss_data["iss_position"]["latitude"])
iss_longitude = float(iss_data["iss_position"]["longitude"])


threshold = 100.0
distance = math.sqrt((abs(float(MY_LAT) - iss_latitude)**2 + abs(float(MY_LONG) - iss_longitude)**2))

# Check if ISS is close to my position and is dark time
while True:
    if distance < threshold and sunrise > time_hour > sunset:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=MY_EMAIL,
                                msg=f"Subject: ISS IS HERE!\n\n LOOK AT THE SKY FAST, ISS IS PASSING BY")
    time.sleep(60)
