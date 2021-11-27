from typing import Optional
from fastapi import FastAPI, Form, Response, Cookie
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

def checkToken(token):
   part_1,part_2 = token.split("--")

   # Check if expired
   if(int(part_1.split("****")[0])>=time.time):
       return "Expired"

   # Check if faked
   hash = int.from_bytes(sha512(part_1.encode()).digest(), byteorder='big')
   with open("../pub.key","r") as f:
        e = int(f.read())

   with open("../key.n","r") as f:
        n = int(f.read())
   hashFromSignature = pow(signature, e, n)
   if hash != hashFromSignature:
        return "Faked"
    
   return "OK"

@app.get("/getMonths")
def read_root(jwt_token: Optional[str] = Cookie(None)):
    # List the videos dir and return the list
    if checkToken(jwt_token) != "OK":
        return "ERROR"
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

for i in range(97,122):
    charList.append(chr(i))

from hashlib import sha512
@app.post("/getToken")
def getToken(response: Response, psw: str = Form(...)):
    if sha512((psw + "udfafgfywyftwewtfegft653rf57twgedjhnsbccvfratkedyuhwfegfdtkwygcfwe5tcvwgkycgtw").encode()).hexdigest() != \
            "15e7208a9f5d4525aa02885d7654c5e982da73cf2447682b0c285eabfec2753855c4fe5fc0b2767e27d8515f59c66a56af8b2efcf44e25915b0dc83cbbb9315b":
                response.status_code = 403
                return "psw error"
    token_part1_time = int(time.time()) + 60*15 # 15 min
    token_part1_random = ''.join(random.choices(charList,k=100))
    msg_str = str(token_part1_time) + "****" + token_part1_random 
    msg = msg_str.encode()
    myhash = int.from_bytes(sha512(msg).digest(), byteorder='big')
    with open("../pvt.key","r") as f:
        d = int(f.read())

    with open("../key.n","r") as f:
        n = int(f.read())

    signature = pow(myhash, d, n)
    cookie = str(msg_str) + "--" + str(signature)
    response.set_cookie(key="jwt_token", value=cookie, samesite="strict")
    return "OK"

@app.get("/login", response_class=HTMLResponse)
def getLoginHTML():
    f = open("./client/login.html","r")
    html = f.read()
    f.close()
    return html
