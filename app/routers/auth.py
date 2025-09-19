from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import pyotp
import pandas as pd
from ..database import engine, db_session  
from ..models import Users                 
from ..security import verify_password
from ..deps import require_login, flash, pop_flashes

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def login_get(request: Request):
    flashes = pop_flashes(request)
    return templates.TemplateResponse("login.html", {"request": request, "flashes": flashes})

@router.get("/login_error", response_class=HTMLResponse)
def login_error_get(request: Request):
    return templates.TemplateResponse("login_error.html", {"request": request})

@router.post("/login")
def login_post(
    request: Request,
    login: str = Form(...),
    senha: str = Form(...),
    remember: str | None = Form(None),
):
    user = db_session.query(Users).filter_by(login=login).first()
    if not user or not verify_password(user.senha, senha):
        return RedirectResponse(url="/login_error", status_code=303)

    request.session["user_id"] = user.UID
    request.session["remember"] = True if remember else False

    usuario = login.split(".")[1] if "." in login else login
    request.session["cod_usuario"] = usuario

    return RedirectResponse(
        url=f"/login_2fa/{usuario}/{user.UID}/{login}",
        status_code=303
    )

@router.get("/login_2fa/{usuario}/{uid}/{login}", response_class=HTMLResponse)
def login_2fa_get(request: Request, usuario: str, uid: str, login: str):
    maybe_redirect = require_login(request)
    if maybe_redirect:
        return maybe_redirect

    flashes = pop_flashes(request)
    return templates.TemplateResponse(
        "login_2fa.html",
        {"request": request, "usuario": usuario, "uid": uid, "login": login, "flashes": flashes},
    )

@router.post("/login_2fa/{usuario}/{uid}/{login}")
def login_2fa_post(request: Request, usuario: str, uid: str, login: str, otp_token: str = Form(...)):
    df = pd.read_sql(f"SELECT totp_secret FROM usuarios_douglas WHERE login = '{login}'", con=engine)
    secret = df["totp_secret"].values[0]

    if pyotp.TOTP(secret).verify(otp_token):
        flash(request, "Token Válido", "success")
        
        return RedirectResponse(
            url=f"/tela_teste/menu_principal?usuario={usuario}&uid={uid}",
            status_code=303
        )
    else:
        flash(request, "Token inválido", "danger")
        return RedirectResponse(
            url=f"/login_2fa/{usuario}/{uid}/{login}",
            status_code=303
        )

@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)
