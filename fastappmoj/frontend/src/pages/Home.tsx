import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import CarCardItem from "../components/CarCardItem";
import SearchForm from "../components/SearchForm";
import type { HomePayload } from "../types";

export default function Home() {
  const [data, setData] = useState<HomePayload | null>(null);
  useEffect(() => {
    api.get<HomePayload>("/home").then(setData).catch(() => setData({ popular_cars: [], popular_locations: [], featured_publishers: [] }));
  }, []);

  return (
    <>
      <section className="hero">
        <div className="container">
          <h1>Pronađi automobil za iznajmljivanje</h1>
          <p>
            Oglasnik za male rent-a-car agencije. Uporedi vozila, proveri dostupnost i pošalji upit izdavaču — bez
            online plaćanja i bez lažnih rezervacija.
          </p>
          <SearchForm />
        </div>
      </section>
      <section className="section">
        <div className="container">
          <h2>Kako platforma radi</h2>
          <div className="how">
            <div>
              <h3>1. Pretraži</h3>
              <p>Filtriraj po lokaciji, datumima, ceni i opremi.</p>
            </div>
            <div>
              <h3>2. Pošalji upit</h3>
              <p>Ostavi telefon. Izdavač te kontaktira i dogovara najam van platforme.</p>
            </div>
            <div>
              <h3>3. Dogovor direktno</h3>
              <p>RentList ne naplaćuje, ne rezerviše i ne drži depozit.</p>
            </div>
          </div>
        </div>
      </section>
      <section className="section">
        <div className="container">
          <h2>Popularna vozila</h2>
          <div className="grid">{data?.popular_cars.map((car) => <CarCardItem key={car.id} car={car} />)}</div>
        </div>
      </section>
      <section className="section">
        <div className="container">
          <h2>Popularne lokacije</h2>
          <div className="chips">
            {data?.popular_locations.map((loc) => (
              <Link key={loc} className="chip" to={`/search?location=${encodeURIComponent(loc)}`}>
                {loc}
              </Link>
            ))}
          </div>
        </div>
      </section>
      <section className="section">
        <div className="container">
          <h2>Preporučeni izdavači</h2>
          <div className="grid">
            {data?.featured_publishers.map((p) => (
              <Link key={p.id} to={`/publishers/${p.id}`} className="card">
                <div className="card-body">
                  <strong>{p.agency_name}</strong> {p.verified && <span className="badge">Verified</span>}
                  <p>{p.location}</p>
                  <p className="meta">{p.cars_count} aktivnih vozila</p>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
