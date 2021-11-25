import os, datetime
from time import sleep
script = "fswebcam images/%d/%d/%d/%d/%d.jpg"
while 1:
    time = datetime.datetime.now()
    os.system("mkdir images/%d/%d/%d/%d -p" % (time.month, time.day, time.hour, time.minute))
    os.system("mkdir images/%d/%d/%d/%d -p" % (time.month, time.day, time.hour, time.minute + 1))
    os.system(script % (time.month, time.day, time.hour, time.minute, time.second))
    sleep(1)
