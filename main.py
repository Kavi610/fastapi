from fastapi import FastAPI
from routes.router import endPoints
app=FastAPI()
app.include_router(endPoints)
