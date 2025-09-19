from fastapi import Request, HTTPException
from starlette.responses import RedirectResponse

def require_login(request: Request):
    if not request.session.get("user_id"):
        return RedirectResponse(url="/", status_code=303)
    return None

def flash(request: Request, message: str, category: str = "info"):
    request.session.setdefault("_flashes", [])
    request.session["_flashes"].append({"message": message, "category": category})

def pop_flashes(request: Request):
    flashes = request.session.pop("_flashes", [])
    return flashes
