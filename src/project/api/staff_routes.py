from fastapi import APIRouter, HTTPException, status, Depends

from project.schemas.user import StaffCreate, StaffSchema, ClientSchema
from project.core.exceptions import StaffNotFound, StaffAlreadyExists
from project.api.depends import database, staff_repo, check_for_admin_access, get_current_client

staff_router = APIRouter()



@staff_router.get(
    "/all_staff",
    response_model=list[StaffSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_client)],
)
async def get_all_staff() -> list[StaffSchema]:
    async with database.session() as session:
        all_staff = await staff_repo.get_all_staff(session=session)

    return all_staff


@staff_router.get(
    "/staff/{staff_id}",
    response_model=StaffSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_client)],
)
async def get_staff_by_id(
    staff_id: int,
) -> StaffSchema:
    try:
        async with database.session() as session:
            staff = await staff_repo.get_staff_by_id(session=session, staff_id=staff_id)
    except StaffNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return staff


@staff_router.post("/add_staff", response_model=StaffSchema, status_code=status.HTTP_201_CREATED)
async def add_staff(
    staff_dto: StaffCreate,
current_client: ClientSchema = Depends(get_current_client),
) -> StaffSchema:
    check_for_admin_access(client=current_client)
    try:
        async with database.session() as session:
            new_staff = await staff_repo.create_staff(session=session, staff=staff_dto)
    except StaffAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.message)

    return new_staff


@staff_router.put(
    "/update_staff/{staff_id}",
    response_model=StaffSchema,
    status_code=status.HTTP_200_OK,
)
async def update_staff(
    staff_id: int,
    staff_dto: StaffCreate,
current_client: ClientSchema = Depends(get_current_client),
) -> StaffSchema:
    check_for_admin_access(client=current_client)
    try:
        async with database.session() as session:
            updated_staff = await staff_repo.update_staff(
                session=session,
                staff_id=staff_id,
                staff=staff_dto,
            )
    except StaffNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return updated_staff


@staff_router.delete("/delete_staff/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_staff(
    staff_id: int,
current_client: ClientSchema = Depends(get_current_client),
) -> None:
    check_for_admin_access(client=current_client)
    try:
        async with database.session() as session:
            staff = await staff_repo.delete_staff(session=session, staff_id=staff_id)
    except StaffNotFound as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error.message)

    return staff
