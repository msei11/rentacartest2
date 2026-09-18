from __future__ import annotations

from datetime import UTC, date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="PUBLISHER")
    full_name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(40), default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    publisher: Mapped[Publisher | None] = relationship(back_populates="user")


class Publisher(Base):
    __tablename__ = "publishers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    agency_name: Mapped[str] = mapped_column(String(120))
    contact_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120))
    phone: Mapped[str] = mapped_column(String(40))
    description: Mapped[str] = mapped_column(Text, default="")
    location: Mapped[str] = mapped_column(String(80), default="")
    logo_url: Mapped[str] = mapped_column(String(500), default="")
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    suspended: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    user: Mapped[User] = relationship(back_populates="publisher")
    cars: Mapped[list[Car]] = relationship(back_populates="publisher", cascade="all, delete-orphan")
    inquiries: Mapped[list[Inquiry]] = relationship(back_populates="publisher")


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publishers.id"), index=True)
    brand: Mapped[str] = mapped_column(String(50), index=True)
    model: Mapped[str] = mapped_column(String(50))
    year: Mapped[int] = mapped_column(Integer)
    price_per_day: Mapped[int] = mapped_column(Integer)
    fuel: Mapped[str] = mapped_column(String(30))
    transmission: Mapped[str] = mapped_column(String(30))
    body_type: Mapped[str] = mapped_column(String(30))
    seats: Mapped[int] = mapped_column(Integer)
    doors: Mapped[int] = mapped_column(Integer, default=5)
    mileage: Mapped[int] = mapped_column(Integer, default=0)
    description: Mapped[str] = mapped_column(Text, default="")
    features: Mapped[str] = mapped_column(Text, default="")
    location: Mapped[str] = mapped_column(String(80), index=True)
    pickup_options: Mapped[str] = mapped_column(String(200), default="Agencija")
    deposit_info: Mapped[str] = mapped_column(String(200), default="")
    cancellation_policy: Mapped[str] = mapped_column(Text, default="")
    min_driver_age: Mapped[int] = mapped_column(Integer, default=21)
    views_count: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    publisher: Mapped[Publisher] = relationship(back_populates="cars")
    images: Mapped[list[CarImage]] = relationship(
        back_populates="car", cascade="all, delete-orphan", order_by="CarImage.sort_order"
    )
    availability_blocks: Mapped[list[AvailabilityBlock]] = relationship(
        back_populates="car", cascade="all, delete-orphan"
    )
    inquiries: Mapped[list[Inquiry]] = relationship(back_populates="car", cascade="all, delete-orphan")


class CarImage(Base):
    __tablename__ = "car_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), index=True)
    url: Mapped[str] = mapped_column(String(500))
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    car: Mapped[Car] = relationship(back_populates="images")


class AvailabilityBlock(Base):
    __tablename__ = "availability_blocks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), index=True)
    date_from: Mapped[date] = mapped_column(Date)
    date_to: Mapped[date] = mapped_column(Date)
    reason: Mapped[str] = mapped_column(String(200), default="")

    car: Mapped[Car] = relationship(back_populates="availability_blocks")


class Inquiry(Base):
    __tablename__ = "inquiries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), index=True)
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publishers.id"), index=True)
    pickup_date: Mapped[date] = mapped_column(Date)
    return_date: Mapped[date] = mapped_column(Date)
    pickup_location: Mapped[str] = mapped_column(String(120))
    full_name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(40))
    email: Mapped[str] = mapped_column(String(120), default="")
    message: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(20), default="PENDING", index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    car: Mapped[Car] = relationship(back_populates="inquiries")
    publisher: Mapped[Publisher] = relationship(back_populates="inquiries")
