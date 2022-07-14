from fastapi import FastAPI, Depends, Query, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from pydantic import BaseModel

from random import randrange

from app.config import settings


app = FastAPI()


engine = create_engine(
    settings.DATABRICKS_DATABASE_URI,
    connect_args={
        "http_path": settings.HTTP_PATH,
    },
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def session():
    db = Session()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base(bind=engine)

# Entity User
class Users(Base):
    __tablename__ = "users"
    # __table_args__ = {"autoload": True}
    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    email = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)


# Request Body
class UsersRequest(BaseModel):
    first_name: str = Query(..., max_length=50)
    last_name: str = Query(..., max_length=50)


@app.get("/")
def root():
    return {"message": "Hello Lakehouse"}


@app.get("/user")
def get_user(
    id: int = None,
    first_name: str = Query(None, max_length=50),
    db: Session = Depends(session),
):
    if id is not None:
        result_set = db.query(Users).filter(Users.id == id).all()
    elif first_name is not None:
        result_set = db.query(Users).filter(Users.first_name == first_name).all()
    else:
        result_set = db.query(Users).all()
    response_body = jsonable_encoder(result_set)
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)


@app.post("/user")
def create_user(request: UsersRequest, db: Session = Depends(session)):
    user = Users(
        id=randrange(1_000_000, 10_000_000),
        first_name=request.first_name,
        last_name=request.last_name,
    )
    db.add(user)
    db.commit()
    response_body = jsonable_encoder({"user_id": user.id})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)


@app.put("/user/{id}")
def update_user(id: int, request: UsersRequest, db: Session = Depends(session)):
    user = db.query(Users).filter(Users.id == id).first()
    if user is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)
    user.first_name = request.first_name
    user.last_name = request.last_name
    db.commit()
    response_body = jsonable_encoder({"user_id": user.id})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)


@app.delete("/user/{id}")
def delete_user(id: int, db: Session = Depends(session)):
    db.query(Users).filter(Users.id == id).delete()
    db.commit()
    response_body = jsonable_encoder({"user_id": id, "msg": "record deleted"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_body)
