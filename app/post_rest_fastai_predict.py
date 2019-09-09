#!C:/bin/anaconda3/envs/pyweb/python.exe
print("HTTP/1.0 200 OK", end="")
print("Content-Type: application/json; charset=UTF-8\r\n\r\n", end="")
import time
g_start_time = time.time()
import datetime
import sys
import os
import torch
import psutil
import cgi
#
import fastai
#from fastai import *
from fastai.vision import *
from io import BytesIO
#
g_data = {}
#
#
#
def get_etime():
	global g_start_time
	etime = time.time() - g_start_time 
	g_start_time = time.time()
	return etime
#
def setup_learner(model_name):
  #model_name = "farm-animals_NkUj.pkl"
	path = Path(__file__).parent
	model_path = path.joinpath("models")
	try:
		learner = load_learner(model_path, model_name)
		return learner
	except RuntimeError as e:
		if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
			message = "This model was trained with an old version of fastai"
			raise RuntimeError(message)
		else:
			raise RuntimeError("Could not load leaner")
#
def get_sys_info():
	data = {}
	now = datetime.datetime.now()
	data.update({"current_time": now.strftime("%Y/%m/%d %H:%M")})
	data.update({"platform": sys.platform})
	data.update({"sys_version":sys.version})
	data.update({"torch_version":torch.__version__})
	data.update({"fastai_version":fastai.__version__})
	val = psutil.cpu_count()
	data.update({"cpu_number":val})
	val = psutil.cpu_freq()
	if (None == val):
		data.update({"cpu_speed_ghz": "not avail"})
	else:
		val = val._asdict()
		data.update({"cpu_speed_ghz":str(round((val["current"] / 1000), 2))})
		data.update({"cpu_max_speed_ghz":str(round((val["max"] / 1000), 2))})
	val = psutil.virtual_memory()._asdict()
	data.update({"ram_total_gb":str(round((val["total"] / (1024**3)), 2))})
	data.update({"ram_free_gb":str(round((val["available"] / (1024**3)), 2))})
	data.update({"cuda_gpu": str(torch.cuda.is_available())})
	val = psutil.disk_usage("/")._asdict()
	data.update({"disk_total_gb":str(round((val["total"] / (1024**3)), 2))})
	data.update({"disk_free_gb":str(round((val["free"] / (1024**3)), 2))})
	data.update({"current_path":str(os.path.abspath("."))})
	return data
#
#
#
g_form = cgi.FieldStorage()
g_data.update({"model_name": g_form.getvalue("model_name")})
#
#
g_data.update({"elapse1_load_time_sec": get_etime()})
g_learner = setup_learner("farm-animals_NkUj.pkl")
g_data.update({"elapse2_load_model_time_sec": get_etime()})
g_data.update({"model_classes": g_learner.data.classes})
#
#
g_img = open_image(BytesIO(g_form.getvalue("file")))
p,i,a = g_learner.predict(g_img)
g_data.update({'result': str(p), 'percent' : str(float(a[i]))})
#
#
g_data.update(get_sys_info())
g_data.update({"elapse3_predict_time_sec": get_etime()})
print(json.dumps(g_data), end="")
#