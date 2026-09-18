from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'rental.db'}"
UPLOAD_DIR = BASE_DIR / "uploads"
SECRET_KEY = "demo-prototype-secret-key-not-for-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
(UPLOAD_DIR / "cars").mkdir(exist_ok=True)
(UPLOAD_DIR / "publishers").mkdir(exist_ok=True)
