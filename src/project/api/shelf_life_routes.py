from fastapi import APIRouter, HTTPException, status
from datetime import date

from project.schemas.user import ShelfLifeCreate, ShelfLifeSchema
from project.core.exceptions import ShelfLifeNotFound, ShelfLifeAlreadyExists
from project.api.depends import database, shelfLife_repo

shelf_life_router = APIRouter()


@shelf_life_router.get("/all", response_model=list[ShelfLifeSchema], status_code=status.HTTP_200_OK)
async def get_all_shelf_lives() -> list[ShelfLifeSchema]:
    async with database.session() as session:
        all_shelf_lives = await shelfLife_repo.get_all_shelf_lives(session=session)

    return all_shelf_lives


@shelf_life_router.get("/shelf/{shelf_id}/delivery/{delivery_id}", response_model=ShelfLifeSchema, status_code=status.HTTP_200_OK)
async def get_shelf_life(
    shelf_id: int,
    delivery_id: int,
) -> ShelfLifeSchema:
    try:
        async with database.session() as session:
            shelf_life = await shelfLife_repo.get_shelf_life(
                session=session,
                shelf_id=shelf_id,
                delivery_id=delivery_id
            )
    except ShelfLifeNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return shelf_life


@shelf_life_router.get("/delivery/{delivery_id}", response_model=list[ShelfLifeSchema], status_code=status.HTTP_200_OK)
async def get_shelf_lives_by_delivery(
    delivery_id: int,
) -> list[ShelfLifeSchema]:
    async with database.session() as session:
        shelf_lives = await shelfLife_repo.get_shelf_lives_by_delivery(
            session=session,
            delivery_id=delivery_id
        )

    return shelf_lives


@shelf_life_router.post("/add", response_model=ShelfLifeSchema, status_code=status.HTTP_201_CREATED)
async def add_shelf_life(
    shelf_life_dto: ShelfLifeCreate,
) -> ShelfLifeSchema:
    try:
        async with database.session() as session:
            new_shelf_life = await shelfLife_repo.create_shelf_life(
                session=session,
                shelf_life=shelf_life_dto
            )
    except ShelfLifeAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_shelf_life


@shelf_life_router.put(
    "/update/shelf/{shelf_id}/delivery/{delivery_id}",
    response_model=ShelfLifeSchema,
    status_code=status.HTTP_200_OK,
)
async def update_shelf_life(
    shelf_id: int,
    delivery_id: int,
    shelf_life_dto: ShelfLifeCreate,
) -> ShelfLifeSchema:
    try:
        async with database.session() as session:
            updated_shelf_life = await shelfLife_repo.update_shelf_life(
                session=session,
                shelf_id=shelf_id,
                delivery_id=delivery_id,
                shelf_life=shelf_life_dto,
            )
    except ShelfLifeNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_shelf_life


@shelf_life_router.delete("/delete/shelf/{shelf_id}/delivery/{delivery_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shelf_life(
    shelf_id: int,
    delivery_id: int,
) -> None:
    try:
        async with database.session() as session:
            await shelfLife_repo.delete_shelf_life(
                session=session,
                shelf_id=shelf_id,
                delivery_id=delivery_id
            )
    except ShelfLifeNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)


@shelf_life_router.get("/expired", response_model=list[ShelfLifeSchema], status_code=status.HTTP_200_OK)
async def get_expired_shelf_lives(
        current_date: date | None = None
) -> list[ShelfLifeSchema]:
    async with database.session() as session:
        expired_items = await shelfLife_repo.get_expired_shelf_lives(
            session=session,
            current_date=current_date
        )

    return expired_items


@shelf_life_router.delete("/delivery/{delivery_id}/delete_all", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shelf_lives_by_delivery(
        delivery_id: int,
) -> None:
    async with database.session() as session:
        await shelfLife_repo.delete_shelf_lives_by_delivery(
            session=session,
            delivery_id=delivery_id
        )