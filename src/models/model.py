from sqlmodel import Field, SQLModel


class Cat(SQLModel, table=True):
    cat_id: int | None = Field(primary_key=True)
    breed: str = Field(index=True)
    name: str | None = Field(index=True)
    favorite_toy: str
    age: int
    picture: str

# # Database setup
# DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = sqlalchemy.orm.declarative_base()