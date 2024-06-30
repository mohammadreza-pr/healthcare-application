from fastapi import APIRouter
from app.api.deps import SessionDep, CurrentUser
from app.models import PublicRecord, CreateRecord, Record, Records, RecordType
from app import crud

router = APIRouter()


@router.get("/", response_model=Records)
async def get_user_records(
        session: SessionDep,
        skip: int,
        rtype: RecordType,
        current_user: CurrentUser,
        limit: int = 100
):
    items = crud.get_user_records(session=session, skip=skip, limit=limit, current_user=current_user, record_type=rtype)
    return items


@router.post("/", response_model=PublicRecord)
async def add_new_record(
        session: SessionDep,
        rtype: RecordType,
        body: CreateRecord
):
    record = Record.model_validate(body, update={"record_type": rtype})
    session.add(record)
    session.commit()
    session.refresh(record)
    return record
