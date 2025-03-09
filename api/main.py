from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, aiagents

from .database import Base, engine

app = FastAPI() 

Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get("/")
def health_check():
    return "Health check complete"

app.include_router(auth.router)
app.include_router(aiagents.router)