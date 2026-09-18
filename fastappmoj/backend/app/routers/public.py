from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models import Car, Inquiry, Publisher
from app.schemas import (
    AvailabilityCheck,
    CarCard,
    CarDetail,
    HomePayload,
    InquiryCreate,
    InquiryOut,
    PublisherPublic,
)
from app.services import car_card, car_detail, inquiry_out, is_available, publisher_public

router = APIRouter(prefix="/api", tags=["public"])


def visible_cars_query(db: Session):
    return (
        db.query(Car)
        .join(Publisher)
        .options(selectinload(Car.images), selectinload(Car.publisher), selectinload(Car.availability_blocks))
        .filter(Car.is_active.is_(True), Publisher.suspended.is_(False))
    )


@router.get("/home", response_model=HomePayload)
def home(db: Session = Depends(get_db)):
    cars = (
        visible_cars_query(db)
        .order_by(Car.views_count.desc(), Car.created_at.desc())
        .limit(6)
        .all()
    )
    locations = [
        row[0]
        for row in db.query(Car.location)
        .join(Publisher)
        .filter(Car.is_active.is_(True), Publisher.suspended.is_(False))
        .distinct()
        .all()
    ]
    publishers = (
        db.query(Publisher)
        .options(selectinload(Publisher.cars))
        .filter(Publisher.suspended.is_(False), Publisher.verified.is_(True))
        .limit(6)
        .all()
    )
    return {
        "popular_cars": [car_card(car) for car in cars],
        "popular_locations": locations,
        "featured_publishers": [publisher_public(p) for p in publishers],
    }


@router.get("/cars", response_model=list[CarCard])
def list_cars(
    location: str | None = None,
    pickup_date: date | None = None,
    return_date: date | None = None,
    brand: str | None = None,
    model: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    fuel: str | None = None,
    transmission: str | None = None,
    body_type: str | None = None,
    seats: int | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    q: str | None = None,
    sort: str = Query(default="newest"),
    db: Session = Depends(get_db),
):
    query = visible_cars_query(db)
    if location:
        query = query.filter(Car.location.ilike(f"%{location}%"))
    if brand:
        query = query.filter(Car.brand.ilike(f"%{brand}%"))
    if model:
        query = query.filter(Car.model.ilike(f"%{model}%"))
    if min_price is not None:
        query = query.filter(Car.price_per_day >= min_price)
    if max_price is not None:
        query = query.filter(Car.price_per_day <= max_price)
    if fuel:
        query = query.filter(Car.fuel.ilike(fuel))
    if transmission:
        query = query.filter(Car.transmission.ilike(transmission))
    if body_type:
        query = query.filter(Car.body_type.ilike(body_type))
    if seats is not None:
        query = query.filter(Car.seats >= seats)
    if year_from is not None:
        query = query.filter(Car.year >= year_from)
    if year_to is not None:
        query = query.filter(Car.year <= year_to)
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(Car.brand.ilike(like), Car.model.ilike(like), Car.location.ilike(like))
        )

    cars = query.all()
    if pickup_date and return_date:
        if return_date < pickup_date:
            raise HTTPException(status_code=400, detail="Datum vraćanja mora biti posle preuzimanja")
        cars = [car for car in cars if is_available(db, car.id, pickup_date, return_date)]

    if sort == "price_asc":
        cars.sort(key=lambda c: c.price_per_day)
    elif sort == "price_desc":
        cars.sort(key=lambda c: c.price_per_day, reverse=True)
    elif sort == "popularity":
        cars.sort(key=lambda c: c.views_count, reverse=True)
    else:
        cars.sort(key=lambda c: c.created_at, reverse=True)
    return [car_card(car) for car in cars]


@router.get("/cars/{car_id}", response_model=CarDetail)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = (
        visible_cars_query(db)
        .filter(Car.id == car_id)
        .first()
    )
    if not car:
        raise HTTPException(status_code=404, detail="Vozilo nije pronađeno")
    car.views_count += 1
    db.commit()
    db.refresh(car)
    return car_detail(car)


@router.get("/cars/{car_id}/availability", response_model=AvailabilityCheck)
def check_availability(
    car_id: int,
    pickup_date: date,
    return_date: date,
    db: Session = Depends(get_db),
):
    car = visible_cars_query(db).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Vozilo nije pronađeno")
    if return_date < pickup_date:
        raise HTTPException(status_code=400, detail="Neispravan period")
    available = is_available(db, car_id, pickup_date, return_date)
    return {
        "available": available,
        "message": "Vozilo je potencijalno dostupno za izabrani period."
        if available
        else "Izabrani period je označen kao zauzet ili blokiran od strane izdavača.",
    }


@router.get("/publishers/{publisher_id}", response_model=PublisherPublic)
def get_publisher_public(publisher_id: int, db: Session = Depends(get_db)):
    publisher = db.query(Publisher).options(selectinload(Publisher.cars)).filter(Publisher.id == publisher_id).first()
    if not publisher or publisher.suspended:
        raise HTTPException(status_code=404, detail="Izdavač nije pronađen")
    return publisher_public(publisher)


@router.get("/publishers/{publisher_id}/cars", response_model=list[CarCard])
def publisher_cars(publisher_id: int, db: Session = Depends(get_db)):
    publisher = db.get(Publisher, publisher_id)
    if not publisher or publisher.suspended:
        raise HTTPException(status_code=404, detail="Izdavač nije pronađen")
    cars = visible_cars_query(db).filter(Car.publisher_id == publisher_id).all()
    return [car_card(car) for car in cars]


@router.post("/inquiries", response_model=InquiryOut, status_code=201)
def create_inquiry(payload: InquiryCreate, db: Session = Depends(get_db)):
    car = visible_cars_query(db).filter(Car.id == payload.car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Vozilo nije pronađeno")
    if payload.return_date < payload.pickup_date:
        raise HTTPException(status_code=400, detail="Neispravan period")
    if not is_available(db, car.id, payload.pickup_date, payload.return_date):
        raise HTTPException(
            status_code=409,
            detail="Vozilo nije dostupno za izabrani period. Izaberite druge datume.",
        )
    inquiry = Inquiry(
        car_id=car.id,
        publisher_id=car.publisher_id,
        pickup_date=payload.pickup_date,
        return_date=payload.return_date,
        pickup_location=payload.pickup_location,
        full_name=payload.full_name,
        phone=payload.phone,
        email=payload.email or "",
        message=payload.message or "",
        status="PENDING",
    )
    db.add(inquiry)
    db.commit()
    db.refresh(inquiry)
    inquiry = (
        db.query(Inquiry)
        .options(selectinload(Inquiry.car).selectinload(Car.images))
        .filter(Inquiry.id == inquiry.id)
        .first()
    )
    return inquiry_out(inquiry)
