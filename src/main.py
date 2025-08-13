from fastapi import FastAPI
from mangum import Mangum

from contextlib import asynccontextmanager
from datetime import datetime as dt

from api.routers import (
    diet_types_diet_type_id,
    diet_types,
    diet_types_name_diet_name,
    images,
    ingredients_ingredient_id,
    ingredients,
    ingredients_name_ingredient_name,
    oauth2_google,
    oauth2_our,
    recipes_recipe_id,
    recipes_search_phrase,
    recipes,
    token_data,
    users_email_email,
    users_name_username,
    users_owner_user_id,
    users,
    users_user_id,
)
from api.routers.vitamins import vitamins, vitamins_id, vitamins_name
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

@app.get("/")
def root_handler():
    return {"message": "Hello!"}

app.include_router(diet_types_name_diet_name.router)
app.include_router(diet_types_diet_type_id.router)
app.include_router(diet_types.router)
app.include_router(images.router)
app.include_router(ingredients_ingredient_id.router)
app.include_router(ingredients_name_ingredient_name.router)
app.include_router(ingredients.router)
app.include_router(oauth2_google.router)
app.include_router(oauth2_our.router)
app.include_router(recipes_recipe_id.router)
app.include_router(recipes_search_phrase.router)
app.include_router(recipes.router)
app.include_router(token_data.router)
app.include_router(users_email_email.router)
app.include_router(users_name_username.router)
app.include_router(users_owner_user_id.router)
app.include_router(users_user_id.router)
app.include_router(users.router)
app.include_router(vitamins_name.router)
app.include_router(vitamins_id.router)
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