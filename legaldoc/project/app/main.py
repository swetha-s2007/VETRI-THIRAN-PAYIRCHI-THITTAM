from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .database import Base,engine
from .routes.pages import router as page_router
from .routes.api import router as api_router
load_dotenv(); Base.metadata.create_all(bind=engine)
app=FastAPI(title='PocketSmart AI',version='1.0.0')
app.add_middleware(CORSMiddleware,allow_origins=['http://127.0.0.1:8000','http://localhost:8000'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
Path('uploads').mkdir(exist_ok=True); app.mount('/static',StaticFiles(directory='static'),name='static'); app.include_router(page_router); app.include_router(api_router)
@app.on_event('startup')
def startup(): Base.metadata.create_all(bind=engine)
