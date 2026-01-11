from fastapi import APIRouter, Request
from utils.templates import templates

router = APIRouter(tags=["pages"])

@router.get("/")
def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/health")
def health():
    return {"status": "ok"}
