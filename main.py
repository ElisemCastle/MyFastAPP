from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from myfastapp.routers import auth, cats

app = FastAPI()

app.include_router(cats.router)
app.include_router(auth.router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # Check if the exception is specifically a 404 Not Found (or another 4xx/5xx if desired)
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={
                "message": f"Oops! The requested endpoint '{request.url.path}' does not exist."
            },
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
