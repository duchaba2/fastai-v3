import aiohttp
import asyncio
import uvicorn
from fastai import *
from fastai.vision import *
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
#
#try:
#    x_model_name = sys.argv[2]
#except IndexError:
#    x_model_name = 'farm-animals_NkUj.pkl'
#export_file_url = 'https://www.dropbox.com/s/6bgq8t6yextloqp/export.pkl?raw=1'
x_model_name = 'pets_A9032.pkl'
learn = None
classes = None

#classes = ['cat', 'cattle', 'chicken', 'dog', 'donkey', 'duck', 'goat', 'goose', 'horse', 'pig', 'rabbit', 'sheep', 'turkey']
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))


async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f:
                f.write(data)


async def setup_learner(x_name=None):
    #await download_file(export_file_url, path / x_model_name)
    z_model_name = x_model_name
    path2 = path.joinpath("models")
    try:
        learn = load_learner(path2, z_model_name)
        classes = learn.data.classes
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "This model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

classes = learn.data.classes

@app.route('/')
async def homepage(request):
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())

@app.route('/original')
async def homepage(request):
    html_file = path / 'view' / 'old-index.html'
    return HTMLResponse(html_file.open().read())
   
@app.route('/analyze', methods=['POST'])
async def analyze(request):
    img_data = await request.form()
    model_name = img_data["model_name"]
    img_bytes = await (img_data['file'].read())
    img = open_image(BytesIO(img_bytes))
    prediction, z,w = learn.predict(img)
    return JSONResponse({'result': str(prediction), 'percent' : str(float(w[z])), 
			"classes": str(learn.data.classes), "model_name": model_name, "argv": str(sys.argv)})

# localhost: 127.0.0.1
if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="debug")
