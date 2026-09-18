# RentList — prototip oglasnika za rent-a-car

MVP / demo aplikacija za oglašavanje vozila za iznajmljivanje. Platforma **nije** rent-a-car agencija: ne naplaćuje najam, ne rezerviše vozila i ne procesira plaćanja. Korisnik šalje **upit (inquiry)**, a izdavač dogovara detalje van platforme.

## 1. Requirements

- Python 3.11+
- Node.js 18+
- pip, npm

## 2. Installation

### Backend

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## 3. Database setup

Koristi se SQLite fajl `backend/rental.db`. Tabele se kreiraju automatski pri startu FastAPI-ja ili pri seed-u.

## 4. Seed demo data

```bash
cd backend
python seed.py
```

Skripta pravi 3 izdavača, 12 vozila, availability blokove i demo upite.

## 5. How to start FastAPI

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

API: http://127.0.0.1:8000  
Docs: http://127.0.0.1:8000/docs

## 6. How to start React

```bash
cd frontend
npm run dev
```

Aplikacija: http://localhost:5173  
Vite proxy šalje `/api` i `/uploads` na backend.

## 7. Demo login credentials

| Uloga | Email | Lozinka |
|---|---|---|
| Admin | admin@rentlist.rs | admin123 |
| Izdavač BeoDrive (Beograd) | drive@beograd.rs | demo123 |
| Izdavač AdriaCar (Novi Sad) | info@adriacar.rs | demo123 |
| Izdavač Coastline (Niš) | hello@coastline.rs | demo123 |

Javni korisnik **ne mora** da se registruje.

## 8. API overview

**Public**

- `GET /api/home`
- `GET /api/cars` (filteri: location, pickup_date, return_date, brand, model, min/max_price, fuel, transmission, body_type, seats, year_from/to, sort)
- `GET /api/cars/{id}`
- `GET /api/cars/{id}/availability`
- `GET /api/publishers/{id}`
- `GET /api/publishers/{id}/cars`
- `POST /api/inquiries`

**Auth**

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/me`

**Publisher** (Bearer JWT)

- `GET/PATCH /api/publisher/me`
- `GET /api/publisher/stats`
- `GET/POST /api/publisher/cars`
- `GET/PATCH/DELETE /api/publisher/cars/{id}`
- `POST /api/publisher/cars/{id}/images`
- `DELETE /api/publisher/cars/{id}/images/{image_id}`
- `GET/POST /api/publisher/cars/{id}/availability`
- `DELETE /api/publisher/cars/{id}/availability/{block_id}`
- `GET/PATCH /api/publisher/inquiries[/{id}]`

**Admin**

- `GET /api/admin/publishers`
- `PATCH /api/admin/publishers/{id}` (verified / suspended)
- `GET /api/admin/cars`
- `DELETE /api/admin/cars/{id}`
- `GET /api/admin/inquiries`

## 9. Arhitektura

```
backend/     FastAPI + SQLAlchemy + SQLite
frontend/    React + TypeScript + Vite
```

- Autentifikacija: jednostavan JWT prototip (nije production security).
- Slike: lokalni `backend/uploads` ili URL-ovi (demo koristi Unsplash).
- Kalendar dostupnosti: periodi blokade (`date_from`–`date_to`), ne booking engine.
- Statusi upita: `PENDING`, `ANSWERED`, `CLOSED`.

Glavni tok: **Home → Search → Details → Proveri dostupnost → Pošalji upit → Publisher inbox**.
