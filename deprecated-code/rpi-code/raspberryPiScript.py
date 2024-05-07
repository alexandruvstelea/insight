from rpi_lcd import LCD
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime, timedelta
import schedule
import requests
import json
import time
import logging

time.sleep(10)

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
)

BUTTON_1 = 17
BUTTON_2 = 27
BUTTON_3 = 22
BUTTON_4 = 5
BUTTON_5 = 6
INTERNET_CONNECTION = False
CURRENT_COURSE = "N/A"
API_URL = "http://192.168.1.134:5000"
LAST_SEND = None

ROOM = 1
ROOM_NAME = "NII1"
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON_1, GPIO.IN)
GPIO.setup(BUTTON_2, GPIO.IN)
GPIO.setup(BUTTON_3, GPIO.IN)
GPIO.setup(BUTTON_4, GPIO.IN)
GPIO.setup(BUTTON_5, GPIO.IN)

lcd = LCD()
lcd.clear()
lcd.text("System", 1)
lcd.text("Started", 2)
logging.info("System Started")


def display_no_internet():
    lcd.clear()
    lcd.text("Fara conexiune", 1)
    lcd.text("la internet!", 2)


def display_sent(grade: int):
    lcd.clear()
    lcd.text(f"Grade {grade}", 1)
    lcd.text("Sent to DB", 2)
    sleep(0.6)


def send_to_postgresql(grade, timestamp):
    global ROOM
    print(f"Sending to PostgreSQL grade {grade} with timestamp {timestamp}.")
    logging.info(
        f"Preparing to send to PostgreSQL grade {grade} with timestamp {timestamp}."
    )
    # data = {"rating":grade,"date":str(timestamp),"room":ROOM}
    data = {"rating": grade, "date": "2024-02-19 09:10:10.10", "room": ROOM}
    try:
        response = requests.post(
            API_URL + "/rating",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        if response.status_code == 200:
            print("POST successful")
            logging.info("Post successful")
        else:
            print("Post failed")
            print(response.text)
            logging.error(f"Post failed {response.text}")
    except requests.exceptions.Timeout as e:
        logging.error(f"Timeout error: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error in send_to_postgresql: {e}")


def send_grade(grade: int):
    global LAST_SEND
    current_send = datetime.now()
    if LAST_SEND == None or current_send - LAST_SEND >= timedelta(seconds=1.75):
        print(f"Send {grade} with timestamp {current_send}")
        logging.info(f"Send {grade} with timestamp {current_send}")
        LAST_SEND = current_send
        send_to_postgresql(grade, current_send)
        display_sent(grade)
        display_course()
    else:
        print("Too fast")
        logging.info("Too fast")


def display_course():
    lcd.clear()
    lcd.text(f"Curs: {CURRENT_COURSE}", 1)
    lcd.text(f"Sala: {ROOM_NAME}", 2)


def button_press(channel):
    if channel == BUTTON_1:
        send_grade(1)
    elif channel == BUTTON_2:
        send_grade(2)
    elif channel == BUTTON_3:
        send_grade(3)
    elif channel == BUTTON_4:
        send_grade(4)
    elif channel == BUTTON_5:
        send_grade(5)


def get_current_course():
    global CURRENT_COURSE
    global ROOM
    try:
        # data = {'date':str(datetime.now()),'room':ROOM}
        data = {"date": "2024-02-19 09:10:10.10", "room": ROOM}

        response = requests.get(
            API_URL + "/subjects/current",
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )
        data = response.json()
        CURRENT_COURSE = data["abbreviation"]
    except requests.exceptions.RequestException as e:
        print(f"An error ocurred: {str(e)}")
        logging.error(f"Error fetching current course: {e}")
    except Exception as e:
        logging.error(f"Unexpected error in get_current_course: {e}")


import os


def check_internet_connection():
    global INTERNET_CONNECTION
    pid = os.getpid()
    print(pid)
    try:
        response = requests.get("http://www.google.com", timeout=5)
        print(response)
        logging.info(f"Ping google respone: {response}")
        if response.status_code == 200:
            INTERNET_CONNECTION = True
            display_course()
        else:
            INTERNET_CONNECTION = False
    except requests.exceptions.ConnectionError:
        INTERNET_CONNECTION = False
        display_no_internet()
        logging.error("No internet connection available.")
    except Exception as e:
        logging.error(f"Unexpected error in check_internet_connection: {e}")


GPIO.add_event_detect(BUTTON_1, GPIO.BOTH, callback=button_press, bouncetime=800)
GPIO.add_event_detect(BUTTON_2, GPIO.BOTH, callback=button_press, bouncetime=800)
GPIO.add_event_detect(BUTTON_3, GPIO.BOTH, callback=button_press, bouncetime=800)
GPIO.add_event_detect(BUTTON_4, GPIO.BOTH, callback=button_press, bouncetime=800)
GPIO.add_event_detect(BUTTON_5, GPIO.BOTH, callback=button_press, bouncetime=800)
get_current_course()
check_internet_connection()
schedule.every(1).minutes.do(check_internet_connection)
schedule.every(5).minutes.do(get_current_course)
while True:
    schedule.run_pending()
    sleep(0.2)
