import { Navigate, Route, Routes } from "react-router-dom";
import Guard from "./components/Guard";
import AdminLayout from "./layouts/AdminLayout";
import PublicLayout from "./layouts/PublicLayout";
import PublisherLayout from "./layouts/PublisherLayout";
import Home from "./pages/Home";
import SearchResults from "./pages/SearchResults";
import CarDetails from "./pages/CarDetails";
import InquiryForm from "./pages/InquiryForm";
import PublisherProfile from "./pages/PublisherProfile";
import PublisherLogin from "./pages/publisher/PublisherLogin";
import PublisherRegister from "./pages/publisher/PublisherRegister";
import PublisherDashboard from "./pages/publisher/PublisherDashboard";
import PublisherCars from "./pages/publisher/PublisherCars";
import PublisherCarForm from "./pages/publisher/PublisherCarForm";
import PublisherCarCalendar from "./pages/publisher/PublisherCarCalendar";
import PublisherInquiries from "./pages/publisher/PublisherInquiries";
import PublisherInquiryDetails from "./pages/publisher/PublisherInquiryDetails";
import PublisherProfileEdit from "./pages/publisher/PublisherProfileEdit";
import AdminDashboard from "./pages/admin/AdminDashboard";
import AdminPublishers from "./pages/admin/AdminPublishers";
import AdminCars from "./pages/admin/AdminCars";
import AdminInquiries from "./pages/admin/AdminInquiries";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<PublicLayout><Home /></PublicLayout>} />
      <Route path="/search" element={<PublicLayout><SearchResults /></PublicLayout>} />
      <Route path="/cars/:id" element={<PublicLayout><CarDetails /></PublicLayout>} />
      <Route path="/cars/:id/inquiry" element={<PublicLayout><InquiryForm /></PublicLayout>} />
      <Route path="/publishers/:id" element={<PublicLayout><PublisherProfile /></PublicLayout>} />
      <Route path="/publisher/login" element={<PublicLayout><PublisherLogin /></PublicLayout>} />
      <Route path="/publisher/register" element={<PublicLayout><PublisherRegister /></PublicLayout>} />
      <Route
        path="/publisher"
        element={<Guard role="PUBLISHER"><PublisherLayout><PublisherDashboard /></PublisherLayout></Guard>}
      />
      <Route
        path="/publisher/cars"
        element={<Guard role="PUBLISHER"><PublisherLayout><PublisherCars /></PublisherLayout></Guard>}
      />
      <Route
        path="/publisher/cars/new"
        element={<Guard role="PUBLISHER"><PublisherLayout><PublisherCarForm mode="create" /></PublisherLayout></Guard>}
      />
      <Route
        path="/publisher/cars/:id/edit"
        element={<Guard role="PUBLISHER"><PublisherLayout><PublisherCarForm mode="edit" /></PublisherLayout></Guard>}
      />
      <Route
        path="/publisher/cars/:id/calendar"
        element={<Guard role="PUBLISHER"><PublisherLayout><PublisherCarCalendar /></PublisherLayout></Guard>}
      />
      <Route
        path="/publisher/inquiries"
        element={<Guard role="PUBLISHER"><PublisherLayout><PublisherInquiries /></PublisherLayout></Guard>}
      />
      <Route
        path="/publisher/inquiries/:id"
        element={<Guard role="PUBLISHER"><PublisherLayout><PublisherInquiryDetails /></PublisherLayout></Guard>}
      />
      <Route
        path="/publisher/profile"
        element={<Guard role="PUBLISHER"><PublisherLayout><PublisherProfileEdit /></PublisherLayout></Guard>}
      />
      <Route path="/admin/login" element={<Navigate to="/publisher/login" replace />} />
      <Route path="/admin" element={<Guard role="ADMIN"><AdminLayout><AdminDashboard /></AdminLayout></Guard>} />
      <Route path="/admin/publishers" element={<Guard role="ADMIN"><AdminLayout><AdminPublishers /></AdminLayout></Guard>} />
      <Route path="/admin/cars" element={<Guard role="ADMIN"><AdminLayout><AdminCars /></AdminLayout></Guard>} />
      <Route path="/admin/inquiries" element={<Guard role="ADMIN"><AdminLayout><AdminInquiries /></AdminLayout></Guard>} />
    </Routes>
  );
}
