import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../api/client";
import type { CarCard } from "../../types";

export default function AdminCars() {
  const [items, setItems] = useState<CarCard[]>([]);
  async function load() {
    setItems(await api.get<CarCard[]>("/admin/cars"));
  }
  useEffect(() => { void load(); }, []);
  async function remove(id: number) {
    if (!confirm("Ukloniti oglas?")) return;
    await api.delete(`/admin/cars/${id}`);
    await load();
  }
  return (
    <div>
      <h1>Vozila</h1>
      <table className="table">
        <thead><tr><th>Vozilo</th><th>Izdavač</th><th>Cena</th><th></th></tr></thead>
        <tbody>
          {items.map((c) => (
            <tr key={c.id}>
              <td><Link to={`/cars/${c.id}`}>{c.brand} {c.model}</Link></td>
              <td>{c.publisher.agency_name}</td>
              <td>{c.price_per_day} €</td>
              <td><button className="btn-danger" onClick={() => remove(c.id)}>Ukloni oglas</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
