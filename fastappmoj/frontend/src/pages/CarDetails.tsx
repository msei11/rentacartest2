import { useEffect, useState } from "react";
import { Link, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { api } from "../api/client";
import AvailabilityCalendar from "../components/AvailabilityCalendar";
import type { CarDetail } from "../types";

export default function CarDetails() {
  const { id } = useParams();
  const [car, setCar] = useState<CarDetail | null>(null);
  const [error, setError] = useState("");
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const [pickup, setPickup] = useState(params.get("pickup_date") || "");
  const [ret, setRet] = useState(params.get("return_date") || "");
  const [avail, setAvail] = useState<{ available: boolean; message: string } | null>(null);

  useEffect(() => {
    api.get<CarDetail>(`/cars/${id}`).then(setCar).catch((e: Error) => setError(e.message));
  }, [id]);

  async function check() {
    if (!pickup || !ret) return;
    const q = new URLSearchParams({ pickup_date: pickup, return_date: ret });
    const res = await api.get<{ available: boolean; message: string }>(`/cars/${id}/availability?${q}`);
    setAvail(res);
  }

  if (error) return <div className="container section"><div className="error">{error}</div></div>;
  if (!car) return <div className="container section">Učitavanje...</div>;
  const hero = car.images[0]?.url;

  return (
    <div className="container details">
      <div>
        <div className="gallery">
          <img src={hero} alt="" />
          <div className="thumbs">
            {car.images.slice(1, 3).map((img) => (
              <img key={img.id} src={img.url} alt="" />
            ))}
          </div>
        </div>
        <div className="panel" style={{ marginTop: 16 }}>
          <h1>
            {car.brand} {car.model} <span className="meta">{car.year}</span>
          </h1>
          <div className="specs">
            <div>Gorivo: {car.fuel}</div>
            <div>Menjač: {car.transmission}</div>
            <div>Karoserija: {car.body_type}</div>
            <div>Sedišta: {car.seats}</div>
            <div>Vrata: {car.doors}</div>
            <div>Kilometraža: {car.mileage.toLocaleString()} km</div>
            <div>Lokacija: {car.location}</div>
            <div>Preuzimanje: {car.pickup_options}</div>
            <div>Depozit: {car.deposit_info}</div>
            <div>Min. starost: {car.min_driver_age}</div>
          </div>
          <p>{car.description}</p>
          <p><strong>Otkazivanje:</strong> {car.cancellation_policy}</p>
          <div className="chips">
            {car.features.map((f) => (
              <span key={f} className="chip">{f}</span>
            ))}
          </div>
        </div>
      </div>
      <div>
        <div className="panel">
          <div className="price">{car.price_per_day} € / dan</div>
          <p className="meta">Cena je informativna. Plaćanje ide direktno izdavaču.</p>
          <label>
            Preuzimanje
            <input type="date" value={pickup} onChange={(e) => setPickup(e.target.value)} />
          </label>
          <label>
            Vraćanje
            <input type="date" value={ret} onChange={(e) => setRet(e.target.value)} />
          </label>
          <div className="toolbar">
            <button className="btn-ghost" onClick={check}>Proveri dostupnost</button>
            <button
              className="btn"
              onClick={() => navigate(`/cars/${car.id}/inquiry?pickup_date=${pickup}&return_date=${ret}`)}
            >
              Pošalji upit
            </button>
          </div>
          {avail && <div className={avail.available ? "notice" : "error"}>{avail.message}</div>}
        </div>
        <div className="panel" style={{ marginTop: 14 }}>
          <h3>Dostupnost</h3>
          <AvailabilityCalendar blocks={car.availability_blocks} />
        </div>
        <div className="panel" style={{ marginTop: 14 }}>
          <h3>Izdavač</h3>
          <p>
            <Link to={`/publishers/${car.publisher.id}`}>
              <strong>{car.publisher.agency_name}</strong>
            </Link>{" "}
            {car.publisher.verified && <span className="badge">Verified</span>}
          </p>
          <p>{car.publisher.location}</p>
          <p>{car.publisher.phone}</p>
        </div>
      </div>
    </div>
  );
}
