from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.get("/register", response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )


@router.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={}
    )


@router.get("/planner/{planner}", response_class=HTMLResponse)
def planner(request: Request, planner: str):
    if planner not in {"home", "party", "jewelry"}:
        return RedirectResponse("/")

    return templates.TemplateResponse(
        request=request,
        name=f"{planner}_planner.html",
        context={}
    )


@router.get("/history", response_class=HTMLResponse)
def history(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={}
    )