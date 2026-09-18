from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session, selectinload

from app.config import UPLOAD_DIR
from app.auth import get_publisher
from app.database import get_db
from app.models import AvailabilityBlock, Car, CarImage, Inquiry, Publisher
from app.schemas import (
    AvailabilityBlockOut,
    AvailabilityCreate,
    CarCard,
    CarCreate,
    CarDetail,
    CarImageOut,
    InquiryOut,
    InquiryStatusUpdate,
    PublisherPublic,
    PublisherStats,
    PublisherUpdate,
    CarUpdate,
)
from app.services import attach_images, car_card, car_detail, inquiry_out, publisher_public

router = APIRouter(prefix="/api/publisher", tags=["publisher"])


def owned_car(db: Session, publisher: Publisher, car_id: int) -> Car:
    car = (
        db.query(Car)
        .options(
            selectinload(Car.images),
            selectinload(Car.availability_blocks),
            selectinload(Car.publisher),
        )
        .filter(Car.id == car_id, Car.publisher_id == publisher.id)
        .first()
    )
    if not car:
        raise HTTPException(status_code=404, detail="Vozilo nije pronađeno")
    return car


@router.get("/me", response_model=PublisherPublic)
def my_profile(publisher: Publisher = Depends(get_publisher), db: Session = Depends(get_db)):
    publisher = db.query(Publisher).options(selectinload(Publisher.cars)).filter(Publisher.id == publisher.id).first()
    return publisher_public(publisher)


@router.patch("/me", response_model=PublisherPublic)
def update_profile(
    payload: PublisherUpdate,
    publisher: Publisher = Depends(get_publisher),
    db: Session = Depends(get_db),
):
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(publisher, key, value)
    db.commit()
    db.refresh(publisher)
    return publisher_public(publisher)


@router.get("/stats", response_model=PublisherStats)
def stats(publisher: Publisher = Depends(get_publisher), db: Session = Depends(get_db)):
    cars = db.query(Car).filter(Car.publisher_id == publisher.id).all()
    inquiries = db.query(Inquiry).filter(Inquiry.publisher_id == publisher.id).all()
    return PublisherStats(
        cars_count=len(cars),
        active_cars=sum(1 for car in cars if car.is_active),
        new_inquiries=sum(1 for item in inquiries if item.status == "PENDING"),
        total_inquiries=len(inquiries),
        views_count=sum(car.views_count for car in cars),
    )


@router.get("/cars", response_model=list[CarCard])
def my_cars(publisher: Publisher = Depends(get_publisher), db: Session = Depends(get_db)):
    cars = (
        db.query(Car)
        .options(selectinload(Car.images), selectinload(Car.publisher))
        .filter(Car.publisher_id == publisher.id)
        .all()
    )
    return [car_card(car) for car in cars]


@router.post("/cars", response_model=CarDetail, status_code=201)
def create_car(
    payload: CarCreate,
    publisher: Publisher = Depends(get_publisher),
    db: Session = Depends(get_db),
):
    data = payload.model_dump(exclude={"image_urls"})
    car = Car(publisher_id=publisher.id, **data)
    db.add(car)
    db.flush()
    attach_images(db, car, payload.image_urls)
    db.commit()
    return car_detail(owned_car(db, publisher, car.id))


@router.get("/cars/{car_id}", response_model=CarDetail)
def get_my_car(car_id: int, publisher: Publisher = Depends(get_publisher), db: Session = Depends(get_db)):
    return car_detail(owned_car(db, publisher, car_id))


