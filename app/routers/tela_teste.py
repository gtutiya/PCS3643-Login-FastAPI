from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..deps import require_login, pop_flashes

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/tela_teste/menu_principal", response_class=HTMLResponse)
def menu_principal(
    request: Request,
    usuario: str | None = Query(None),
    uid: str | None = Query(None),
):
    maybe_redirect = require_login(request)
    if maybe_redirect:
        return maybe_redirect

    flashes = pop_flashes(request)

    if not usuario:
        usuario = request.session.get("cod_usuario") or "usuário"
    if not uid:
        uid = str(request.session.get("user_id") or "")

    ctx = {"request": request, "usuario": usuario, "uid": uid, "flashes": flashes}
    return templates.TemplateResponse("tela_teste.html", ctx)
