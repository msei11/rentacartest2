import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const links = [
  ["/publisher", "Dashboard"],
  ["/publisher/cars", "Moja vozila"],
  ["/publisher/cars/new", "Dodaj vozilo"],
  ["/publisher/inquiries", "Upiti"],
  ["/publisher/profile", "Profil"],
];

export default function PublisherLayout({ children }: { children: React.ReactNode }) {
  const { logout } = useAuth();
  const navigate = useNavigate();
  return (
    <div className="dash">
      <aside className="side">
        <div className="logo" style={{ marginBottom: 18 }}>
          RENT<span>LIST</span>
        </div>
        {links.map(([to, label]) => (
          <NavLink key={to} to={to} end={to === "/publisher"}>
            {label}
          </NavLink>
        ))}
        <NavLink to="/">Javni sajt</NavLink>
        <button
          onClick={() => {
            logout();
            navigate("/");
          }}
        >
          Logout
        </button>
      </aside>
      <div className="dash-main">{children}</div>
    </div>
  );
}
