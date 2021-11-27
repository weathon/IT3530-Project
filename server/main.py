from typing import Optional
from fastapi import FastAPI, Form, Response, Cookie
import os
from fastapi.responses import HTMLResponse, FileResponse
if os.name == 'posix': #On RPi
    from RPi import GPIO
    GPIO.setmode(GPIO.BCM) 
    import eink_lib


#pin = GPIO.PWM(20, 600)
import random
import time
app = FastAPI()


def checkToken(token):
   if token == None:
       return 'None'
   part_1,part_2 = token.split("--")

   # Check if expired
   if(int(part_1.split("****")[0])<time.time()):
       return "Expired"

   # Check if faked
   hash = int.from_bytes(sha512(part_1.encode()).digest(), byteorder='big')
   with open("../pub.key","r") as f:
        e = int(f.read())

   with open("../key.n","r") as f:
        n = int(f.read())

   signature = int(part_2)
   hashFromSignature = pow(signature, e, n)
   if hash != hashFromSignature:
        #print((signature,hashFromSignature))
        return "Faked"

   return "OK"

@app.get("/", response_class=HTMLResponse)
def index():
    f = open("./client/index.html","r")
    html = f.read()
    f.close()
    return html

@app.get("/getMonths_images")
def read_root(jwt_token: Optional[str] = Cookie(None)):
    # List the videos dir and return the list
    login_stat = checkToken(jwt_token)
    if login_stat != "OK":
        return "LOGIN ERROR"
    ls = os.listdir("./images")
    return ls

@app.get("/getDays_images",response_class=HTMLResponse)
def read_root(month, jwt_token: Optional[str] = Cookie(None)):
    # List the videos dir and return the list
    if checkToken(jwt_token) != "OK":
        return "LOGIN ERROR"
    ls = os.listdir("./images/"+month)
    f = open("./client/getdays.html","r")
    html = f.read()
    f.close()  
    html = html.replace("{{JSONDATA}}",str(ls)).replace("{{imagesOrAudio}}",'images').replace("{{month}}",month)
    return html


@app.get("/getHours_images", response_class=HTMLResponse)
def read_root(monthAndDay,jwt_token: Optional[str] = Cookie(None)):
    # List the videos dir and return the list
    if checkToken(jwt_token) != "OK":
        return "LOGIN ERROR"
    ls = os.listdir("./images/"+monthAndDay)
    f = open("./client/gethours.html","r")
    html = f.read()
    f.close()  
    html = html.replace("{{JSONDATA}}",str(ls)).replace("{{imagesOrAudio}}",'images').replace("{{before}}",monthAndDay)
    return html

@app.get("/getMins_images", response_class=HTMLResponse)
def read_root(monthAndDayAndHour,jwt_token: Optional[str] = Cookie(None)):
    # List the videos dir and return the list
    if checkToken(jwt_token) != "OK":
        return "LOGIN ERROR"
    ls = os.listdir("./images/"+monthAndDayAndHour)
    f = open("./client/getmin_images.html","r")
    html = f.read()
    f.close()  
    html = html.replace("{{JSONDATA}}",str(ls)).replace("{{imagesOrAudio}}",'images').replace("{{before}}",monthAndDayAndHour)
    return html


@app.get("/getImage")
def read_root(monthAndDayAndHourAndMinAndImageID,jwt_token: Optional[str] = Cookie(None)):
    # List the videos dir and return the list
    if checkToken(jwt_token) != "OK":
        return "LOGIN ERROR"
    return FileResponse("./images/"+monthAndDayAndHourAndMinAndImageID)



# Audio

@app.get("/getMonths_audio")
def read_root(jwt_token: Optional[str] = Cookie(None)):
    # List the videos dir and return the list
    login_stat = checkToken(jwt_token)
    if login_stat != "OK":
        return "LOGIN ERROR"
    ls = os.listdir("./audio")
    return ls

@app.get("/getDays_audio", response_class=HTMLResponse)
def read_root(month,jwt_token: Optional[str] = Cookie(None)):
    # List the videos dir and return the list
    if checkToken(jwt_token) != "OK":
        return "LOGIN ERROR"
    ls = os.listdir("./audio/"+month)
    f = open("./client/getdays.html","r")
    html = f.read()
    f.close()  
    html = html.replace("{{JSONDATA}}",str(ls)).replace("{{imagesOrAudio}}",'audio').replace("{{month}}",month)
    return html

@app.get("/getHours_audio", response_class=HTMLResponse)
def read_root(monthAndDay,jwt_token: Optional[str] = Cookie(None)):
    # print(monthAndDay)
    # List the videos dir and return the list
    if checkToken(jwt_token) != "OK":
        return "LOGIN ERROR"
    ls = os.listdir("./audio/"+monthAndDay)
    f = open("./client/gethours.html","r")
    html = f.read()
    f.close()  
    html = html.replace("{{JSONDATA}}",str(ls)).replace("{{imagesOrAudio}}",'audio').replace("{{before}}",monthAndDay)
    return html

@app.get("/getMins_audio", response_class=HTMLResponse)
def read_root(monthAndDayAndHour,jwt_token: Optional[str] = Cookie(None)):
    # List the videos dir and return the list
    if checkToken(jwt_token) != "OK":
        return "LOGIN ERROR"
    ls = os.listdir("./audio/"+monthAndDayAndHour)
    f = open("./client/getmin_audio.html","r")
    html = f.read()
    f.close()  
    html = html.replace("{{JSONDATA}}",str(ls)).replace("{{before}}",monthAndDayAndHour)
    return html
    


@app.get("/getAudio")
def read_root(monthAndDayAndHourAndMin,jwt_token: Optional[str] = Cookie(None)):
    # List the videos dir and return the list
    if checkToken(jwt_token) != "OK":
        return "LOGIN ERROR"
    return FileResponse("./audio/"+monthAndDayAndHourAndMin)



@app.get("/beep")
def beep(jwt_token: Optional[str] = Cookie(None)):
    if checkToken(jwt_token) != "OK":
        return "LOGIN ERROR"
    GPIO.setup(20, GPIO.OUT)
    pin = GPIO.PWM(20, 600)
    pin.start(50) # Duty cycle [14]
    time.sleep(5)
    pin.stop()

@app.post("/text")
def text(Text: str = Form(...),jwt_token: Optional[str] = Cookie(None)):
    if checkToken(jwt_token) != "OK":
        return "LOGIN ERROR"
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
