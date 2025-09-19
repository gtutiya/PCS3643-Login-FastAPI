from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from .routers import auth,tela_teste

app = FastAPI(title="Auth App (FastAPI)")


app.add_middleware(SessionMiddleware, secret_key="senha")

app.include_router(auth.router)
app.include_router(tela_teste.router)

