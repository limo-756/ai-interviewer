from sqlalchemy.orm import Session
from . import models, schemas


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.UserModel).filter(models.UserModel.id == user_id).first()


def get_user_by_email(db: Session, user_email: str):
    return (db.query(models.UserModel)
            .filter(models.UserModel.email == user_email)
            .first())


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserModel).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.User):
    db_item = models.UserModel(name=user.name, email=user.email, password_hash=hash(user.password))
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
