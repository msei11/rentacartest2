import { FormEvent, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../../api/client";
import AvailabilityCalendar from "../../components/AvailabilityCalendar";
import type { AvailabilityBlock, CarDetail } from "../../types";

export default function PublisherCarCalendar() {
  const { id } = useParams();
  const [car, setCar] = useState<CarDetail | null>(null);
  const [blocks, setBlocks] = useState<AvailabilityBlock[]>([]);
  async function load() {
    const c = await api.get<CarDetail>(`/publisher/cars/${id}`);
    setCar(c);
    setBlocks(await api.get<AvailabilityBlock[]>(`/publisher/cars/${id}/availability`));
  }
  useEffect(() => { void load(); }, [id]);
  async function add(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const d = new FormData(e.currentTarget);
    await api.post(`/publisher/cars/${id}/availability`, {
      date_from: d.get("date_from"),
      date_to: d.get("date_to"),
      reason: d.get("reason"),
    });
    e.currentTarget.reset();
    await load();
  }
  async function remove(blockId: number) {
    await api.delete(`/publisher/cars/${id}/availability/${blockId}`);
    await load();
  }
  if (!car) return <p>Učitavanje...</p>;
  return (
    <div>
      <h1>Kalendar — {car.brand} {car.model}</h1>
      <div className="panel" style={{ maxWidth: 520, marginBottom: 16 }}>
        <AvailabilityCalendar blocks={blocks} />
      </div>
      <form className="panel form" style={{ maxWidth: 520 }} onSubmit={add}>
        <h3>Dodaj blokirani period</h3>
        <label>Od<input type="date" name="date_from" required /></label>
        <label>Do<input type="date" name="date_to" required /></label>
        <label>Razlog<input name="reason" placeholder="Already rented" /></label>
        <button className="btn" type="submit">Blokiraj</button>
      </form>
      <table className="table" style={{ marginTop: 16 }}>
        <thead><tr><th>Period</th><th>Razlog</th><th></th></tr></thead>
        <tbody>
          {blocks.map((b) => (
            <tr key={b.id}>
              <td>{b.date_from} — {b.date_to}</td>
              <td>{b.reason}</td>
              <td><button className="btn-danger" onClick={() => remove(b.id)}>Obriši</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
