nohup uvicorn main:app --host 0.0.0.0 --port 80 > http.log &
nohup python3 record.py &
nohup python3 images.py &

