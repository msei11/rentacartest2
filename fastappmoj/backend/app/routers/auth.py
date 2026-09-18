from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import create_token, get_current_user, hash_password, verify_password
from app.database import get_db
from app.models import Publisher, User
from app.schemas import LoginRequest, RegisterRequest, TokenResponse, UserMe

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == payload.email.lower()).first()
    if exists:
        raise HTTPException(status_code=409, detail="Email je već registrovan")
    user = User(
        email=payload.email.lower(),
        hashed_password=hash_password(payload.password),
        role="PUBLISHER",
        full_name=payload.contact_name,
        phone=payload.phone,
    )
    db.add(user)
    db.flush()
    publisher = Publisher(
        user_id=user.id,
        agency_name=payload.agency_name,
        contact_name=payload.contact_name,
        email=payload.email.lower(),
        phone=payload.phone,
        description=payload.description,
        location=payload.location,
        verified=False,
        suspended=False,
    )
    db.add(publisher)
    db.commit()
    return TokenResponse(access_token=create_token(user), role=user.role)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Pogrešan email ili lozinka")
    if user.role == "PUBLISHER":
        publisher = db.query(Publisher).filter(Publisher.user_id == user.id).first()
        if publisher and publisher.suspended:
            raise HTTPException(status_code=403, detail="Nalog je suspendovan")
    return TokenResponse(access_token=create_token(user), role=user.role)


@router.post("/logout")
def logout():
    return {"ok": True}


@router.get("/me", response_model=UserMe)
def me(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    publisher = db.query(Publisher).filter(Publisher.user_id == user.id).first()
    return UserMe(
        id=user.id,
        email=user.email,
        role=user.role,
        full_name=user.full_name,
        phone=user.phone,
        publisher_id=publisher.id if publisher else None,
    )
