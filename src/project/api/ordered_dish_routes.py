from fastapi import APIRouter, HTTPException, status

from project.schemas.user import OrderedDishCreate, OrderedDishSchema
from project.core.exceptions import OrderedDishNotFound, OrderedDishAlreadyExists
from project.api.depends import database, orderedDish_repo

ordered_dish_router = APIRouter()


@ordered_dish_router.get("/all", response_model=list[OrderedDishSchema], status_code=status.HTTP_200_OK)
async def get_all_ordered_dishes() -> list[OrderedDishSchema]:
    async with database.session() as session:
        all_ordered_dishes = await orderedDish_repo.get_all_ordered_dishes(session=session)

    return all_ordered_dishes


@ordered_dish_router.get("/order/{order_id}/dish/{dish_id}", response_model=OrderedDishSchema, status_code=status.HTTP_200_OK)
async def get_ordered_dish(
    order_id: int,
    dish_id: int,
) -> OrderedDishSchema:
    try:
        async with database.session() as session:
            ordered_dish = await orderedDish_repo.get_ordered_dish(
                session=session,
                order_id=order_id,
                dish_id=dish_id
            )
    except OrderedDishNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return ordered_dish


@ordered_dish_router.get("/order/{order_id}", response_model=list[OrderedDishSchema], status_code=status.HTTP_200_OK)
async def get_dishes_by_order(
    order_id: int,
) -> list[OrderedDishSchema]:
    async with database.session() as session:
        ordered_dishes = await orderedDish_repo.get_dishes_by_order(
            session=session,
            order_id=order_id
        )

    return ordered_dishes


@ordered_dish_router.post("/add", response_model=OrderedDishSchema, status_code=status.HTTP_201_CREATED)
async def add_ordered_dish(
    ordered_dish_dto: OrderedDishCreate,
) -> OrderedDishSchema:
    try:
        async with database.session() as session:
            new_ordered_dish = await orderedDish_repo.create_ordered_dish(
                session=session,
                ordered_dish=ordered_dish_dto
            )
    except OrderedDishAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_ordered_dish


@ordered_dish_router.put(
    "/update/order/{order_id}/dish/{dish_id}",
    response_model=OrderedDishSchema,
    status_code=status.HTTP_200_OK,
)
async def update_ordered_dish(
    order_id: int,
    dish_id: int,
    ordered_dish_dto: OrderedDishCreate,
) -> OrderedDishSchema:
    try:
        async with database.session() as session:
            updated_ordered_dish = await orderedDish_repo.update_ordered_dish(
                session=session,
                order_id=order_id,
                dish_id=dish_id,
                ordered_dish=ordered_dish_dto,
            )
    except OrderedDishNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_ordered_dish


@ordered_dish_router.delete("/delete/order/{order_id}/dish/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ordered_dish(
    order_id: int,
    dish_id: int,
) -> None:
    try:
        async with database.session() as session:
            await orderedDish_repo.delete_ordered_dish(
                session=session,
                order_id=order_id,
                dish_id=dish_id
            )
    except OrderedDishNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)


@ordered_dish_router.put(
    "/update_count/order/{order_id}/dish/{dish_id}",
    response_model=OrderedDishSchema,
    status_code=status.HTTP_200_OK,
)
async def update_dish_count(
    order_id: int,
    dish_id: int,
    count: int,
) -> OrderedDishSchema:
    try:
        async with database.session() as session:
            updated_ordered_dish = await orderedDish_repo.update_dish_count(
                session=session,
                order_id=order_id,
                dish_id=dish_id,
                count=count
            )
    except OrderedDishNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_ordered_dish


@ordered_dish_router.delete("/order/{order_id}/delete_all", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dishes_from_order(
    order_id: int,
) -> None:
    async with database.session() as session:
        await orderedDish_repo.delete_dishes_from_order(
            session=session,
            order_id=order_id
        )