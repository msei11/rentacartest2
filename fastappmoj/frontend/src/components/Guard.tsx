import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Guard({ role, children }: { role: string; children: React.ReactNode }) {
  const { user, loading } = useAuth();
  if (loading) return <p className="container section">Učitavanje...</p>;
  if (!user) return <Navigate to="/publisher/login" replace />;
  if (user.role !== role) return <Navigate to="/" replace />;
  return <>{children}</>;
}
