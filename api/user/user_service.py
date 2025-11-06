from sqlmodel import Session, select
from uuid import uuid4

from api.user.user_model import User, UserCreate
from core.security import hash_password, verify_password, get_token
from fastapi.security import OAuth2PasswordRequestForm

def register(session: Session, user: UserCreate):
    db_user = User(
        id=str(uuid4()),
        user_name=user.user_name,
        password=hash_password(user.password)
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

def login(session: Session, form_data: OAuth2PasswordRequestForm):
    statement = select(User).where(User.user_name == form_data.username)
    db_user = session.exec(statement=statement).first()

    if not db_user or not verify_password(form_data.password, db_user.password):
        return None
    
    token = get_token(form_data.username)

    return token
