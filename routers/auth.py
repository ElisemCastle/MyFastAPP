from typing import Annotated
from fastapi import FastAPI, Request, Form, APIRouter
from pathlib import Path
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Python excpects the files to be in the current working dir where you call the app
BASE_DIR = Path(__file__).resolve().parent.parent
USERS_FILE = BASE_DIR / "users.csv"

router = APIRouter()

@router.get("/")
async def root(request: Request):
    return RedirectResponse("/login")


@router.get("/portal")
def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="portal.html",
        context={"message": "Hello from FastAPI!"}
    )

users = {}

@router.get("/login")
def login(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"message": "Hello from FastAPI!"}
    )

@router.post("/login")
def login(request: Request, Username: Annotated[str, Form()], Password: Annotated[str, Form()]):
    with open(USERS_FILE, "r") as f:
        filedata = f.read().splitlines()

    for line in filedata:
        entries = line.split(", ")
        users.update({entries[0]: entries[1]})
    
    if Username not in users:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Username not found"
            },
            status_code=401
        )

    if Password not in users[Username]:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Incorrect Password"
            },
            status_code=401
        )
        
    return RedirectResponse("/portal", status_code=303)