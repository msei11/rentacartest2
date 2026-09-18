from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload

from app.auth import get_admin
from app.database import get_db
from app.models import Car, Inquiry, Publisher, User
from app.schemas import AdminPublisherUpdate, CarCard, InquiryOut, PublisherPublic
from app.services import car_card, inquiry_out, publisher_public

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/publishers", response_model=list[PublisherPublic])
def list_publishers(_: User = Depends(get_admin), db: Session = Depends(get_db)):
    items = db.query(Publisher).options(selectinload(Publisher.cars)).all()
    return [publisher_public(item) | {"verified": item.verified} for item in items]


@router.patch("/publishers/{publisher_id}", response_model=PublisherPublic)
def update_publisher(
    publisher_id: int,
    payload: AdminPublisherUpdate,
    _: User = Depends(get_admin),
    db: Session = Depends(get_db),
):
    publisher = db.query(Publisher).options(selectinload(Publisher.cars)).filter(Publisher.id == publisher_id).first()
    if not publisher:
        raise HTTPException(status_code=404, detail="Izdavač nije pronađen")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(publisher, key, value)
    db.commit()
    db.refresh(publisher)
    result = publisher_public(publisher)
    result["verified"] = publisher.verified
    return result


@router.get("/cars", response_model=list[CarCard])
def list_cars(_: User = Depends(get_admin), db: Session = Depends(get_db)):
    cars = db.query(Car).options(selectinload(Car.images), selectinload(Car.publisher)).all()
    return [car_card(car) for car in cars]


@router.delete("/cars/{car_id}", status_code=204)
def remove_car(car_id: int, _: User = Depends(get_admin), db: Session = Depends(get_db)):
    car = db.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Vozilo nije pronađeno")
    db.delete(car)
    db.commit()


@router.get("/inquiries", response_model=list[InquiryOut])
def list_inquiries(_: User = Depends(get_admin), db: Session = Depends(get_db)):
    items = (
        db.query(Inquiry)
        .options(selectinload(Inquiry.car).selectinload(Car.images))
        .order_by(Inquiry.created_at.desc())
        .all()
    )
    return [inquiry_out(item) for item in items]
