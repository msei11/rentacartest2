from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    agency_name: str = Field(min_length=2, max_length=120)
    contact_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=6, max_length=40)
    password: str = Field(min_length=6, max_length=80)
    location: str = Field(default="", max_length=80)
    description: str = Field(default="", max_length=2000)


class UserMe(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: str
    full_name: str
    phone: str
    publisher_id: int | None = None


class PublisherPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    agency_name: str
    contact_name: str
    email: str
    phone: str
    description: str
    location: str
    logo_url: str
    verified: bool
    suspended: bool = False
    cars_count: int = 0


class PublisherUpdate(BaseModel):
    agency_name: str | None = Field(default=None, min_length=2, max_length=120)
    contact_name: str | None = Field(default=None, min_length=2, max_length=100)
    phone: str | None = None
    description: str | None = None
    location: str | None = None
    logo_url: str | None = None


class CarImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    is_primary: bool
    sort_order: int


class AvailabilityBlockOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_from: date
    date_to: date
    reason: str


class PublisherMini(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    agency_name: str
    verified: bool
    location: str
    logo_url: str


class CarCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    brand: str
    model: str
    year: int
    price_per_day: int
    fuel: str
    transmission: str
    body_type: str
    seats: int
    location: str
    views_count: int
    primary_image: str | None = None
    publisher: PublisherMini


class CarDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    brand: str
    model: str
    year: int
    price_per_day: int
    fuel: str
    transmission: str
    body_type: str
    seats: int
    doors: int
    mileage: int
    description: str
    features: list[str]
    location: str
    pickup_options: str
    deposit_info: str
    cancellation_policy: str
    min_driver_age: int
    views_count: int
    images: list[CarImageOut]
    availability_blocks: list[AvailabilityBlockOut]
    publisher: PublisherPublic


class CarCreate(BaseModel):
    brand: str = Field(min_length=1, max_length=50)
    model: str = Field(min_length=1, max_length=50)
    year: int = Field(ge=1990, le=2030)
    price_per_day: int = Field(gt=0)
    fuel: str
    transmission: str
    body_type: str
    seats: int = Field(ge=2, le=20)
    doors: int = Field(ge=2, le=6)
    mileage: int = Field(ge=0)
    description: str = ""
    features: str = ""
    location: str
    pickup_options: str = "Agencija"
    deposit_info: str = ""
    cancellation_policy: str = ""
    min_driver_age: int = Field(default=21, ge=18, le=30)
    image_urls: list[str] = Field(default_factory=list)


class CarUpdate(BaseModel):
    brand: str | None = None
    model: str | None = None
    year: int | None = None
    price_per_day: int | None = None
    fuel: str | None = None
    transmission: str | None = None
    body_type: str | None = None
    seats: int | None = None
    doors: int | None = None
    mileage: int | None = None
    description: str | None = None
    features: str | None = None
    location: str | None = None
    pickup_options: str | None = None
    deposit_info: str | None = None
    cancellation_policy: str | None = None
    min_driver_age: int | None = None
    is_active: bool | None = None


class InquiryCreate(BaseModel):
    car_id: int
    pickup_date: date
    return_date: date
    pickup_location: str = Field(min_length=2, max_length=120)
    full_name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=6, max_length=40)
    email: str = Field(default="", max_length=120)
    message: str = Field(default="", max_length=2000)


class InquiryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    car_id: int
    publisher_id: int
    pickup_date: date
    return_date: date
    pickup_location: str
    full_name: str
    phone: str
    email: str
    message: str
    status: str
    created_at: datetime
    car_title: str = ""
    car_image: str | None = None


class InquiryStatusUpdate(BaseModel):
    status: str


class AvailabilityCreate(BaseModel):
    date_from: date
    date_to: date
    reason: str = Field(default="", max_length=200)


class AvailabilityCheck(BaseModel):
    available: bool
    message: str


class HomePayload(BaseModel):
    popular_cars: list[CarCard]
    popular_locations: list[str]
    featured_publishers: list[PublisherPublic]


class PublisherStats(BaseModel):
    cars_count: int
    active_cars: int
    new_inquiries: int
    total_inquiries: int
    views_count: int


class AdminPublisherUpdate(BaseModel):
    verified: bool | None = None
    suspended: bool | None = None
