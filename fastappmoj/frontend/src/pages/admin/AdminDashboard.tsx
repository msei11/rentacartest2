import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../api/client";
import type { CarCard, Inquiry, PublisherPublic } from "../../types";

export default function AdminDashboard() {
  const [pubs, setPubs] = useState<PublisherPublic[]>([]);
  const [cars, setCars] = useState<CarCard[]>([]);
  const [inquiries, setInquiries] = useState<Inquiry[]>([]);
  useEffect(() => {
    api.get<PublisherPublic[]>("/admin/publishers").then(setPubs);
    api.get<CarCard[]>("/admin/cars").then(setCars);
    api.get<Inquiry[]>("/admin/inquiries").then(setInquiries);
  }, []);
  return (
    <div>
      <h1>Admin pregled</h1>
      <div className="stats">
        <Link className="stat" to="/admin/publishers"><div className="meta">Izdavači</div><strong>{pubs.length}</strong></Link>
        <Link className="stat" to="/admin/cars"><div className="meta">Vozila</div><strong>{cars.length}</strong></Link>
        <Link className="stat" to="/admin/inquiries"><div className="meta">Upiti</div><strong>{inquiries.length}</strong></Link>
      </div>
    </div>
  );
}
