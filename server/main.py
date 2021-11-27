from typing import Optional
from fastapi import FastAPI, Form
import os
from fastapi.responses import HTMLResponse
import eink_lib
from RPi import GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
pin = GPIO.PWM(20, 500)
import random

app = FastAPI()

@app.get("/getMonths")
def read_root():
    # List the videos dir and return the list
    monthes = os.listdir("../record/videos")
    return monthes

@app.get("/getDays")
def get_days(month):
    days = os.listdir("../record/videos/%s/" % month)
    return days

@app.get("/listVideos")
def list_videos(month,day):
    video_list = os.listdir("../record/videos/%s/%s" % (month,day))
    return video_list

@app.get("/beep")
def beep():
    pin.start(10) # Duty cycle [14]
    time.sleep(5)
    pin.stop()

@app.post("/text")
def text(Text):
    eink_lib.show(Text)

charList = []
#ASCII
for i in range(65,90):
    charList.append(chr(i))

for i in range(97,126):
    charList.append(chr(i))

@app.post("/getToken")
def getToken(psw: str = Form(...)):
    token_part1_time = int(time.time()) + 60*15 # 15 min
    token_part1_random = ''.join(random.choices(charList,k=100))
    

@app.get("/login", response_class=HTMLResponse)
def getLoginHTML():
    f = open("./client/login.html","r")
    html = f.read()
    f.close()
    return html
