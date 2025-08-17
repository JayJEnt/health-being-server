from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from contextlib import asynccontextmanager
from datetime import datetime as dt

from api.routers import (
    diet_types,
    images,
    ingredients,
    oauth2,
    recipes,
    token_data,
    users,
    vitamins,
)
from logger import logger


startup_start = dt.now()
logger.info(f"Starting up the server... {startup_start}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for the FastAPI app."""
    startup_time = (dt.now() - startup_start).total_seconds()*1000
    logger.info(f"Server started in {startup_time:.2f} ms")
    yield
    shutdown_start = dt.now()
    logger.info(f"Shutting down the server... {shutdown_start}")
    logger.info(f"Server uptime: {shutdown_start - startup_start}")
    
    
app = FastAPI(lifespan=None)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root_handler():
    return {"message": "Hello!"}

app.include_router(diet_types.router)
app.include_router(images.router)
app.include_router(ingredients.router)
app.include_router(oauth2.router)
app.include_router(recipes.router)
app.include_router(token_data.router)
app.include_router(users.router)
app.include_router(vitamins.router)

def handler(event, context):
    logger.debug(f"Event: {event}")

    
    asgi_handler = Mangum(app, lifespan="on", api_gateway_base_path='/dev')
    response = asgi_handler(event, context)
    
    return response

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Local mode: Development server started")
    uvicorn.run("main:app", port=8000, reload=True)