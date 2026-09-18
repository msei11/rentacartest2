from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.auth import hash_password
from app.database import Base, SessionLocal, engine
from app.models import AvailabilityBlock, Car, CarImage, Inquiry, Publisher, User

IMAGES = {
    "bmw": [
        "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=1200&q=80",
        "https://images.unsplash.com/photo-1617531657520-57e6d0f4a4e1?w=1200&q=80",
    ],
    "mercedes": [
        "https://images.unsplash.com/photo-1618843479313-40f8aa3dd68d?w=1200&q=80",
        "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=1200&q=80",
    ],
    "audi": [
        "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=1200&q=80",
        "https://images.unsplash.com/photo-1542282088-fe8426682b8f?w=1200&q=80",
    ],
    "vw": [
        "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?w=1200&q=80",
        "https://images.unsplash.com/photo-1502877338535-766e1452684a?w=1200&q=80",
    ],
    "toyota": [
        "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=1200&q=80",
        "https://images.unsplash.com/photo-1619767886558-efdc259cde1a?w=1200&q=80",
    ],
    "skoda": [
        "https://images.unsplash.com/photo-1609521263047-f8e859b75576?w=1200&q=80",
        "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=1200&q=80",
    ],
    "renault": [
        "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=1200&q=80",
        "https://images.unsplash.com/photo-1489824904134-891ab64532f1?w=1200&q=80",
    ],
}


def add_car(db: Session, publisher_id: int, data: dict, key: str) -> Car:
    images = data.pop("images_key")
    car = Car(publisher_id=publisher_id, **data)
    db.add(car)
    db.flush()
    for index, url in enumerate(IMAGES[images]):
        db.add(CarImage(car_id=car.id, url=url, is_primary=index == 0, sort_order=index))
    return car


