#!C:/bin/anaconda3/envs/pyweb/python.exe
import datetime
import sys
import torch
import psutil
import os
#import fastai
print("Content-Type: text/html\n")
print ("<h2>Hello from Python. This is super cool!</h2>")
now = datetime.datetime.now()
print ("<ol><li>System current date and time is: ", now.strftime("%Y/%m/%d %H:%M"), "</li>")
print ("<li>The platform is: ", sys.platform, "</li>")
print ("<li>Python version is: ", sys.version, "</li>")
print ("<li>PyTorch version is: ", torch.__version__, "</li>")
#print ("<li>Fastai version is: ", fastai.__version__, "</li>")
val = psutil.cpu_count()
print ("<li>The Number of CPU is: ", val, "</li>")
val = psutil.cpu_freq()
if (None != val):
	val = val._asdict()
	print ("<li>CPU current speed is: ", str(round((val["current"] / 1000), 2)), "GHz</li>")
	print ("<li>CPU max speed is: ", str(round((val["max"] / 1000), 2)), "GHz</li>")
else:
	print ("<li>CPU speed is not available.</li>")
val = psutil.virtual_memory()._asdict()
print ("<li>RAM total is: ", str(round((val["total"] / (1024**3)), 2)), "Gb</li>")
print ("<li>RAM free is: ", str(round((val["available"] / (1024**3)), 2)), "Gb", " : ", str(100 - val["percent"]), "%</li>")
print ("<li>GPU-Cuda available: ", torch.cuda.is_available()) # @UndefinedVariable
val = psutil.disk_usage("/")._asdict()
print ("<li>Disk space total is: ", str(round((val["total"] / (1024**3)), 2)), "Gb</li>")
print ("<li>Disk space free is: ", str(round((val["free"] / (1024**3)), 2)), "Gb", " : ", str(100 - val["percent"]), "%</li>")
print ("<li>The current directory:", os.path.abspath("."), "</li>")

print ("</ol>")

