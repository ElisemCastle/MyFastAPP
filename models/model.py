from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Cat(SQLModel, table=True):
    cat_id: int | None = Field(primary_key=True)
    breed: str = Field(index=True)
    name: str | None = Field(index=True)
    favorite_toy: str
    age: int
    picture: str
