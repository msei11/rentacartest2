import { FormEvent, useEffect, useState } from "react";
import { api } from "../../api/client";
import type { PublisherPublic } from "../../types";

export default function PublisherProfileEdit() {
  const [profile, setProfile] = useState<PublisherPublic | null>(null);
  const [ok, setOk] = useState(false);
  useEffect(() => {
    api.get<PublisherPublic>("/publisher/me").then(setProfile);
  }, []);
  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const d = new FormData(e.currentTarget);
    const updated = await api.patch<PublisherPublic>("/publisher/me", {
      agency_name: d.get("agency_name"),
      contact_name: d.get("contact_name"),
      phone: d.get("phone"),
      location: d.get("location"),
      description: d.get("description"),
      logo_url: d.get("logo_url"),
    });
    setProfile(updated);
    setOk(true);
  }
  if (!profile) return <p>Učitavanje...</p>;
  return (
    <form className="panel form" style={{ maxWidth: 560 }} onSubmit={onSubmit}>
      <h1>Profil izdavača</h1>
      {ok && <div className="notice">Profil je sačuvan.</div>}
      <label>Naziv<input name="agency_name" defaultValue={profile.agency_name} /></label>
      <label>Kontakt<input name="contact_name" defaultValue={profile.contact_name} /></label>
      <label>Telefon<input name="phone" defaultValue={profile.phone} /></label>
      <label>Lokacija<input name="location" defaultValue={profile.location} /></label>
      <label>Logo URL<input name="logo_url" defaultValue={profile.logo_url} /></label>
      <label>Opis<textarea name="description" rows={4} defaultValue={profile.description} /></label>
      <button className="btn" type="submit">Sačuvaj</button>
    </form>
  );
}
