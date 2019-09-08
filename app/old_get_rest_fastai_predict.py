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
from django.http import JsonResponse
#
#from starlette.applications import Starlette
#from starlette.middleware.cors import CORSMiddleware
#from starlette.responses import HTMLResponse, JSONResponse
#from starlette.staticfiles import StaticFiles

return_json = {}
#
#
#print("Content-Type: text/html\n")
#
#
#
def setup_learner(model_name):
	#print("check-2")
  #model_name = "farm-animals_NkUj.pkl"
	path = Path(__file__).parent
	model_path = path.joinpath("models")
	try:
		learner = load_learner(model_path, model_name)
		#classes = learn.data.classes
		return learner
	except RuntimeError as e:
		#print("check-x1")
		if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
			#print(e)
			message = "This model was trained with an old version of fastai"
			raise RuntimeError(message)
		else:
			raise RuntimeError("Could not load leaner")
#
#
end_time = start_time - time.time()
#print("check-1: ", end_time-start_time, " :sec")
return_json.update({"load_time_sec": str(end_time)})
start_time = time.time()
g_learner = setup_learner("farm-animals_NkUj.pkl")
#print("check-3")
g_classes = g_learner.data.classes
#print (str(g_classes))
return_json.update({"classes": str(g_classes)})
end_time = start_time - time.time()
return_json.update({"load_learner_time_sec": str(end_time)})
start_time = time.time()
#
#
#
# Create instance of FieldStorage 
'''
form = cgi.FieldStorage() 

# Get data from fields
file = form.getvalue('file')
model_name  = form.getvalue('model_name')
return_json.update({"model_name: ": model_name})
#
#
#

now = datetime.datetime.now()
return_json.update({"current_time": now.strftime("%Y/%m/%d %H:%M")})
return_json.update({"platform": sys.platform})
return_json.update({"python_version": sys.version})
return_json.update({"pytorch": torch.__version__})
#print ("<li>Fastai version is: ", fastai.__version__, "</li>")
val = psutil.cpu_count()
return_json.update({"cpu_count": val})
val = psutil.cpu_freq()
if (None != val):
	val = val._asdict()
	return_json.update({"cpu_speed_ghz": str(round((val["current"] / 1000), 2))})
	return_json.update({"cpu_max_ghz": str(round((val["max"] / 1000), 2))})
else:
	return_json.update({"cpu_speed" : "none"})
val = psutil.virtual_memory()._asdict()
return_json.update({"ram_total_gb": str(round((val["total"] / (1024**3)), 2))})
return_json.update({"ram_free_gb": str(round((val["available"] / (1024**3)), 2))})
return_json.update({"is_cuda": str(torch.cuda.is_available())}) # @UndefinedVariable
val = psutil.disk_usage("/")._asdict()
return_json.update({"disk_total_gb": str(round((val["total"] / (1024**3)), 2))})
return_json.update({"disk_free_gb": str(round((val["free"] / (1024**3)), 2))})
return_json.update({"abs_path": os.path.abspath(".")})
end_time = start_time - time.time()
return_json.update({"total_time_sec", str(end_time)})
'''
return JsonResponse(return_json)