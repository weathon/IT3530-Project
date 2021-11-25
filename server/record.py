script = """ffmpeg `#Use ffmpeg to record` \
        -f alsa  `# * Use alsa [6]` \
        -channels 4  `# Channel numbers are 4 for ps eyes` \
        -i hw:1,0  `# * Audio input [6]` \
        -video_size 640x480  `# Video size [7] [8]` \
        -i /dev/video0  `# Video input` \
        -t 60 `# 60 seconds for each clip, it should be placed before file name` \
        -r 0.5 -crf 0 -preset ultrafast `# Set frame rate to 5` \
        %d/%d/%d/%d.mp4 `# * The Pi is not fast enough, so we sacrifice space and use avi in exchange for speed` """
import os, datetime
if 1:
    time = datetime.datetime.now()
    os.system("mkdir %d/%d/%d -p" % (time.month, time.day, time.hour))
    os.system("mkdir %d/%d/%d -p" % (time.month, time.day, time.hour + 1)) # In case it is right on the time between hours
    os.system(script % (time.month, time.day, time.hour, time.minute))
