from fastapi import APIRouter, HTTPException, status
from datetime import date


from project.schemas.user import DeliveryCreate, DeliverySchema
from project.core.exceptions import DeliveryNotFound, DeliveryAlreadyExists
from project.api.depends import database, delivery_repo

delivery_router = APIRouter()


@delivery_router.get("/all_deliveries", response_model=list[DeliverySchema], status_code=status.HTTP_200_OK)
async def get_all_deliveries() -> list[DeliverySchema]:
    async with database.session() as session:
        all_deliveries = await delivery_repo.get_all_deliveries(session=session)

    return all_deliveries


@delivery_router.get("/delivery/{delivery_id}", response_model=DeliverySchema, status_code=status.HTTP_200_OK)
async def get_delivery_by_id(
    delivery_id: int,
) -> DeliverySchema:
    try:
        async with database.session() as session:
            delivery = await delivery_repo.get_delivery_by_id(
                session=session,
                delivery_id=delivery_id
            )
    except DeliveryNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return delivery


@delivery_router.get("/deliveries_by_date/{delivery_date}", response_model=list[DeliverySchema], status_code=status.HTTP_200_OK)
async def get_deliveries_by_date(
    delivery_date: date,
) -> list[DeliverySchema]:
    async with database.session() as session:
        deliveries = await delivery_repo.get_deliveries_by_date(
            session=session,
            delivery_date=delivery_date
        )

    return deliveries


@delivery_router.post("/add_delivery", response_model=DeliverySchema, status_code=status.HTTP_201_CREATED)
async def add_delivery(
    delivery_dto: DeliveryCreate,
) -> DeliverySchema:
    try:
        async with database.session() as session:
            new_delivery = await delivery_repo.create_delivery(
                session=session,
                delivery=delivery_dto
            )
    except DeliveryAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_delivery


@delivery_router.put(
    "/update_delivery/{delivery_id}",
    response_model=DeliverySchema,
    status_code=status.HTTP_200_OK,
)
async def update_delivery(
    delivery_id: int,
    delivery_dto: DeliveryCreate,
) -> DeliverySchema:
    try:
        async with database.session() as session:
            updated_delivery = await delivery_repo.update_delivery(
                session=session,
                delivery_id=delivery_id,
                delivery=delivery_dto,
            )
    except DeliveryNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_delivery


@delivery_router.delete("/delete_delivery/{delivery_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_delivery(
    delivery_id: int,
) -> None:
    try:
        async with database.session() as session:
            delivery = await delivery_repo.delete_delivery(
                session=session,
                delivery_id=delivery_id
            )
    except DeliveryNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return delivery
