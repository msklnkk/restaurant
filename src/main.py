import asyncio
import logging
import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from project.core.config import settings
from project.api.healthcheck import healthcheck_router
from project.api.auth_routes import auth_router

from project.api.client_routes import client_router
from project.api.delivery_routes import delivery_router
from project.api.dish_products_routes import dish_products_router
from project.api.dish_routes import dish_router
from project.api.drink_routes import drink_router
from project.api.order_routes import order_router
from project.api.ordered_dish_routes import ordered_dish_router
from project.api.ordered_drink_routes import ordered_drink_router
from project.api.price_routes import price_router
from project.api.product_in_delivery_routes import product_in_delivery_router
from project.api.product_routes import product_router
from project.api.shelf_life_routes import shelf_life_router
from project.api.staff_routes import staff_router
from project.api.supplier_routes import supplier_router
from project.api.table_routes import table_router

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app_options = {}
    if settings.ENV.lower() == "prod":
        app_options = {
            "docs_url": None,
            "redoc_url": None,
        }
    if settings.LOG_LEVEL in ["DEBUG", "INFO"]:
        app_options["debug"] = True

    app = FastAPI(root_path=settings.ROOT_PATH, **app_options)
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    app.include_router(client_router, tags=["Client"])
    app.include_router(delivery_router, tags=["Delivery"])
    app.include_router(dish_products_router, tags=["Dish Product"])
    app.include_router(dish_router, tags=["Dish"])
    app.include_router(drink_router, tags=["Drink"])
    app.include_router(order_router, tags=["Order"])
    app.include_router(ordered_dish_router, tags=["Ordered Dish"])
    app.include_router(ordered_drink_router, tags=["Ordered Drink"])
    app.include_router(price_router, tags=["Price"])
    app.include_router(product_in_delivery_router, tags=["Product In Delivery"])
    app.include_router(product_router, tags=["Product"])
    app.include_router(shelf_life_router, tags=["Shelf Life"])
    app.include_router(staff_router, tags=["Staff"])
    app.include_router(supplier_router, tags=["Supplier"])
    app.include_router(table_router, tags=["Table"])
    app.include_router(auth_router, tags=["Auth"])
    app.include_router(healthcheck_router, tags=["Health check"])

    return app


app = create_app()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def run() -> None:
    config = uvicorn.Config("main:app", host="0.0.0.0", port=8000, reload=False)
    server = uvicorn.Server(config=config)
    tasks = (
        asyncio.create_task(server.serve()),
    )

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == "__main__":
    logger.debug(f"{settings.postgres_url}=")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())