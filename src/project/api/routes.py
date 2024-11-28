from fastapi import APIRouter, HTTPException, status

from project.schemas.user import ClientCreate, ClientSchema, DrinkCreate, DrinkSchema, PriceCreate, PriceSchema
from project.schemas.healthcheck import HealthCheckSchema
from project.core.exceptions import UserNotFound, UserAlreadyExists, DrinkNotFound, DrinkAlreadyExists
from project.core.exceptions import PriceNotFound, PriceAlreadyExists
from project.api.depends import database, user_repo, drink_repo, price_repo


router = APIRouter()


@router.get("/healthcheck", response_model=HealthCheckSchema, status_code=status.HTTP_200_OK)
async def check_health() -> HealthCheckSchema:
    async with database.session() as session:
        db_is_ok = await user_repo.check_connection(session=session)

    return HealthCheckSchema(
        db_is_ok=db_is_ok,
    )

# Client
@router.get("/all_users", response_model=list[ClientSchema], status_code=status.HTTP_200_OK)
async def get_all_users() -> list[ClientSchema]:
    async with database.session() as session:
        all_users = await user_repo.get_all_users(session=session)

    return all_users


@router.get("/user/{user_id}", response_model=ClientSchema, status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: int,
) -> ClientSchema:
    try:
        async with database.session() as session:
            user = await user_repo.get_user_by_id(session=session, user_id=user_id)
    except UserNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return user


@router.post("/add_user", response_model=ClientSchema, status_code=status.HTTP_201_CREATED)
async def add_user(
    user_dto: ClientCreate,
) -> ClientSchema:
    try:
        async with database.session() as session:
            new_user = await user_repo.create_user(session=session, user=user_dto)
    except UserAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_user


@router.put(
    "/update_user/{user_id}",
    response_model=ClientSchema,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: int,
    user_dto: ClientCreate,
) -> ClientSchema:
    try:
        async with database.session() as session:
            updated_user = await user_repo.update_user(
                session=session,
                user_id=user_id,
                user=user_dto,
            )
    except UserNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_user


@router.delete("/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
) -> None:
    try:
        async with database.session() as session:
            user = await user_repo.delete_user(session=session, user_id=user_id)
    except UserNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return user


# Drink

@router.get("/all_drinks", response_model=list[DrinkSchema], status_code=status.HTTP_200_OK)
async def get_all_drinks() -> list[DrinkSchema]:
    async with database.session() as session:
        all_drinks = await drink_repo.get_all_drinks(session=session)
    return all_drinks


@router.get("/drink/{drink_id}", response_model=DrinkSchema, status_code=status.HTTP_200_OK)
async def get_drink_by_id(
    drink_id: int,
) -> DrinkSchema:
    try:
        async with database.session() as session:
            drink = await drink_repo.get_drink_by_id(session=session, drink_id=drink_id)
    except DrinkNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return drink


@router.post("/add_drink", response_model=DrinkSchema, status_code=status.HTTP_201_CREATED)
async def add_drink(
    drink_dto: DrinkCreate,
) -> DrinkSchema:
    try:
        async with database.session() as session:
            new_drink = await drink_repo.create_drink(session=session, drink=drink_dto)
            await session.commit()
    except DrinkAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)
    return new_drink


@router.put(
    "/update_drink/{drink_id}",
    response_model=DrinkSchema,
    status_code=status.HTTP_200_OK,
)
async def update_drink(
    drink_id: int,
    drink_dto: DrinkCreate,
) -> DrinkSchema:
    try:
        async with database.session() as session:
            updated_drink = await drink_repo.update_drink(
                session=session,
                drink_id=drink_id,
                drink=drink_dto,
            )
            await session.commit()
    except DrinkNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return updated_drink


@router.delete("/delete_drink/{drink_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_drink(
    drink_id: int,
) -> None:
    try:
        async with database.session() as session:
            await drink_repo.delete_drink(session=session, drink_id=drink_id)
            await session.commit()
    except DrinkNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)



# Price
@router.get("/all_prices", response_model=list[PriceSchema], status_code=status.HTTP_200_OK)
async def get_all_prices() -> list[PriceSchema]:
    async with database.session() as session:
        all_prices = await price_repo.get_all_prices(session=session)
    return all_prices


@router.get("/price/{dish_id}", response_model=PriceSchema, status_code=status.HTTP_200_OK)
async def get_price_by_dish_id(
    dish_id: int,
) -> PriceSchema:
    try:
        async with database.session() as session:
            price = await price_repo.get_price_by_dish_id(session=session, dish_id=dish_id)
    except PriceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
    return price


@router.post("/add_price/{dish_id}", response_model=PriceSchema, status_code=status.HTTP_201_CREATED)
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


@router.put(
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


@router.delete("/delete_price/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_price(
    dish_id: int,
) -> None:
    try:
        async with database.session() as session:
            await price_repo.delete_price(session=session, dish_id=dish_id)
            await session.commit()
    except PriceNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)