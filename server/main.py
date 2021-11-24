from typing import Optional
from fastapi import FastAPI
import os

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

