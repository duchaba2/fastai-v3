#!C:/bin/anaconda3/envs/pyweb/python.exe
print("HTTP/1.0 200 OK", end="")
print("Content-Type: application/json; charset=UTF-8\r\n\r\n", end="")
import time
start_time = time.time()
import json
import sys

data = json.dumps({"cat": "catfood"})
print(data, end="")