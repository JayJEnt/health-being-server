from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from contextlib import asynccontextmanager
from datetime import datetime as dt

from api.routers.admin_role import (
    diet_types_admin,
    ingredients_admin,
    ingredients_data_admin,
    recipes_admin,
    users_data_admin,
    users_admin,
    vitamins_admin,
)
from api.routers.public import (
    diet_types_public,
    images_public,
    ingredients_public,
    oauth2_public,
    recipes_public,
    vitamins_public,
)
from api.routers.user_role import (
    follows_user,
    images_user,
    prefered_ingredients_user,
    prefered_recipe_type_user,
    recipe_favourite_user,
    recipes_user,
    refrigerator_user,
    token_data_user,
    users_data_user,
    users_user,
)
from logger import logger


startup_start = dt.now()
logger.info(f"Starting up the server... {startup_start}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for the FastAPI app."""
    startup_time = (dt.now() - startup_start).total_seconds() * 1000
    logger.info(f"Server started in {startup_time:.2f} ms")
    yield
    shutdown_start = dt.now()
    logger.info(f"Shutting down the server... {shutdown_start}")
    logger.info(f"Server uptime: {shutdown_start - startup_start}")


app = FastAPI(lifespan=None)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root_handler():
    return {"message": "Hello!"}


# admin routers
app.include_router(diet_types_admin.router)
app.include_router(ingredients_admin.router)
app.include_router(ingredients_data_admin.router)
app.include_router(recipes_admin.router)
app.include_router(users_data_admin.router)
app.include_router(users_admin.router)
app.include_router(vitamins_admin.router)

# public routers
app.include_router(diet_types_public.router)
app.include_router(images_public.router)
app.include_router(ingredients_public.router)
app.include_router(oauth2_public.router)
app.include_router(recipes_public.router)
app.include_router(vitamins_public.router)

# user routers
app.include_router(follows_user.router)
app.include_router(images_user.router)
app.include_router(prefered_ingredients_user.router)
app.include_router(prefered_recipe_type_user.router)
app.include_router(recipe_favourite_user.router)
app.include_router(recipes_user.router)
app.include_router(refrigerator_user.router)
app.include_router(token_data_user.router)
app.include_router(users_data_user.router)
app.include_router(users_user.router)


def handler(event, context):
    logger.debug(f"Event: {event}")

    asgi_handler = Mangum(app, lifespan="on", api_gateway_base_path="/dev")
    response = asgi_handler(event, context)

    return response


if __name__ == "__main__":
    import uvicorn

    logger.info("Local mode: Development server started")
    uvicorn.run("main:app", port=8000, reload=True)
