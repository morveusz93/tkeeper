from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
import database

models.database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, offset=offset, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/spiders/", response_model=schemas.Spider)
def create_spider_for_user(
    user_id: int, spider: schemas.SpiderCreate, db: Session = Depends(get_db)
):
    return crud.create_user_spider(db=db, spider=spider, user_id=user_id)


@app.get("/spiders/", response_model=list[schemas.Spider])
def read_spiders(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    spiders = crud.get_spiders(db, offset=offset, limit=limit)
    return spiders
