from fastapi import APIRouter, HTTPException, status

from project.schemas.user import PriceSchema, PriceCreate
from project.core.exceptions import PriceNotFound, PriceAlreadyExists
from project.api.depends import database, price_repo

price_router = APIRouter()



@price_router.get("/all_prices", response_model=list[PriceSchema], status_code=status.HTTP_200_OK)
async def get_all_prices() -> list[PriceSchema]:
    async with database.session() as session:
        all_prices = await price_repo.get_all_prices(session=session)
    return all_prices


@price_router.get("/price/{dish_id}", response_model=PriceSchema, status_code=status.HTTP_200_OK)
async def get_price_by_dish_id(
    dish_id: int,
) -> PriceSchema:
    try:
        async with database.session() as session:
            price = await price_repo.get_price_by_dish_id(session=session, dish_id=dish_id)
    except PriceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return price


@price_router.post("/add_price/{dish_id}", response_model=PriceSchema, status_code=status.HTTP_201_CREATED)
async def add_price(
    dish_id: int,
    price_dto: PriceCreate,
) -> PriceSchema:
    try:
        async with database.session() as session:
            new_price = await price_repo.create_price(
                session=session,
                price=price_dto,
                dish_id=dish_id
            )
            await session.commit()
    except PriceAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_price


@price_router.put(
    "/update_price/{dish_id}",
    response_model=PriceSchema,
    status_code=status.HTTP_200_OK,
)
async def update_price(
    dish_id: int,
    price_dto: PriceCreate,
) -> PriceSchema:
    try:
        async with database.session() as session:
            updated_price = await price_repo.update_price(
                session=session,
                dish_id=dish_id,
                price=price_dto,
            )
            await session.commit()
    except PriceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_price


@price_router.delete("/delete_price/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_price(
    dish_id: int,
) -> None:
    try:
        async with database.session() as session:
            await price_repo.delete_price(session=session, dish_id=dish_id)
            await session.commit()
    except PriceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

