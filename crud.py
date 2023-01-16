from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).one()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).one()


def get_users(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.User).offset(offset).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_spiders(db: Session, offset: int = 0, limit: int = 100):
    return db.query(models.Spider).offset(offset).limit(limit).all()


def create_user_spider(db: Session, spider: schemas.SpiderCreate, user_id: int):
    db_spider = models.Spider(**spider.dict(), owner_id=user_id)
    db.add(db_spider)
    db.commit()
    db.refresh(db_spider)
    return db_spider
