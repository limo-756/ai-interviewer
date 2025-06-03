from typing import Optional

from sqlalchemy.orm import Session
import interviewer.models as models
from interviewer.app.api.utils.hash_utils import stable_hash
from interviewer.app.api.schemas.user import User


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.UserModel).filter(models.UserModel.user_id == user_id).first()


def get_user_by_email(db: Session, user_email: str) -> Optional[User]:
    user_model = (db.query(models.UserModel)
                  .filter(models.UserModel.email.key == user_email)
                  .first())
    if user_model is not None:
        return user_model.to_user()
    return None


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserModel).offset(skip).limit(limit).all()


def create_user(db: Session, name: str, email: str, password: str):
    db_item = models.UserModel(name=name, email=email, password_hash=stable_hash(password))
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