@router.patch("/cars/{car_id}", response_model=CarDetail)
def update_car(
    car_id: int,
    payload: CarUpdate,
    publisher: Publisher = Depends(get_publisher),
    db: Session = Depends(get_db),
):
    car = owned_car(db, publisher, car_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(car, key, value)
    db.commit()
    return car_detail(owned_car(db, publisher, car_id))


@router.delete("/cars/{car_id}", status_code=204)
def delete_car(car_id: int, publisher: Publisher = Depends(get_publisher), db: Session = Depends(get_db)):
    car = owned_car(db, publisher, car_id)
    db.delete(car)
    db.commit()


@router.post("/cars/{car_id}/images", response_model=CarImageOut)
async def upload_image(
    car_id: int,
    file: UploadFile = File(...),
    publisher: Publisher = Depends(get_publisher),
    db: Session = Depends(get_db),
):
    car = owned_car(db, publisher, car_id)
    suffix = Path(file.filename or "image.jpg").suffix.lower() or ".jpg"
    if suffix not in {".jpg", ".jpeg", ".png", ".webp"}:
        raise HTTPException(status_code=400, detail="Dozvoljeni formati: jpg, png, webp")
    filename = f"car_{car.id}_{len(car.images) + 1}{suffix}"
    dest = UPLOAD_DIR / "cars" / filename
    dest.write_bytes(await file.read())
    image = CarImage(
        car_id=car.id,
        url=f"/uploads/cars/{filename}",
        is_primary=len(car.images) == 0,
        sort_order=len(car.images),
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


@router.delete("/cars/{car_id}/images/{image_id}", status_code=204)
def delete_image(
    car_id: int,
    image_id: int,
    publisher: Publisher = Depends(get_publisher),
    db: Session = Depends(get_db),
):
    owned_car(db, publisher, car_id)
    image = db.query(CarImage).filter(CarImage.id == image_id, CarImage.car_id == car_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Slika nije pronađena")
    db.delete(image)
    db.commit()


@router.get("/cars/{car_id}/availability", response_model=list[AvailabilityBlockOut])
def list_blocks(car_id: int, publisher: Publisher = Depends(get_publisher), db: Session = Depends(get_db)):
    car = owned_car(db, publisher, car_id)
    return car.availability_blocks


@router.post("/cars/{car_id}/availability", response_model=AvailabilityBlockOut, status_code=201)
def add_block(
    car_id: int,
    payload: AvailabilityCreate,
    publisher: Publisher = Depends(get_publisher),
    db: Session = Depends(get_db),
):
    owned_car(db, publisher, car_id)
    if payload.date_to < payload.date_from:
        raise HTTPException(status_code=400, detail="Neispravan period")
    block = AvailabilityBlock(
        car_id=car_id,
        date_from=payload.date_from,
        date_to=payload.date_to,
        reason=payload.reason,
    )
    db.add(block)
    db.commit()
    db.refresh(block)
    return block


@router.delete("/cars/{car_id}/availability/{block_id}", status_code=204)
def delete_block(
    car_id: int,
    block_id: int,
    publisher: Publisher = Depends(get_publisher),
    db: Session = Depends(get_db),
):
    owned_car(db, publisher, car_id)
    block = (
        db.query(AvailabilityBlock)
        .filter(AvailabilityBlock.id == block_id, AvailabilityBlock.car_id == car_id)
        .first()
    )
    if not block:
        raise HTTPException(status_code=404, detail="Blokada nije pronađena")
    db.delete(block)
    db.commit()


@router.get("/inquiries", response_model=list[InquiryOut])
def list_inquiries(publisher: Publisher = Depends(get_publisher), db: Session = Depends(get_db)):
    items = (
        db.query(Inquiry)
        .options(selectinload(Inquiry.car).selectinload(Car.images))
        .filter(Inquiry.publisher_id == publisher.id)
        .order_by(Inquiry.created_at.desc())
        .all()
    )
    return [inquiry_out(item) for item in items]


@router.get("/inquiries/{inquiry_id}", response_model=InquiryOut)
def get_inquiry(
    inquiry_id: int,
    publisher: Publisher = Depends(get_publisher),
    db: Session = Depends(get_db),
):
    item = (
        db.query(Inquiry)
        .options(selectinload(Inquiry.car).selectinload(Car.images))
        .filter(Inquiry.id == inquiry_id, Inquiry.publisher_id == publisher.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Upit nije pronađen")
    return inquiry_out(item)


@router.patch("/inquiries/{inquiry_id}", response_model=InquiryOut)
def update_inquiry(
    inquiry_id: int,
    payload: InquiryStatusUpdate,
    publisher: Publisher = Depends(get_publisher),
    db: Session = Depends(get_db),
):
    if payload.status not in {"PENDING", "ANSWERED", "CLOSED"}:
        raise HTTPException(status_code=400, detail="Nedozvoljen status")
    item = (
        db.query(Inquiry)
        .options(selectinload(Inquiry.car).selectinload(Car.images))
        .filter(Inquiry.id == inquiry_id, Inquiry.publisher_id == publisher.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Upit nije pronađen")
    item.status = payload.status
    db.commit()
    db.refresh(item)
    return inquiry_out(item)
