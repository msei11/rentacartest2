import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export default function PublisherRegister() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");
  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const d = new FormData(e.currentTarget);
    try {
      await register({
        agency_name: String(d.get("agency_name")),
        contact_name: String(d.get("contact_name")),
        email: String(d.get("email")),
        phone: String(d.get("phone")),
        password: String(d.get("password")),
        location: String(d.get("location")),
        description: String(d.get("description")),
      });
      navigate("/publisher");
    } catch (err) {
      setError((err as Error).message);
    }
  }
  return (
    <div className="container section">
      <form className="panel form" style={{ maxWidth: 560, margin: "0 auto" }} onSubmit={onSubmit}>
        <h2>Registracija izdavača</h2>
        {error && <div className="error">{error}</div>}
        <label>Naziv agencije / izdavača<input name="agency_name" required /></label>
        <label>Ime kontakt osobe<input name="contact_name" required /></label>
        <label>Email<input name="email" type="email" required /></label>
        <label>Telefon<input name="phone" required /></label>
        <label>Lokacija<input name="location" /></label>
        <label>Lozinka<input name="password" type="password" minLength={6} required /></label>
        <label>Opis<textarea name="description" rows={3} /></label>
        <button className="btn" type="submit">Napravi nalog</button>
      </form>
    </div>
  );
}
