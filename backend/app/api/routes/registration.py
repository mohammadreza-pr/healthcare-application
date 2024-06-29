from fastapi import APIRouter, HTTPException
from app.api.deps import SessionDep
from app.models import UserRegister, UserPublic
from app import crud


router = APIRouter()


@router.post('/register', response_model=UserPublic)
async def register_new_user(
        session: SessionDep, body: UserRegister
):
    user = crud.get_user_by_phone(session=session, phone_number=body.phone_number)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user already exists"
        )
    user = crud.register_new_user(session=session, user_register=body)
    return user
