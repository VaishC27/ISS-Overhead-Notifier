import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 18.520430
MY_LONG = 73.856743
MY_EMAIL = "your_email@example.com"
MY_PASSWORD = "Your app password"
#You need to generate app password from your gmail account.
# Here's a youtube link for the same "https://youtu.be/N_J3HCATA1c?si=zix9RSyKT_x9rRXZ"

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_position = (iss_longitude, iss_latitude)

    #Check if you position is within +5 or -5 degrees of iss position.
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <=iss_longitude <=MY_LONG+5:
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
    sunrise = int( data["results"]["sunrise"].split("T")[1].split(":")[0])
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




