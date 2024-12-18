from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import OrderedDrinkCreate, OrderedDrinkSchema, ClientSchema
from project.core.exceptions import OrderedDrinkNotFound, OrderedDrinkAlreadyExists
from project.api.depends import database, orderedDrink_repo, get_current_client

ordered_drink_router = APIRouter()


@ordered_drink_router.get(
    "/ordered_drinks",
    response_model=list[OrderedDrinkSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_client)],
)
async def get_all_ordered_drinks() -> list[OrderedDrinkSchema]:
    async with database.session() as session:
        ordered_drinks = await orderedDrink_repo.get_all_ordered_drinks(session=session)

    return ordered_drinks


@ordered_drink_router.get(
    "/ordered_drink/order/{order_id}/drink/{drink_id}",
    response_model=OrderedDrinkSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_client)],
)
async def get_ordered_drink(
        order_id: int,
        drink_id: int,
) -> OrderedDrinkSchema:
    try:
        async with database.session() as session:
            ordered_drink = await orderedDrink_repo.get_ordered_drink(
                session=session,
                order_id=order_id,
                drink_id=drink_id
            )
    except OrderedDrinkNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return ordered_drink


@ordered_drink_router.get(
    "/ordered_drinks/order/{order_id}",
    response_model=list[OrderedDrinkSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_client)],
)
async def get_drinks_by_order(
        order_id: int,
) -> list[OrderedDrinkSchema]:
    async with database.session() as session:
        ordered_drinks = await orderedDrink_repo.get_drinks_by_order(
            session=session,
            order_id=order_id
        )

    return ordered_drinks


@ordered_drink_router.post("/ordered_drink", response_model=OrderedDrinkSchema, status_code=status.HTTP_201_CREATED)
async def create_ordered_drink(
        ordered_drink_dto: OrderedDrinkCreate,
) -> OrderedDrinkSchema:
    try:
        async with database.session() as session:
            new_ordered_drink = await orderedDrink_repo.create_ordered_drink(
                session=session,
                ordered_drink=ordered_drink_dto
            )
    except OrderedDrinkAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_ordered_drink


@ordered_drink_router.put(
    "/ordered_drink/order/{order_id}/drink/{drink_id}",
    response_model=OrderedDrinkSchema,
    status_code=status.HTTP_200_OK,
)
async def update_ordered_drink(
        order_id: int,
        drink_id: int,
        ordered_drink_dto: OrderedDrinkCreate,
) -> OrderedDrinkSchema:
    try:
        async with database.session() as session:
            updated_ordered_drink = await orderedDrink_repo.update_ordered_drink(
                session=session,
                order_id=order_id,
                drink_id=drink_id,
                ordered_drink=ordered_drink_dto
            )
    except OrderedDrinkNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_ordered_drink


@ordered_drink_router.delete("/ordered_drink/order/{order_id}/drink/{drink_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ordered_drink(
        order_id: int,
        drink_id: int,
) -> None:
    try:
        async with database.session() as session:
            await orderedDrink_repo.delete_ordered_drink(
                session=session,
                order_id=order_id,
                drink_id=drink_id
            )
    except OrderedDrinkNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)



@ordered_drink_router.put(
    "/ordered_drink/order/{order_id}/drink/{drink_id}/count",
    response_model=OrderedDrinkSchema,
    status_code=status.HTTP_200_OK,
)
async def update_drink_count(
    order_id: int,
    drink_id: int,
    count: int,
) -> OrderedDrinkSchema:
    try:
        async with database.session() as session:
            updated_ordered_drink = await orderedDrink_repo.update_drink_count(
                session=session,
                order_id=order_id,
                drink_id=drink_id,
                count=count
            )
    except OrderedDrinkNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_ordered_drink


@ordered_drink_router.delete("/ordered_drinks/order/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_drinks_from_order(
    order_id: int,
) -> None:
    async with database.session() as session:
        await orderedDrink_repo.delete_drinks_from_order(
            session=session,
            order_id=order_id
        )
