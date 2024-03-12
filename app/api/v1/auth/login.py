from fastapi import Depends, HTTPException, status
from core.config import settings
from sqlalchemy.orm import Session
from jose import jwt
from jose.exceptions import ExpiredSignatureError
from api.v1.models.admin_model import AdminModel
from .admin_auth import oauth2_bearer, get_user_exceptions
from db.session import get_db

SECRET_KEY = settings.JWT_PRIVATE_KEY
ALGORITHM = settings.JWT_ALGORITHM


async def get_current_admin(token: str = Depends(oauth2_bearer),
                            db: Session = Depends(get_db)):
    try:
        pyload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Update token")

    gmail: str = pyload.get("username")
    user_id: int = pyload.get("id")
    try:
        res = db.query(AdminModel).filter(AdminModel.gmail == gmail).first()

        is_super = res.is_superuser
        if res is None:
            raise get_user_exceptions()

        if gmail is None or user_id is None:
            raise get_user_exceptions()
    except AttributeError:
        raise get_user_exceptions()

    return {"sub": gmail, "user_id": user_id}


async def get_current_staff(token: str = Depends(oauth2_bearer),
                            db: Session = Depends(get_db)):
    try:
        pyload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Update token")

    gmail: str = pyload.get("username")
    user_id: int = pyload.get("id")

    res = db.query(AdminModel).filter(AdminModel.gmail == gmail).first()

    if res is None:
        raise get_user_exceptions()

    is_staff = res.is_staff

    if is_staff == False:
        raise get_user_exceptions()

    if gmail is None or user_id is None:
        raise get_user_exceptions()

    return {"sub": gmail, "user_id": user_id}


async def get_current_user(token: str = Depends(oauth2_bearer),
                           db: Session = Depends(get_db)):
    try:
        pyload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Update token")

    gmail: str = pyload.get("username")
    user_id: int = pyload.get("id")

    res = db.query(AdminModel).filter(AdminModel.gmail == gmail).first()

    if res is None:
        raise get_user_exceptions()

    if gmail is None or user_id is None:
        raise get_user_exceptions()

    return {"sub": gmail, "user_id": user_id}
