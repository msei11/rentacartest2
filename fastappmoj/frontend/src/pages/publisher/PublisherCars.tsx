import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../../api/client";
import type { CarCard } from "../../types";

export default function PublisherCars() {
  const [cars, setCars] = useState<CarCard[]>([]);
  async function load() {
    setCars(await api.get<CarCard[]>("/publisher/cars"));
  }
  useEffect(() => { void load(); }, []);
  async function remove(id: number) {
    if (!confirm("Obrisati oglas?")) return;
    await api.delete(`/publisher/cars/${id}`);
    await load();
  }
  return (
    <div>
      <div className="toolbar">
        <h1>Moja vozila</h1>
        <Link className="btn" to="/publisher/cars/new">Dodaj vozilo</Link>
      </div>
      <table className="table">
        <thead>
          <tr><th>Vozilo</th><th>Lokacija</th><th>Cena</th><th></th></tr>
        </thead>
        <tbody>
          {cars.map((c) => (
            <tr key={c.id}>
              <td>{c.brand} {c.model} ({c.year})</td>
              <td>{c.location}</td>
              <td>{c.price_per_day} €</td>
              <td className="meta">
                <Link to={`/cars/${c.id}`}>View</Link> ·
                <Link to={`/publisher/cars/${c.id}/edit`}> Edit</Link> ·
                <Link to={`/publisher/cars/${c.id}/calendar`}> Kalendar</Link> ·
                <button className="btn-ghost" onClick={() => remove(c.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
