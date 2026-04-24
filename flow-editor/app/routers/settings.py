from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import AppSettings
from app.config import settings
from app.schemas import SettingsUpdate

router = APIRouter()


@router.get("/")
def get_settings(db: Session = Depends(get_db)):
    db_settings = db.query(AppSettings).all()
    result = {s.key: s.value for s in db_settings}
    result["ai_model"] = settings.ai_model
    result["ai_provider"] = settings.ai_provider
    result["api_key_configured"] = settings.has_api_key()
    return result


@router.put("/")
def update_setting(data: SettingsUpdate, db: Session = Depends(get_db)):
    existing = db.query(AppSettings).filter(AppSettings.key == data.key).first()
    if existing:
        existing.value = data.value
    else:
        s = AppSettings(key=data.key, value=data.value)
        db.add(s)
    db.commit()

    # Atualiza settings em memória para chave de API
    if data.key == "anthropic_api_key":
        import os
        os.environ["ANTHROPIC_API_KEY"] = data.value
        settings.anthropic_api_key = data.value
        from app.services.ai_provider import ai_provider
        ai_provider.api_key = data.value

    return {"ok": True}
