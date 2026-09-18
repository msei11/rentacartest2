import { useEffect, useState } from "react";
import { api } from "../../api/client";
import type { PublisherPublic } from "../../types";

export default function AdminPublishers() {
  const [items, setItems] = useState<PublisherPublic[]>([]);
  async function load() {
    setItems(await api.get<PublisherPublic[]>("/admin/publishers"));
  }
  useEffect(() => { void load(); }, []);
  async function patch(id: number, body: Record<string, boolean>) {
    await api.patch(`/admin/publishers/${id}`, body);
    await load();
  }
  return (
    <div>
      <h1>Izdavači</h1>
      <table className="table">
        <thead><tr><th>Agencija</th><th>Lokacija</th><th>Verified</th><th>Suspendovan</th><th></th></tr></thead>
        <tbody>
          {items.map((p) => (
            <tr key={p.id}>
              <td>{p.agency_name}</td>
              <td>{p.location}</td>
              <td>{p.verified ? "da" : "ne"}</td>
              <td>{p.suspended ? "da" : "ne"}</td>
              <td>
                <button className="btn-ghost" onClick={() => patch(p.id, { verified: !p.verified })}>
                  {p.verified ? "Unverify" : "Verify"}
                </button>
                <button className="btn-danger" onClick={() => patch(p.id, { suspended: !p.suspended })}>
                  {p.suspended ? "Aktiviraj" : "Suspenduj"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
