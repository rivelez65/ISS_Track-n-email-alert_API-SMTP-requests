import requests
from datetime import datetime
import smtplib
import time
import plot
import os
from dotenv import load_dotenv

# CALL ENVIRONMENT VARIABLES
load_dotenv()
MY_EMAIL = os.environ.get('MY_EMAIL')
MY_PASSWORD = os.environ.get('MY_PASSWORD')

# TORONTO COORDINATES
MY_LAT = 43.589046
MY_LONG = -79.644119

# API REQUEST PARAMETERS
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

# PERSONALIZED MESSAGE TELLING THE ISS IS PASSING OVERHEAD
personalized = "Look up if the Sky is clear tonight!! \n\n You have a high chance of spotting the ISS \n\n GOOD LUCK" \
               "\n\n Sincerely: Ricky"

# TO FIND OUT WHETHER ITS DARK OUTSIDE
time_today = datetime.now().hour

# PLOT ISS POSITION USING TURTLE
iss = plot.IssPlotter()


while True:
    # REQUEST ISS COORDINATES EVERY 30SECOND INTERVALS
    time.sleep(30)
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    longitude = iss_response.json()["iss_position"]["longitude"]
    latitude = iss_response.json()["iss_position"]["latitude"]
    iss_position = (latitude, longitude)

    # SCALE DOWN ISS COORDINATES TO FIT WORLD IMAGE GRID IN TURTLE
    iss_x = float(longitude) * (15/8.8)
    iss_y = float(latitude) * (15/7.8)

    # PLOT CURRENT POSITION OF ISS
    iss.iss.goto(iss_x, iss_y)
    iss.iss.pendown()

    # FOR DEBUGGING PURPOSES
    # print(f"ISS Position: {iss_position}")
    # print(f"Mississauga:  ({MY_LAT},{MY_LONG})\n\n")

    # IF ISS POSITION IS WITHIN GIVEN MARGIN OF ERROR AND IT IS BETWEEN 9PM AND 5AM SEND EMAIL ALERT
    if -3 < float(longitude) - MY_LONG < 3:
        if -3 < float(latitude) - MY_LAT < 3:
            if time_today <= 5 or time_today >= 21:

                with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                    connection.starttls()
                    connection.login(
                        user=MY_EMAIL,
                        password=MY_PASSWORD
                    )
                    connection.sendmail(
                        from_addr=MY_EMAIL,
                        to_addrs=MY_EMAIL,
                        msg=f'Subject: ISS PASSING OVERHEAD!\n\n {personalized}'
                    )
