# app/dashboard/dashboard.py

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    tags=["Dashboard"]
)

templates = Jinja2Templates(
    directory="app/dashboard/templates"
)


@router.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard_home():
    """
    Web dashboard entry point
    """

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": {}
        }
    )
