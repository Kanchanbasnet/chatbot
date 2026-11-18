from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Users


def get_current_user(
    db: Session = Depends(get_db), x_user_email: str = Header(None), x_user_name: str = Header(None)
):
    if not x_user_email:
        raise HTTPException(status_code=401, detail="Not Logged in.")

    user = db.query(Users).filter(Users.email == x_user_email).first()
    if not user:
        user = Users(email=x_user_email, name=x_user_name)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
