from fastapi import APIRouter, HTTPException, status, Depends
from datetime import date

from project.schemas.user import OrderCreate, OrderSchema, ClientSchema
from project.core.exceptions import OrderNotFound, OrderAlreadyExists
from project.api.depends import database, order_repo, check_for_admin_access, get_current_client

order_router = APIRouter()


@order_router.get(
    "/all_orders",
    response_model=list[OrderSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_client)],
)
async def get_all_orders() -> list[OrderSchema]:
    async with database.session() as session:
        all_orders = await order_repo.get_all_orders(session=session)

    return all_orders


@order_router.get(
    "/order/{order_id}",
    response_model=OrderSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_client)],
)
async def get_order_by_id(
    order_id: int,
) -> OrderSchema:
    try:
        async with database.session() as session:
            order = await order_repo.get_order_by_id(session=session, order_id=order_id)
    except OrderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return order


@order_router.get(
    "/orders/date/{order_date}",
    response_model=list[OrderSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_client)],
)
async def get_orders_by_date(
    order_date: date,
) -> list[OrderSchema]:
    async with database.session() as session:
        orders = await order_repo.get_orders_by_date(session=session, order_date=order_date)

    return orders


@order_router.get(
    "/orders/status/{status}",
    response_model=list[OrderSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_client)],
)
async def get_orders_by_status(
    status: str,
) -> list[OrderSchema]:
    async with database.session() as session:
        orders = await order_repo.get_orders_by_status(session=session, status=status)

    return orders


@order_router.get(
    "/orders/client/{client_id}",
    response_model=list[OrderSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_client)],
)
async def get_orders_by_client(
    client_id: int,
) -> list[OrderSchema]:
    async with database.session() as session:
        orders = await order_repo.get_orders_by_client(session=session, client_id=client_id)

    return orders


@order_router.get(
    "/orders/staff/{staff_id}",
    response_model=list[OrderSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_client)],
)
async def get_orders_by_staff(
    staff_id: int,
) -> list[OrderSchema]:
    async with database.session() as session:
        orders = await order_repo.get_orders_by_staff(session=session, staff_id=staff_id)

    return orders


@order_router.post("/add_order", response_model=OrderSchema, status_code=status.HTTP_201_CREATED)
async def add_order(
    order_dto: OrderCreate,
current_client: ClientSchema = Depends(get_current_client),
) -> OrderSchema:
    check_for_admin_access(client=current_client)
    try:
        async with database.session() as session:
            new_order = await order_repo.create_order(session=session, order=order_dto)
    except OrderAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_order


@order_router.put(
    "/update_order/{order_id}",
    response_model=OrderSchema,
    status_code=status.HTTP_200_OK,
)
async def update_order(
    order_id: int,
    order_dto: OrderCreate,
current_client: ClientSchema = Depends(get_current_client),
) -> OrderSchema:
    check_for_admin_access(client=current_client)
    try:
        async with database.session() as session:
            updated_order = await order_repo.update_order(
                session=session,
                order_id=order_id,
                order=order_dto,
            )
    except OrderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_order


@order_router.patch(
    "/order/{order_id}/status",
    response_model=OrderSchema,
    status_code=status.HTTP_200_OK,
)
async def update_order_status(
    order_id: int,
    status: str,
current_client: ClientSchema = Depends(get_current_client),
) -> OrderSchema:
    check_for_admin_access(client=current_client)
    try:
        async with database.session() as session:
            updated_order = await order_repo.update_order_status(
                session=session,
                order_id=order_id,
                status=status,
            )
    except OrderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_order


@order_router.delete("/delete_order/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: int,
current_client: ClientSchema = Depends(get_current_client),
) -> None:
    check_for_admin_access(client=current_client)
    try:
        async with database.session() as session:
            await order_repo.delete_order(session=session, order_id=order_id)
    except OrderNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)
