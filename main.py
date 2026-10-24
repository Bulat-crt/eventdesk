#uvicorn main:app --reload
from fastapi import FastAPI
from app.routers.event_router import router as event_router
from app.routers.registration_router import router as registration_router

app = FastAPI()

app.include_router(event_router)
app.include_router(registration_router)