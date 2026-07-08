from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from security import require_api_auth
from db import load_observations
from reporting import generate_pdf_report, generate_tex_report

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/pdf")
def pdf(_: dict = Depends(require_api_auth("report"))):
    path = generate_pdf_report(load_observations(), "IndoMarket Insight API Report", "api_report")
    return FileResponse(str(path), filename=path.name, media_type="application/pdf")

@router.get("/tex")
def tex(_: dict = Depends(require_api_auth("report"))):
    path = generate_tex_report(load_observations(), "IndoMarket Insight API Report", "api_report")
    return FileResponse(str(path), filename=path.name, media_type="text/x-tex")
