import { useEffect, useState } from "react";
import { api } from "../../api/client";
import type { Inquiry } from "../../types";

export default function AdminInquiries() {
  const [items, setItems] = useState<Inquiry[]>([]);
  useEffect(() => {
    api.get<Inquiry[]>("/admin/inquiries").then(setItems);
  }, []);
  return (
    <div>
      <h1>Svi upiti</h1>
      <table className="table">
        <thead><tr><th>Vozilo</th><th>Kontakt</th><th>Period</th><th>Status</th></tr></thead>
        <tbody>
          {items.map((i) => (
            <tr key={i.id}>
              <td>{i.car_title}</td>
              <td>{i.full_name} · {i.phone}</td>
              <td>{i.pickup_date} → {i.return_date}</td>
              <td className={`status ${i.status}`}>{i.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
