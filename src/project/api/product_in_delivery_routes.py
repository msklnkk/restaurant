from fastapi import APIRouter, HTTPException, status
from decimal import Decimal

from project.schemas.user import ProductInDeliveryCreate, ProductInDeliverySchema
from project.core.exceptions import ProductInDeliveryNotFound, ProductInDeliveryAlreadyExists
from project.api.depends import database, productInDelivery_repo

product_in_delivery_router = APIRouter()


@product_in_delivery_router.get("/all", response_model=list[ProductInDeliverySchema], status_code=status.HTTP_200_OK)
async def get_all_products_in_deliveries() -> list[ProductInDeliverySchema]:
    async with database.session() as session:
        all_products = await productInDelivery_repo.get_all_products_in_deliveries(session=session)

    return all_products


@product_in_delivery_router.get("/product/{product_id}/delivery/{delivery_id}", response_model=ProductInDeliverySchema, status_code=status.HTTP_200_OK)
async def get_product_in_delivery(
    product_id: int,
    delivery_id: int,
) -> ProductInDeliverySchema:
    try:
        async with database.session() as session:
            product = await productInDelivery_repo.get_product_in_delivery(
                session=session,
                product_id=product_id,
                delivery_id=delivery_id
            )
    except ProductInDeliveryNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return product


@product_in_delivery_router.get("/delivery/{delivery_id}", response_model=list[ProductInDeliverySchema], status_code=status.HTTP_200_OK)
async def get_products_by_delivery(
    delivery_id: int,
) -> list[ProductInDeliverySchema]:
    async with database.session() as session:
        products = await productInDelivery_repo.get_products_by_delivery(
            session=session,
            delivery_id=delivery_id
        )

    return products


@product_in_delivery_router.post("/add", response_model=ProductInDeliverySchema, status_code=status.HTTP_201_CREATED)
async def add_product_in_delivery(
    product_dto: ProductInDeliveryCreate,
) -> ProductInDeliverySchema:
    try:
        async with database.session() as session:
            new_product = await productInDelivery_repo.create_product_in_delivery(
                session=session,
                product=product_dto
            )
    except ProductInDeliveryAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_product


@product_in_delivery_router.put(
    "/update/product/{product_id}/delivery/{delivery_id}",
    response_model=ProductInDeliverySchema,
    status_code=status.HTTP_200_OK,
)
async def update_product_in_delivery(
    product_id: int,
    delivery_id: int,
    product_dto: ProductInDeliveryCreate,
) -> ProductInDeliverySchema:
    try:
        async with database.session() as session:
            updated_product = await productInDelivery_repo.update_product_in_delivery(
                session=session,
                product_id=product_id,
                delivery_id=delivery_id,
                product=product_dto,
            )
    except ProductInDeliveryNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_product


@product_in_delivery_router.delete("/delete/product/{product_id}/delivery/{delivery_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_in_delivery(
    product_id: int,
    delivery_id: int,
) -> None:
    try:
        async with database.session() as session:
            await productInDelivery_repo.delete_product_in_delivery(
                session=session,
                product_id=product_id,
                delivery_id=delivery_id
            )
    except ProductInDeliveryNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)


@product_in_delivery_router.get("/delivery/{delivery_id}/total_cost", response_model=Decimal, status_code=status.HTTP_200_OK)
async def get_total_cost_by_delivery(
        delivery_id: int,
) -> Decimal:
    async with database.session() as session:
        total_cost = await productInDelivery_repo.get_total_cost_by_delivery(
            session=session,
            delivery_id=delivery_id
        )

    return total_cost


@product_in_delivery_router.delete("/delivery/{delivery_id}/delete_all", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_products_in_delivery(
        delivery_id: int,
) -> None:
    async with database.session() as session:
        await productInDelivery_repo.delete_all_products_in_delivery(
            session=session,
            delivery_id=delivery_id
        )
