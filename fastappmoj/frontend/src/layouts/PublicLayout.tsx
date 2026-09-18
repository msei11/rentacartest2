import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function PublicLayout({ children }: { children: React.ReactNode }) {
  const { user, logout } = useAuth();
  return (
    <>
      <header className="site-header">
        <div className="container header-inner">
          <NavLink to="/" className="logo">
            RENT<span>LIST</span>
          </NavLink>
          <nav className="nav">
            <NavLink to="/search">Pretraga</NavLink>
            {user?.role === "PUBLISHER" && <NavLink to="/publisher">Izdavač</NavLink>}
            {user?.role === "ADMIN" && <NavLink to="/admin">Admin</NavLink>}
            {user ? (
              <button className="btn-ghost" onClick={logout}>
                Odjava
              </button>
            ) : (
              <>
                <NavLink to="/publisher/login">Prijava izdavača</NavLink>
                <NavLink to="/publisher/register" className="btn header-cta">
                  Postavi oglas
                </NavLink>
              </>
            )}
          </nav>
        </div>
      </header>
      {children}
      <footer className="site-footer">
        <div className="container">
          RentList je oglasnik. Ne naplaćujemo najam, ne rezervišemo vozila i ne procesiramo plaćanja.
          Korisnik šalje upit, a izdavač dogovara detalje direktno.
        </div>
      </footer>
    </>
  );
}
