import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../api/client";
import type { Inquiry, PublisherStats } from "../../types";

export default function PublisherDashboard() {
  const [stats, setStats] = useState<PublisherStats | null>(null);
  const [inquiries, setInquiries] = useState<Inquiry[]>([]);
  useEffect(() => {
    api.get<PublisherStats>("/publisher/stats").then(setStats);
    api.get<Inquiry[]>("/publisher/inquiries").then(setInquiries);
  }, []);
  const newest = inquiries.filter((i) => i.status === "PENDING");
  return (
    <div>
      <h1>Dashboard</h1>
      {newest.length > 0 && <div className="notice">New inquiry received — {newest.length} novih upita.</div>}
      <div className="stats" style={{ marginTop: 16 }}>
        <div className="stat"><div className="meta">Vozila</div><strong>{stats?.cars_count ?? "-"}</strong></div>
        <div className="stat"><div className="meta">Aktivni oglasi</div><strong>{stats?.active_cars ?? "-"}</strong></div>
        <div className="stat"><div className="meta">Novi upiti</div><strong>{stats?.new_inquiries ?? "-"}</strong></div>
        <div className="stat"><div className="meta">Pregledi</div><strong>{stats?.views_count ?? "-"}</strong></div>
      </div>
      <div className="toolbar" style={{ marginTop: 24 }}>
        <h2>Najnoviji upiti</h2>
        <Link className="btn" to="/publisher/inquiries">Inbox</Link>
      </div>
      <table className="table">
        <thead>
          <tr><th>Vozilo</th><th>Period</th><th>Kontakt</th><th>Status</th></tr>
        </thead>
        <tbody>
          {inquiries.slice(0, 5).map((i) => (
            <tr key={i.id}>
              <td><Link to={`/publisher/inquiries/${i.id}`}>{i.car_title}</Link></td>
              <td>{i.pickup_date} → {i.return_date}</td>
              <td>{i.full_name}</td>
              <td className={`status ${i.status}`}>{i.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
