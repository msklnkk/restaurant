from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import TableCreate, TableSchema, ClientSchema
from project.core.exceptions import TableNotFound, TableAlreadyExists
from project.api.depends import database, table_repo, check_for_admin_access, get_current_client


table_router = APIRouter()



@table_router.get("/all_tables", response_model=list[TableSchema], status_code=status.HTTP_200_OK)
async def get_all_tables() -> list[TableSchema]:
    async with database.session() as session:
        all_tables = await table_repo.get_all_tables(session=session)

    return all_tables


@table_router.get(
    "/table/{table_id}",
    response_model=TableSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_client)],
)
async def get_table_by_id(
    table_id: int,
) -> TableSchema:
    try:
        async with database.session() as session:
            table = await table_repo.get_table_by_id(session=session, table_id=table_id)
    except TableNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return table


@table_router.post("/add_table", response_model=TableSchema, status_code=status.HTTP_201_CREATED)
async def add_table(
    table_dto: TableCreate,
        current_client: ClientSchema = Depends(get_current_client),
) -> TableSchema:
    check_for_admin_access(client=current_client)
    try:
        async with database.session() as session:
            new_table = await table_repo.create_table(session=session, table=table_dto)
    except TableAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_table


@table_router.put(
    "/update_table/{table_id}",
    response_model=TableSchema,
    status_code=status.HTTP_200_OK,
)
async def update_table(
    table_id: int,
    table_dto: TableCreate,
) -> TableSchema:
    try:
        async with database.session() as session:
            updated_table = await table_repo.update_table(
                session=session,
                table_id=table_id,
                table=table_dto,
            )
    except TableNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_table


@table_router.delete("/delete_table/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(
    table_id: int,
        current_client: ClientSchema = Depends(get_current_client),
) -> None:
    check_for_admin_access(client=current_client)
    try:
        async with database.session() as session:
            table = await table_repo.delete_table(session=session, table_id=table_id)
    except TableNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return table