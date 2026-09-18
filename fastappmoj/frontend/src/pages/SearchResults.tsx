import { FormEvent, useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { api, carsQuery } from "../api/client";
import CarCardItem from "../components/CarCardItem";
import type { CarCard } from "../types";

const empty = {
  location: "",
  pickup_date: "",
  return_date: "",
  brand: "",
  model: "",
  min_price: "",
  max_price: "",
  fuel: "",
  transmission: "",
  body_type: "",
  seats: "",
  year_from: "",
  year_to: "",
  sort: "newest",
};

export default function SearchResults() {
  const [params, setParams] = useSearchParams();
  const filters = useMemo(() => {
    const next = { ...empty };
    Object.keys(empty).forEach((key) => {
      next[key as keyof typeof empty] = params.get(key) || "";
    });
    return next;
  }, [params]);
  const [cars, setCars] = useState<CarCard[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api
      .get<CarCard[]>(carsQuery(filters))
      .then(setCars)
      .catch(() => setCars([]))
      .finally(() => setLoading(false));
  }, [params]);

  function apply(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const data = new FormData(e.currentTarget);
    const next = new URLSearchParams();
    Object.keys(empty).forEach((key) => {
      const value = String(data.get(key) || "");
      if (value) next.set(key, value);
    });
    setParams(next);
  }

  return (
    <div className="container layout-split">
      <form className="filters" onSubmit={apply}>
        <h3>Filteri</h3>
        <div className="stack">
          <label>Lokacija<input name="location" defaultValue={filters.location} /></label>
          <label>Preuzimanje<input type="date" name="pickup_date" defaultValue={filters.pickup_date} /></label>
          <label>Vraćanje<input type="date" name="return_date" defaultValue={filters.return_date} /></label>
          <label>Marka<input name="brand" defaultValue={filters.brand} /></label>
          <label>Model<input name="model" defaultValue={filters.model} /></label>
          <label>Cena od<input type="number" name="min_price" defaultValue={filters.min_price} /></label>
          <label>Cena do<input type="number" name="max_price" defaultValue={filters.max_price} /></label>
          <label>
            Gorivo
            <select name="fuel" defaultValue={filters.fuel}>
              <option value="">Sve</option>
              <option>Benzin</option>
              <option>Dizel</option>
              <option>Hibrid</option>
            </select>
          </label>
          <label>
            Menjač
            <select name="transmission" defaultValue={filters.transmission}>
              <option value="">Sve</option>
              <option>Manuelni</option>
              <option>Automatski</option>
            </select>
          </label>
          <label>
            Karoserija
            <select name="body_type" defaultValue={filters.body_type}>
              <option value="">Sve</option>
              <option>Limuzina</option>
              <option>Hatchback</option>
              <option>Karavan</option>
              <option>SUV</option>
            </select>
          </label>
          <label>Min. sedišta<input type="number" name="seats" defaultValue={filters.seats} /></label>
          <label>Godina od<input type="number" name="year_from" defaultValue={filters.year_from} /></label>
          <label>Godina do<input type="number" name="year_to" defaultValue={filters.year_to} /></label>
          <label>
            Sortiraj
            <select name="sort" defaultValue={filters.sort}>
              <option value="newest">Najnoviji oglasi</option>
              <option value="price_asc">Cena rastuće</option>
              <option value="price_desc">Cena opadajuće</option>
              <option value="popularity">Popularnost</option>
            </select>
          </label>
          <button className="btn" type="submit">Primeni</button>
        </div>
      </form>
      <div>
        <div className="toolbar">
          <h2>Rezultati pretrage</h2>
          <span className="meta">{loading ? "Učitavanje..." : `${cars.length} vozila`}</span>
        </div>
        <div className="grid">
          {cars.map((car) => (
            <CarCardItem key={car.id} car={car} />
          ))}
        </div>
      </div>
    </div>
  );
}
