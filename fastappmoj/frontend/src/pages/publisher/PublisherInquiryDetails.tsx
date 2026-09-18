import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../../api/client";
import type { Inquiry } from "../../types";

export default function PublisherInquiryDetails() {
  const { id } = useParams();
  const [item, setItem] = useState<Inquiry | null>(null);
  async function load() {
    setItem(await api.get<Inquiry>(`/publisher/inquiries/${id}`));
  }
  useEffect(() => { void load(); }, [id]);
  async function setStatus(status: string) {
    setItem(await api.patch<Inquiry>(`/publisher/inquiries/${id}`, { status }));
  }
  if (!item) return <p>Učitavanje...</p>;
  return (
    <div className="panel" style={{ maxWidth: 640 }}>
      <h1>{item.car_title}</h1>
      <p>{item.pickup_date} → {item.return_date}</p>
      <p>Preuzimanje: {item.pickup_location}</p>
      <h3>{item.full_name}</h3>
      <p>Telefon: <a href={`tel:${item.phone}`}>{item.phone}</a></p>
      {item.email && <p>Email: <a href={`mailto:${item.email}`}>{item.email}</a></p>}
      <p>{item.message}</p>
      <p className={`status ${item.status}`}>{item.status}</p>
      <div className="toolbar">
        <button className="btn" onClick={() => setStatus("ANSWERED")}>Označi ANSWERED</button>
        <button className="btn-ghost" onClick={() => setStatus("CLOSED")}>Označi CLOSED</button>
        <button className="btn-ghost" onClick={() => setStatus("PENDING")}>Vrati na PENDING</button>
      </div>
    </div>
  );
}
