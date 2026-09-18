import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const links = [
  ["/admin", "Pregled"],
  ["/admin/publishers", "Izdavači"],
  ["/admin/cars", "Vozila"],
  ["/admin/inquiries", "Upiti"],
];

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const { logout } = useAuth();
  const navigate = useNavigate();
  return (
    <div className="dash">
      <aside className="side">
        <div className="logo" style={{ marginBottom: 18 }}>
          ADMIN
        </div>
        {links.map(([to, label]) => (
          <NavLink key={to} to={to} end={to === "/admin"}>
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
