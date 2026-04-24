import shutil
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Edict, Project
from app.config import settings
from app.services.edital_extractor import extract_edict_from_pdf

router = APIRouter()


@router.post("/upload/{project_id}")
async def upload_edict(
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são aceitos")

    uploads_path = settings.get_uploads_path()
    safe_name = f"{project_id}_{file.filename}"
    file_path = uploads_path / safe_name

    with open(str(file_path), "wb") as f:
        content = await file.read()
        f.write(content)

    # Extrai texto e estrutura do edital
    try:
        extracted_json, raw_text, page_count, status = extract_edict_from_pdf(str(file_path))
    except Exception as e:
        extracted_json = {}
        raw_text = ""
        page_count = 0
        status = f"erro: {e}"

    edict = Edict(
        project_id=project_id,
        filename=file.filename,
        raw_text=raw_text,
        extracted_json=extracted_json,
        page_count=page_count,
        extraction_status=status,
    )
    db.add(edict)
    db.commit()
    db.refresh(edict)

    return {
        "id": edict.id,
        "filename": edict.filename,
        "page_count": edict.page_count,
        "extraction_status": edict.extraction_status,
        "extracted_json": edict.extracted_json,
        "preview": raw_text[:1000] if raw_text else "",
    }


@router.get("/{project_id}/latest")
def get_latest_edict(project_id: int, db: Session = Depends(get_db)):
    edict = db.query(Edict).filter(Edict.project_id == project_id).order_by(Edict.id.desc()).first()
    if not edict:
        raise HTTPException(status_code=404, detail="Nenhum edital encontrado para este projeto")
    return {
        "id": edict.id,
        "filename": edict.filename,
        "page_count": edict.page_count,
        "extraction_status": edict.extraction_status,
        "extracted_json": edict.extracted_json,
    }


@router.put("/{edict_id}/extracted")
def update_edict_extraction(edict_id: int, data: dict, db: Session = Depends(get_db)):
    """Permite correção manual do JSON extraído."""
    edict = db.query(Edict).filter(Edict.id == edict_id).first()
    if not edict:
        raise HTTPException(status_code=404, detail="Edital não encontrado")
    edict.extracted_json = data.get("extracted_json", edict.extracted_json)
    db.commit()
    return {"ok": True}
