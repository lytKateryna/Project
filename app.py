from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
# from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from routes.films import router as films_router
from routes.meta import router as meta_router

app = FastAPI(title="Movie Finder API", version="0.1.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(films_router)
app.include_router(meta_router)


