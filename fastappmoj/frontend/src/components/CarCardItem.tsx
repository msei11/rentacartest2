import { Link } from "react-router-dom";
import type { CarCard } from "../types";

export default function CarCardItem({ car }: { car: CarCard }) {
  return (
    <Link to={`/cars/${car.id}`} className="card">
      <img src={car.primary_image || "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=800"} alt={`${car.brand} ${car.model}`} />
      <div className="card-body">
        <div className="toolbar" style={{ marginBottom: 6 }}>
          <strong>
            {car.brand} {car.model}
          </strong>
          {car.publisher.verified && <span className="badge">Verified</span>}
        </div>
        <div className="meta">
          <span>{car.year}</span>
          <span>{car.fuel}</span>
          <span>{car.transmission}</span>
          <span>{car.seats} sed.</span>
        </div>
        <p style={{ margin: "10px 0 6px" }}>{car.location} · {car.publisher.agency_name}</p>
        <div className="price">{car.price_per_day} € / dan</div>
      </div>
    </Link>
  );
}
