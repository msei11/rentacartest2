import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../api/client";
import type { Inquiry } from "../../types";

export default function PublisherInquiries() {
  const [items, setItems] = useState<Inquiry[]>([]);
  useEffect(() => {
    api.get<Inquiry[]>("/publisher/inquiries").then(setItems);
  }, []);
  return (
    <div>
      <h1>Upiti</h1>
      {items.map((i) => (
        <Link key={i.id} to={`/publisher/inquiries/${i.id}`} className="panel" style={{ display: "block", marginBottom: 12 }}>
          <div className="toolbar">
            <strong>NEW INQUIRY · {i.car_title}</strong>
            <span className={`status ${i.status}`}>{i.status}</span>
          </div>
          <p>{i.pickup_date} → {i.return_date}</p>
          <p>{i.full_name} · {i.phone}</p>
          <p>{i.message || "—"}</p>
        </Link>
      ))}
    </div>
  );
}
