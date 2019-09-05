#!C:/bin/anaconda3/envs/pyweb/python.exe
import time
start_time = time.time()
import datetime
import sys
import cgi, cgitb 
import os
import torch
import psutil
import aiohttp
#
#import fastai
#import fastai.basic_train
#import asyncio
#from fastai import *
from fastai.vision import *
from io import BytesIO
#
#from starlette.applications import Starlette
#from starlette.middleware.cors import CORSMiddleware
#from starlette.responses import HTMLResponse, JSONResponse
#from starlette.staticfiles import StaticFiles


#
#
print("Content-Type: text/html\n")
#
#
#
def setup_learner(model_name):
	print("check-2")
  #model_name = "farm-animals_NkUj.pkl"
	path = Path(__file__).parent
	model_path = path.joinpath("models")
	try:
		learner = load_learner(model_path, model_name)
		#classes = learn.data.classes
		return learner
	except RuntimeError as e:
		print("check-x1")
		if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
			print(e)
			message = "This model was trained with an old version of fastai"
			raise RuntimeError(message)
		else:
			raise RuntimeError("Could not load leaner")
#
#
end_time = time.time()
print("check-1: ", end_time-start_time, " :sec")
start_time = time.time()
g_learner = setup_learner("farm-animals_NkUj.pkl")
print("check-3")
g_classes = g_learner.data.classes
print (str(g_classes))
end_time = time.time()
print ("check-4", end_time-start_time, " : sec")
start_time = time.time()
#
#
#
# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
first_name = form.getvalue('first_name')
last_name  = form.getvalue('last_name')
print("first_name: ", first_name, "last_name: ", last_name)
#
#
#
print ("<div><b>all import OK</b></div>")
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
end_time = time.time()
print("time: ", end_time-start_time, " :sec")
