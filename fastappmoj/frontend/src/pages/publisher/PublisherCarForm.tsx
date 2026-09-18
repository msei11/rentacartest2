import { FormEvent, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api } from "../../api/client";
import type { CarDetail } from "../../types";

const fields = [
  ["brand", "Marka"],
  ["model", "Model"],
  ["year", "Godište"],
  ["price_per_day", "Cena po danu"],
  ["fuel", "Gorivo"],
  ["transmission", "Menjač"],
  ["body_type", "Karoserija"],
  ["seats", "Sedišta"],
  ["doors", "Vrata"],
  ["mileage", "Kilometraža"],
  ["location", "Lokacija"],
  ["pickup_options", "Pickup opcije"],
  ["deposit_info", "Depozit (info)"],
  ["min_driver_age", "Min. starost vozača"],
];

export default function PublisherCarForm({ mode }: { mode: "create" | "edit" }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [car, setCar] = useState<CarDetail | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (mode === "edit" && id) api.get<CarDetail>(`/publisher/cars/${id}`).then(setCar);
  }, [mode, id]);

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const d = new FormData(e.currentTarget);
    const payload: Record<string, unknown> = {};
    fields.forEach(([key]) => {
      const v = String(d.get(key) || "");
      payload[key] = ["year", "price_per_day", "seats", "doors", "mileage", "min_driver_age"].includes(key)
        ? Number(v)
        : v;
    });
    payload.description = String(d.get("description") || "");
    payload.features = String(d.get("features") || "");
    payload.cancellation_policy = String(d.get("cancellation_policy") || "");
    try {
      if (mode === "create") {
        const urls = String(d.get("image_urls") || "")
          .split("\n")
          .map((s) => s.trim())
          .filter(Boolean);
        const created = await api.post<{ id: number }>("/publisher/cars", { ...payload, image_urls: urls });
        const file = d.get("file") as File;
        if (file && file.size) await api.upload(`/publisher/cars/${created.id}/images`, file);
        navigate("/publisher/cars");
      } else {
        await api.patch(`/publisher/cars/${id}`, payload);
        const file = d.get("file") as File;
        if (file && file.size) await api.upload(`/publisher/cars/${id}/images`, file);
        navigate("/publisher/cars");
      }
    } catch (err) {
      setError((err as Error).message);
    }
  }

  if (mode === "edit" && !car) return <p>Učitavanje...</p>;

  const val = (key: string, fallback = "") =>
    car ? String((car as unknown as Record<string, unknown>)[key] ?? fallback) : fallback;

  return (
    <div>
      <h1>{mode === "create" ? "Dodaj vozilo" : "Izmeni vozilo"}</h1>
      {error && <div className="error">{error}</div>}
      <form className="form two panel" onSubmit={onSubmit}>
        {fields.map(([key, label]) => (
          <label key={key}>
            {label}
            <input name={key} defaultValue={val(key)} required={["brand", "model", "location"].includes(key)} />
          </label>
        ))}
        <label style={{ gridColumn: "1 / -1" }}>Opis<textarea name="description" rows={3} defaultValue={car?.description} /></label>
        <label style={{ gridColumn: "1 / -1" }}>Features (zarezom)<input name="features" defaultValue={car?.features.join(", ")} /></label>
        <label style={{ gridColumn: "1 / -1" }}>Politika otkazivanja<textarea name="cancellation_policy" rows={2} defaultValue={car?.cancellation_policy} /></label>
        {mode === "create" && (
          <label style={{ gridColumn: "1 / -1" }}>
            URL fotografija (jedan po liniji)
            <textarea name="image_urls" rows={3} placeholder="https://..." />
          </label>
        )}
        <label>Upload fotografije<input type="file" name="file" accept="image/*" /></label>
        <div style={{ gridColumn: "1 / -1" }}>
          <button className="btn" type="submit">Sačuvaj</button>
        </div>
      </form>
    </div>
  );
}
