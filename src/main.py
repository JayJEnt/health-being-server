from fastapi import FastAPI
from mangum import Mangum

from contextlib import asynccontextmanager
from datetime import datetime as dt

from api.routers import (
    ingredients_ingredient_id,
    ingredients_ingredient_name,
    ingredients,
    recipes_recipe_id,
    recipes,
    users_user_id,
    users,
)
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

app.include_router(ingredients_ingredient_id.router)
app.include_router(ingredients_ingredient_name.router)
app.include_router(ingredients.router)
app.include_router(recipes_recipe_id.router)
app.include_router(recipes.router)
app.include_router(users_user_id.router)
app.include_router(users.router)

def handler(event, context):
    logger.debug(f"Event: {event}")

    
    asgi_handler = Mangum(app, lifespan="on", api_gateway_base_path='/dev')
    response = asgi_handler(event, context)
    
    return response

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Local mode: Development server started")
    uvicorn.run("main:app", port=8000, reload=True)