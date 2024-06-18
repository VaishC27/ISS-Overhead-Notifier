# ISS-Overhead-Notifier
Ever wanted to know when the International Space Station (ISS) is creeping up on you from the dark abyss above? 
Now you can, with this nifty Python script that will send you an email whenever the ISS is overhead and it's dark outside!. 
Here's how it works!

## Features

ISS Position Tracking: Uses the Open Notify API to get the current position of the ISS.

Night Time Check: Determines if it's currently night at your location using the Sunrise-Sunset API.

Email Alerts: Sends you an email when the ISS is overhead and it's dark, so you can go outside and wave at the astronauts.

## Setup

Latitude and Longitude:
Set your location coordinates in the MY_LAT and MY_LONG variables.

Email Configuration:
Configure your email and password in the MY_EMAIL and MY_PASSWORD variables. (Pro tip: Don't share these with anyone, especially the password!)

Install Required Libraries:
Ensure you have the requests and smtplib libraries installed. If not, you can install them using:
sh

pip install requests

Run the Script:
Execute the script, sit back, and wait for the magic to happen.

import requests
from datetime import datetime
import smtplib
import time

# Your location coordinates
MY_LAT = 18.520430
MY_LONG = 73.856743
MY_EMAIL = "your_email@example.com"
MY_PASSWORD = "your_password"

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_position = (iss_longitude, iss_latitude)

    # Check if ISS is within +5 or -5 degrees of your position
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True

while True:

    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
           connection.starttls()
           connection.login(user=MY_EMAIL, password=MY_PASSWORD)
           connection.sendmail(from_addr=MY_EMAIL,
                               to_addrs=MY_EMAIL,
                               msg="Subject:Look UP!☝️\n\nThe ISS is above you in the sky")

                               
## Notes
The script checks the ISS position and whether it’s night every 60 seconds.
Ensure your email provider allows less secure apps or use an app-specific password if needed.


## Disclaimer
Use this at your own risk. Looking up at the sky for too long might cause neck strain, surprise alien abductions, or increased chances of spotting shooting stars. Enjoy responsibly!
