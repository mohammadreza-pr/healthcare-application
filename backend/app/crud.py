from typing import Any

from sqlmodel import Session, select, func, desc, or_

from app.core.security import get_password_hash, verify_password
from app.models import Item, ItemCreate, User, UserCreate, UserUpdate, UserRegister, Record, Records, RecordType


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def register_new_user(*, session: Session, user_register: UserRegister):
    db_user = User.model_validate(user_register, update={"hashed_password": get_password_hash(user_register.password)})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def get_user_by_phone(*, session: Session, phone_number: str) -> User | None:
    db_user = session.exec(select(User).where(User.phone_number == phone_number)).first()
    return db_user


def get_user_by_national_id(*, session: Session, national_id: str) -> User | None:
    db_user = session.exec(select(User).where(User.national_id == national_id)).first()
    return db_user


def authenticate(*, session: Session, phone_number: str, password: str) -> User | None:
    db_user = get_user_by_phone(session=session, phone_number=phone_number)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: int) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def get_user_records(*, session: Session, skip: int, limit: int, current_user: User, record_type: RecordType):
    device_id = current_user.device_id
    count_statement = (
        select(func.count())
        .select_from(Record)
        .where(Record.device_id == device_id, Record.record_type == record_type)
    )
    count = session.exec(count_statement).one()
    statement = (
        select(Record)
        .where(Record.device_id == device_id, Record.record_type == record_type)
        .order_by(desc(Record.created_at))
        .offset(skip)
        .limit(limit)
    )
    records = session.exec(statement).all()
    return Records(data=records, count=count)
