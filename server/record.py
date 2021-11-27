audio_script = """ ffmpeg -f alsa  `# * Use alsa [6]` \
        -channels 4 `# Channel numbers are 4 for ps eyes` \
        -i hw:1,0 # * Audio input [6]` \
        -t 65 audio/%d/%d/%d/%d.wav """
import os, datetime
while 1:
    time = datetime.datetime.now()
    os.system("mkdir audio/%d/%d/%d -p" % (time.month, time.day, time.hour))
    os.system("mkdir audio/%d/%d/%d -p" % (time.month, time.day, time.hour + 1)) # In case it is right on the time between hours
    os.system(audio_script % (time.month, time.day, time.hour, time.minute))
