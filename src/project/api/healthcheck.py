from fastapi import APIRouter, status
from project.api.depends import database, client_repo, delivery_repo, dish_repo, dishProducts_repo
from project.api.depends import drink_repo, order_repo, orderedDish_repo, orderedDrink_repo
from project.api.depends import price_repo, product_repo, productInDelivery_repo, shelfLife_repo
from project.api.depends import staff_repo, supplier_repo, table_repo
from project.schemas.healthcheck import HealthCheckSchema
from project.core.exceptions import DatabaseError
healthcheck_router = APIRouter()

@healthcheck_router.get("/healthcheck", response_model=HealthCheckSchema, status_code=status.HTTP_200_OK)
async def check_health() -> HealthCheckSchema:
    try:
        async with database.session() as session:
            db_is_ok = await client_repo.check_connection(session=session)
            db_is_ok2 = await delivery_repo.check_connection(session=session)
            db_is_ok3 = await dish_repo.check_connection(session=session)
            db_is_ok4 = await dishProducts_repo.check_connection(session=session)
            db_is_ok5 = await drink_repo.check_connection(session=session)
            db_is_ok6 = await order_repo.check_connection(session=session)
            db_is_ok7 = await orderedDish_repo.check_connection(session=session)
            db_is_ok8 = await orderedDrink_repo.check_connection(session=session)
            db_is_ok9 = await price_repo.check_connection(session=session)
            db_is_ok10 = await product_repo.check_connection(session=session)
            db_is_ok11 = await productInDelivery_repo.check_connection(session=session)
            db_is_ok12 = await shelfLife_repo.check_connection(session=session)
            db_is_ok13 = await staff_repo.check_connection(session=session)
            db_is_ok14 = await supplier_repo.check_connection(session=session)
            db_is_ok15 = await table_repo.check_connection(session=session)

    except DatabaseError as error:
        db_is_ok = False
    return HealthCheckSchema(
        db_is_ok=db_is_ok,
    )