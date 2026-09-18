import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function PublisherLogin() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState("");
  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const data = new FormData(e.currentTarget);
    try {
      const me = await login(String(data.get("email")), String(data.get("password")));
      navigate(me.role === "ADMIN" ? "/admin" : "/publisher");
    } catch (err) {
      setError((err as Error).message);
    }
  }
  return (
    <div className="container section">
      <form className="panel form" style={{ maxWidth: 420, margin: "0 auto" }} onSubmit={onSubmit}>
        <h2>Prijava izdavača / admina</h2>
        {error && <div className="error">{error}</div>}
        <label>Email<input name="email" type="email" required defaultValue="drive@beograd.rs" /></label>
        <label>Lozinka<input name="password" type="password" required defaultValue="demo123" /></label>
        <button className="btn" type="submit">Prijavi se</button>
        <p>Nemaš nalog? <Link to="/publisher/register">Registruj agenciju</Link></p>
        <p className="meta">Admin: admin@rentlist.rs / admin123</p>
      </form>
    </div>
  );
}
