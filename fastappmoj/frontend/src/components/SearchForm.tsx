import { FormEvent } from "react";
import { useNavigate } from "react-router-dom";

type Props = {
  defaults?: Record<string, string>;
};

export default function SearchForm({ defaults = {} }: Props) {
  const navigate = useNavigate();

  function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const data = new FormData(e.currentTarget);
    const params = new URLSearchParams();
    ["location", "pickup_date", "return_date", "max_price"].forEach((key) => {
      const value = String(data.get(key) || "");
      if (value) params.set(key, value);
    });
    navigate(`/search?${params.toString()}`);
  }

  return (
    <form className="search-card" onSubmit={onSubmit}>
      <label>
        Lokacija
        <input name="location" placeholder="Beograd, Novi Sad..." defaultValue={defaults.location || ""} />
      </label>
      <label>
        Preuzimanje
        <input type="date" name="pickup_date" defaultValue={defaults.pickup_date || ""} />
      </label>
      <label>
        Vraćanje
        <input type="date" name="return_date" defaultValue={defaults.return_date || ""} />
      </label>
      <label>
        Budžet do (€)
        <input type="number" name="max_price" min={1} placeholder="npr. 80" defaultValue={defaults.max_price || ""} />
      </label>
      <button className="btn" type="submit">
        Pretraži
      </button>
    </form>
  );
}
