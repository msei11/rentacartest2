import { FormEvent, useEffect, useState } from "react";
import { useNavigate, useParams, useSearchParams } from "react-router-dom";
import { api } from "../api/client";
import type { CarDetail } from "../types";

export default function InquiryForm() {
  const { id } = useParams();
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const [car, setCar] = useState<CarDetail | null>(null);
  const [done, setDone] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get<CarDetail>(`/cars/${id}`).then(setCar);
  }, [id]);

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");
    const data = new FormData(e.currentTarget);
    try {
      await api.post("/inquiries", {
        car_id: Number(id),
        pickup_date: data.get("pickup_date"),
        return_date: data.get("return_date"),
        pickup_location: data.get("pickup_location"),
        full_name: data.get("full_name"),
        phone: data.get("phone"),
        email: data.get("email"),
        message: data.get("message"),
      });
      setDone(true);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  if (done) {
    return (
      <div className="container section">
        <div className="panel">
          <h2>Vaš upit je uspešno poslat.</h2>
          <p>Izdavač će vas kontaktirati telefonom, SMS-om ili emailom. RentList ne potvrđuje rezervaciju.</p>
          <button className="btn" onClick={() => navigate("/")}>Nazad na početnu</button>
        </div>
      </div>
    );
  }

  return (
    <div className="container section">
      <div className="panel" style={{ maxWidth: 640, margin: "0 auto" }}>
        <h2>Pošalji upit {car ? `— ${car.brand} ${car.model}` : ""}</h2>
        <p className="meta">Nije potrebna registracija. Ovo nije rezervacija niti plaćanje.</p>
        {error && <div className="error">{error}</div>}
        <form className="form" onSubmit={onSubmit}>
          <label>Datum preuzimanja<input type="date" name="pickup_date" required defaultValue={params.get("pickup_date") || ""} /></label>
          <label>Datum vraćanja<input type="date" name="return_date" required defaultValue={params.get("return_date") || ""} /></label>
          <label>Lokacija preuzimanja<input name="pickup_location" required defaultValue={car?.location || ""} /></label>
          <label>Ime i prezime<input name="full_name" required /></label>
          <label>Telefon<input name="phone" required /></label>
          <label>Email (opciono)<input type="email" name="email" /></label>
          <label>Poruka<textarea name="message" rows={4} placeholder="Da li je automobil dostupan?" /></label>
          <button className="btn" type="submit">Pošalji upit</button>
        </form>
      </div>
    </div>
  );
}
