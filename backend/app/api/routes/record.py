from fastapi import APIRouter, HTTPException
from app.api.deps import SessionDep, CurrentUser
from app.models import PublicRecord, CreateRecord, Record, Records
from app import crud

router = APIRouter()


@router.get("/", response_model=Records)
async def get_user_records(
        session: SessionDep,
        skip: int,
        current_user: CurrentUser,
        limit: int = 100
):
    items = crud.get_user_records(session=session, skip=skip, limit=limit, current_user=current_user)
    return items


@router.post("/", response_model=PublicRecord)
async def add_new_record(
        session: SessionDep,
        body: CreateRecord
):
    record = Record.model_validate(body)
    session.add(record)
    session.commit()
    session.refresh(record)
    return record
