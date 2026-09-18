from datetime import date

from sqlalchemy.orm import Session

from app.models import AvailabilityBlock, Car, CarImage, Publisher


def parse_features(raw: str) -> list[str]:
    if not raw:
        return []
    return [part.strip() for part in raw.replace(";", ",").split(",") if part.strip()]


def primary_image(car: Car) -> str | None:
    if not car.images:
        return None
    for image in car.images:
        if image.is_primary:
            return image.url
    return car.images[0].url


def periods_overlap(a_from: date, a_to: date, b_from: date, b_to: date) -> bool:
    return a_from <= b_to and a_to >= b_from


def is_available(db: Session, car_id: int, start: date, end: date) -> bool:
    blocks = db.query(AvailabilityBlock).filter(AvailabilityBlock.car_id == car_id).all()
    return not any(periods_overlap(start, end, block.date_from, block.date_to) for block in blocks)


def publisher_public(publisher: Publisher, cars_count: int | None = None) -> dict:
    if cars_count is None:
        cars_count = sum(1 for car in publisher.cars if car.is_active)
    return {
        "id": publisher.id,
        "agency_name": publisher.agency_name,
        "contact_name": publisher.contact_name,
        "email": publisher.email,
        "phone": publisher.phone,
        "description": publisher.description,
        "location": publisher.location,
        "logo_url": publisher.logo_url,
        "verified": publisher.verified,
        "suspended": publisher.suspended,
        "cars_count": cars_count,
    }


def car_card(car: Car) -> dict:
    return {
        "id": car.id,
        "brand": car.brand,
        "model": car.model,
        "year": car.year,
        "price_per_day": car.price_per_day,
        "fuel": car.fuel,
        "transmission": car.transmission,
        "body_type": car.body_type,
        "seats": car.seats,
        "location": car.location,
        "views_count": car.views_count,
        "primary_image": primary_image(car),
        "publisher": {
            "id": car.publisher.id,
            "agency_name": car.publisher.agency_name,
            "verified": car.publisher.verified,
            "location": car.publisher.location,
            "logo_url": car.publisher.logo_url,
        },
    }


def car_detail(car: Car) -> dict:
    return {
        "id": car.id,
        "brand": car.brand,
        "model": car.model,
        "year": car.year,
        "price_per_day": car.price_per_day,
        "fuel": car.fuel,
        "transmission": car.transmission,
        "body_type": car.body_type,
        "seats": car.seats,
        "doors": car.doors,
        "mileage": car.mileage,
        "description": car.description,
        "features": parse_features(car.features),
        "location": car.location,
        "pickup_options": car.pickup_options,
        "deposit_info": car.deposit_info,
        "cancellation_policy": car.cancellation_policy,
        "min_driver_age": car.min_driver_age,
        "views_count": car.views_count,
        "images": car.images,
        "availability_blocks": car.availability_blocks,
        "publisher": publisher_public(car.publisher),
    }


def inquiry_out(inquiry) -> dict:
    return {
        "id": inquiry.id,
        "car_id": inquiry.car_id,
        "publisher_id": inquiry.publisher_id,
        "pickup_date": inquiry.pickup_date,
        "return_date": inquiry.return_date,
        "pickup_location": inquiry.pickup_location,
        "full_name": inquiry.full_name,
        "phone": inquiry.phone,
        "email": inquiry.email,
        "message": inquiry.message,
        "status": inquiry.status,
        "created_at": inquiry.created_at,
        "car_title": f"{inquiry.car.brand} {inquiry.car.model}" if inquiry.car else "",
        "car_image": primary_image(inquiry.car) if inquiry.car else None,
    }


def attach_images(db: Session, car: Car, urls: list[str]) -> None:
    for index, url in enumerate(urls):
        db.add(
            CarImage(
                car_id=car.id,
                url=url,
                is_primary=index == 0 and not car.images,
                sort_order=index,
            )
        )
