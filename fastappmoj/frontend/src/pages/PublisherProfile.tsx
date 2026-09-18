import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api/client";
import CarCardItem from "../components/CarCardItem";
import type { CarCard, PublisherPublic } from "../types";

export default function PublisherProfile() {
  const { id } = useParams();
  const [pub, setPub] = useState<PublisherPublic | null>(null);
  const [cars, setCars] = useState<CarCard[]>([]);
  useEffect(() => {
    api.get<PublisherPublic>(`/publishers/${id}`).then(setPub);
    api.get<CarCard[]>(`/publishers/${id}/cars`).then(setCars);
  }, [id]);
  if (!pub) return <div className="container section">Učitavanje...</div>;
  return (
    <div className="container section">
      <div className="panel">
        <h1>
          {pub.agency_name} {pub.verified && <span className="badge">Verified</span>}
        </h1>
        <p>{pub.description}</p>
        <div className="meta">
          <span>{pub.location}</span>
          <span>{pub.phone}</span>
          <span>{pub.email}</span>
          <span>{pub.cars_count} vozila</span>
        </div>
      </div>
      <h2 style={{ marginTop: 28 }}>Vozila ovog izdavača</h2>
      <div className="grid">{cars.map((car) => <CarCardItem key={car.id} car={car} />)}</div>
    </div>
  );
}
