from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from src.routers import auth, cats, health

app = FastAPI()

app.include_router(cats.router)
app.include_router(auth.router)
app.include_router(health.router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # Set custom 404 message route not found.
    if exc.status_code == 404 and request.scope.get("endpoint") is None:
        return JSONResponse(
            status_code=404,
            content={
                "message": f"Oops! The requested endpoint '{request.url.path}' does not exist."
            },
        )
    # To raise all other exceptions.
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )
