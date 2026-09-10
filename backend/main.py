import hashlib
import json
import secrets
from datetime import datetime, timezone
from typing import Generator

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import ScanRecord, User
from scanner import run_security_scan

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Aegis AI Auditor API",
    version="1.0.0",
    description="Deterministic security governance scans for LLM workflows and agentic pipelines.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class ScanRequest(BaseModel):
    target_text: str = Field(min_length=1, max_length=100_000)
    user_id: int | None = Field(default=None, ge=1)


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def db_session() -> Generator[Session, None, None]:
    yield from get_db()


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "aegis-ai-auditor"}


@app.post("/api/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(db_session)) -> dict[str, object]:
    normalized_email = payload.email.lower().strip()
    if db.query(User).filter(User.email == normalized_email).first():
        raise HTTPException(status_code=409, detail="An account with this email already exists.")

    user = User(email=normalized_email, hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "user": {"id": user.id, "email": user.email},
        "message": "Account created successfully.",
    }


@app.post("/api/login")
def login(payload: LoginRequest, db: Session = Depends(db_session)) -> dict[str, object]:
    normalized_email = payload.email.lower().strip()
    user = db.query(User).filter(User.email == normalized_email).first()
    if not user or user.hashed_password != hash_password(payload.password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    return {
        "access_token": secrets.token_urlsafe(32),
        "token_type": "bearer",
        "user": {"id": user.id, "email": user.email},
        "issued_at": datetime.now(timezone.utc).isoformat(),
        "note": "This development build returns an ephemeral session stub. Replace with signed JWT authentication before public deployment.",
    }


@app.post("/api/scan")
def scan(payload: ScanRequest, db: Session = Depends(db_session)) -> dict[str, object]:
    if payload.user_id is not None and not db.get(User, payload.user_id):
        raise HTTPException(status_code=404, detail="User not found.")

    try:
        report = run_security_scan(payload.target_text)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    record = ScanRecord(
        user_id=payload.user_id,
        target_url=payload.target_text,
        risk_score=report["risk_score"],
        findings_json=json.dumps(report),
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "scan_id": record.id,
        "created_at": record.created_at.isoformat(),
        **report,
    }
