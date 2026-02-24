from fastapi import FastAPI
from fastapi import Request, Form
from typing import Annotated
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from starlette.middleware.sessions import SessionMiddleware
import json
import uvicorn
from pydantic import BaseModel, HttpUrl
from myfastapp.routers import cats, auth
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, Depends, HTTPException, status, Header
# from sqlalchemy import create_engine, select
# from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

# from fastapi_pagination import set_params, set_page
# from fastapi_pagination.cursor import CursorPage, CursorParams
# from fastapi_pagination.ext.sqlalchemy import paginatex

app = FastAPI()

app.include_router(cats.router)
app.include_router(auth.router)



@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # Check if the exception is specifically a 404 Not Found (or another 4xx/5xx if desired)
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"message": f"Oops! The requested endpoint '{request.url.path}' does not exist."},
        )
    # Re-raise or handle other HTTP exceptions if needed
    return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )


# # Database setup
# DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = sqlalchemy.orm.declarative_base()

