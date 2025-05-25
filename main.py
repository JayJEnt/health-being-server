from contextlib import asynccontextmanager
from datetime import datetime as dt
from fastapi import FastAPI
from mangum import Mangum

from api.routers import recipe
from api.routers import refrigerator
from api.routers import test
from logger import configure_logger

logger = configure_logger()
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

@app.get("/")
def root_handler():
    return {"message": "Hello!"}

app.include_router(test.router)
app.include_router(recipe.router)
app.include_router(refrigerator.router)

def handler(event, context):
    logger.debug(f"Event: {event}")

    
    asgi_handler = Mangum(app, lifespan="on", api_gateway_base_path='/dev')
    response = asgi_handler(event, context)
    
    return response

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Local mode: Development server started")
    uvicorn.run("main:app", port=8000, reload=True)