def seed() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    admin = User(
        email="admin@rentlist.rs",
        hashed_password=hash_password("admin123"),
        role="ADMIN",
        full_name="Admin RentList",
        phone="+381111111",
    )
    db.add(admin)

    publishers_data = [
        {
            "email": "drive@beograd.rs",
            "password": "demo123",
            "agency": "BeoDrive Rent",
            "contact": "Nikola Petrović",
            "phone": "+381 64 111 2200",
            "location": "Beograd",
            "desc": "Porodična agencija sa flotom novijih vozila u Beogradu. Preuzimanje na aerodromu i u centru.",
            "verified": True,
        },
        {
            "email": "info@adriacar.rs",
            "password": "demo123",
            "agency": "AdriaCar Novi Sad",
            "contact": "Ana Jovanović",
            "phone": "+381 63 222 3344",
            "location": "Novi Sad",
            "desc": "Izdavanje automobila u Novom Sadu i okolini. Fokus na ekonomična i porodična vozila.",
            "verified": True,
        },
        {
            "email": "hello@coastline.rs",
            "password": "demo123",
            "agency": "Coastline Mobility",
            "contact": "Luka Milić",
            "phone": "+381 69 555 7788",
            "location": "Niš",
            "desc": "Premium i standard vozila za poslovna putovanja i vikend izlete.",
            "verified": False,
        },
    ]

    pubs: list[Publisher] = []
    for item in publishers_data:
        user = User(
            email=item["email"],
            hashed_password=hash_password(item["password"]),
            role="PUBLISHER",
            full_name=item["contact"],
            phone=item["phone"],
        )
        db.add(user)
        db.flush()
        pub = Publisher(
            user_id=user.id,
            agency_name=item["agency"],
            contact_name=item["contact"],
            email=item["email"],
            phone=item["phone"],
            description=item["desc"],
            location=item["location"],
            logo_url="",
            verified=item["verified"],
        )
        db.add(pub)
        db.flush()
        pubs.append(pub)

    today = date.today()
    cars_spec = [
        (pubs[0].id, {
            "brand": "BMW", "model": "320d", "year": 2022, "price_per_day": 85, "fuel": "Dizel",
            "transmission": "Automatski", "body_type": "Limuzina", "seats": 5, "doors": 4, "mileage": 42000,
            "description": "Udoban poslovni BMW, idealan za duža putovanja.",
            "features": "Navigacija, klima, parking senzori, Bluetooth, tempomat",
            "location": "Beograd", "pickup_options": "Agencija, Aerodrom Nikola Tesla",
            "deposit_info": "Depozit se dogovara direktno sa izdavačem",
            "cancellation_policy": "Besplatno otkazivanje do 48h pre preuzimanja, po dogovoru sa izdavačem.",
            "min_driver_age": 23, "views_count": 128, "images_key": "bmw",
        }),
        (pubs[0].id, {
            "brand": "Mercedes", "model": "C 220", "year": 2021, "price_per_day": 95, "fuel": "Dizel",
            "transmission": "Automatski", "body_type": "Limuzina", "seats": 5, "doors": 4, "mileage": 51000,
            "description": "Premium C klasa sa kompletnom opremom.",
            "features": "Koža, kamera, LED farovi, Apple CarPlay",
            "location": "Beograd", "pickup_options": "Agencija, dostava u hotel",
            "deposit_info": "Dogovor sa izdavačem", "cancellation_policy": "Fleksibilna politika uz najavu.",
            "min_driver_age": 25, "views_count": 201, "images_key": "mercedes",
        }),
        (pubs[0].id, {
            "brand": "Volkswagen", "model": "Golf 8", "year": 2023, "price_per_day": 48, "fuel": "Benzin",
            "transmission": "Manuelni", "body_type": "Hatchback", "seats": 5, "doors": 5, "mileage": 18000,
            "description": "Štedljiv i okretan Golf za grad i vicend.",
            "features": "Klima, USB, start-stop, zadnja kamera",
            "location": "Beograd", "pickup_options": "Agencija",
            "deposit_info": "Dogovor", "cancellation_policy": "Otkazivanje 24h unapred.",
            "min_driver_age": 21, "views_count": 96, "images_key": "vw",
        }),
        (pubs[0].id, {
            "brand": "Toyota", "model": "RAV4", "year": 2022, "price_per_day": 72, "fuel": "Hibrid",
            "transmission": "Automatski", "body_type": "SUV", "seats": 5, "doors": 5, "mileage": 33000,
            "description": "Porodični SUV, pogodan i za planinu.",
            "features": "4x4, krovni nosači, navigacija, kružni tempomat",
            "location": "Beograd", "pickup_options": "Agencija, aerodrom",
            "deposit_info": "Dogovor", "cancellation_policy": "Standardna politika izdavača.",
            "min_driver_age": 23, "views_count": 154, "images_key": "toyota",
        }),
        (pubs[1].id, {
            "brand": "Škoda", "model": "Octavia", "year": 2021, "price_per_day": 42, "fuel": "Dizel",
            "transmission": "Manuelni", "body_type": "Karavan", "seats": 5, "doors": 5, "mileage": 61000,
            "description": "Prostran karavan za porodicu i prtljag.",
            "features": "Ogromna gepek, klima, Bluetooth",
            "location": "Novi Sad", "pickup_options": "Agencija, autobuska stanica",
            "deposit_info": "Dogovor", "cancellation_policy": "Otkazivanje do 24h.",
            "min_driver_age": 21, "views_count": 77, "images_key": "skoda",
        }),
        (pubs[1].id, {
            "brand": "Renault", "model": "Clio", "year": 2020, "price_per_day": 28, "fuel": "Benzin",
            "transmission": "Manuelni", "body_type": "Hatchback", "seats": 5, "doors": 5, "mileage": 74000,
            "description": "Ekonomičan gradski automobil.",
            "features": "Klima, Bluetooth",
            "location": "Novi Sad", "pickup_options": "Agencija",
            "deposit_info": "Dogovor", "cancellation_policy": "Fleksibilno.",
            "min_driver_age": 21, "views_count": 63, "images_key": "renault",
        }),
        (pubs[1].id, {
            "brand": "Audi", "model": "A4", "year": 2020, "price_per_day": 70, "fuel": "Dizel",
            "transmission": "Automatski", "body_type": "Limuzina", "seats": 5, "doors": 4, "mileage": 69000,
            "description": "Elegantna A4 za poslovne obilaske Vojvodine.",
            "features": "Navigacija, xenon, parking asistencija",
            "location": "Novi Sad", "pickup_options": "Agencija, hotel",
            "deposit_info": "Dogovor", "cancellation_policy": "48h unapred.",
            "min_driver_age": 23, "views_count": 88, "images_key": "audi",
        }),
        (pubs[1].id, {
            "brand": "Volkswagen", "model": "Tiguan", "year": 2021, "price_per_day": 68, "fuel": "Dizel",
            "transmission": "Automatski", "body_type": "SUV", "seats": 5, "doors": 5, "mileage": 48000,
            "description": "SUV visokog komfora.",
            "features": "4MOTION, kamera, grejanje sedišta",
            "location": "Novi Sad", "pickup_options": "Agencija",
            "deposit_info": "Dogovor", "cancellation_policy": "Po dogovoru.",
            "min_driver_age": 23, "views_count": 112, "images_key": "vw",
        }),
        (pubs[2].id, {
            "brand": "Mercedes", "model": "GLA 200", "year": 2023, "price_per_day": 89, "fuel": "Benzin",
            "transmission": "Automatski", "body_type": "SUV", "seats": 5, "doors": 5, "mileage": 12000,
            "description": "Noviji kompaktni SUV, odličan za putovanja.",
            "features": "MBUX, kamera 360, koža",
            "location": "Niš", "pickup_options": "Agencija, aerodrom Niš",
            "deposit_info": "Dogovor", "cancellation_policy": "Otkazivanje 48h.",
            "min_driver_age": 25, "views_count": 45, "images_key": "mercedes",
        }),
        (pubs[2].id, {
            "brand": "Toyota", "model": "Corolla", "year": 2022, "price_per_day": 39, "fuel": "Hibrid",
            "transmission": "Automatski", "body_type": "Limuzina", "seats": 5, "doors": 4, "mileage": 27000,
            "description": "Pouzdana i štedljiva Corolla.",
            "features": "Hibrid, klima, kamera",
            "location": "Niš", "pickup_options": "Agencija",
            "deposit_info": "Dogovor", "cancellation_policy": "24h unapred.",
            "min_driver_age": 21, "views_count": 59, "images_key": "toyota",
        }),
        (pubs[2].id, {
            "brand": "BMW", "model": "X1", "year": 2021, "price_per_day": 78, "fuel": "Dizel",
            "transmission": "Automatski", "body_type": "SUV", "seats": 5, "doors": 5, "mileage": 39000,
            "description": "Kompaktni BMW SUV.",
            "features": "xDrive, navigacija, parking senzori",
            "location": "Niš", "pickup_options": "Agencija, hotel",
            "deposit_info": "Dogovor", "cancellation_policy": "Po dogovoru.",
            "min_driver_age": 23, "views_count": 71, "images_key": "bmw",
        }),
        (pubs[0].id, {
            "brand": "Audi", "model": "Q5", "year": 2022, "price_per_day": 110, "fuel": "Dizel",
            "transmission": "Automatski", "body_type": "SUV", "seats": 5, "doors": 5, "mileage": 29000,
            "description": "Premium Q5 za duža putovanja i porodicu.",
            "features": "Quattro, virtual cockpit, kamera, koža",
            "location": "Beograd", "pickup_options": "Agencija, aerodrom",
            "deposit_info": "Dogovor sa izdavačem", "cancellation_policy": "48h unapred.",
            "min_driver_age": 25, "views_count": 133, "images_key": "audi",
        }),
    ]

    created: list[Car] = []
    for publisher_id, spec in cars_spec:
        created.append(add_car(db, publisher_id, spec, spec.get("images_key", "bmw")))

    db.add_all(
        [
            AvailabilityBlock(car_id=created[0].id, date_from=today + timedelta(days=10), date_to=today + timedelta(days=14), reason="Već izdato"),
            AvailabilityBlock(car_id=created[1].id, date_from=today + timedelta(days=3), date_to=today + timedelta(days=6), reason="Servis"),
            AvailabilityBlock(car_id=created[4].id, date_from=today + timedelta(days=20), date_to=today + timedelta(days=25), reason="Blokirano"),
        ]
    )

    db.add_all(
        [
            Inquiry(
                car_id=created[0].id,
                publisher_id=pubs[0].id,
                pickup_date=today + timedelta(days=16),
                return_date=today + timedelta(days=20),
                pickup_location="Beograd — aerodrom",
                full_name="Marko Marković",
                phone="+381 64 555 0101",
                email="marko@example.com",
                message="Da li je automobil dostupan i da li može preuzimanje uveče?",
                status="PENDING",
            ),
            Inquiry(
                car_id=created[2].id,
                publisher_id=pubs[0].id,
                pickup_date=today + timedelta(days=2),
                return_date=today + timedelta(days=5),
                pickup_location="Beograd centar",
                full_name="Jelena Ilić",
                phone="+381 63 444 2211",
                email="jelena@example.com",
                message="Trebaju nam dečije sedište ako je moguće.",
                status="ANSWERED",
            ),
            Inquiry(
                car_id=created[5].id,
                publisher_id=pubs[1].id,
                pickup_date=today + timedelta(days=8),
                return_date=today + timedelta(days=12),
                pickup_location="Novi Sad",
                full_name="Petar Simić",
                phone="+381 60 333 1199",
                email="",
                message="Molim potvrdu dostupnosti za vikend.",
                status="PENDING",
            ),
        ]
    )

    db.commit()
    db.close()
    print("Demo podaci su ubačeni. Nalozi:")
    print("  Admin:     admin@rentlist.rs / admin123")
    print("  BeoDrive:  drive@beograd.rs / demo123")
    print("  AdriaCar:  info@adriacar.rs / demo123")
    print("  Coastline: hello@coastline.rs / demo123")


if __name__ == "__main__":
    seed()
