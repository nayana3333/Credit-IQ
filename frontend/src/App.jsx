import { Suspense, lazy } from "react";
import { Navigate, Route, Routes } from "react-router-dom";

import AppLayout from "./components/layout/AppLayout";
import Login from "./pages/Login";
import Register from "./pages/Register";

const Assistant = lazy(() => import("./pages/Assistant"));
const Analytics = lazy(() => import("./pages/Analytics"));
const Applications = lazy(() => import("./pages/Applications"));
const BatchPredict = lazy(() => import("./pages/BatchPredict"));
const Dashboard = lazy(() => import("./pages/Dashboard"));
const LoanDecision = lazy(() => import("./pages/LoanDecision"));
const LoanForm = lazy(() => import("./pages/LoanForm"));
const Profile = lazy(() => import("./pages/Profile"));
const Simulation = lazy(() => import("./pages/Simulation"));

function RouteFallback() {
  return <div className="p-6 text-[13px] text-[#737373]">Loading...</div>;
}

function Protected({ children }) {
  if (!localStorage.getItem("token")) {
    return <Navigate to="/login" replace />;
  }

  return (
    <AppLayout>
      <Suspense fallback={<RouteFallback />}>{children}</Suspense>
    </AppLayout>
  );
}

export default function App() {
  const fallback = localStorage.getItem("token") ? "/dashboard" : "/login";

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/" element={<Navigate to={fallback} replace />} />
      <Route path="/dashboard" element={<Protected><Dashboard /></Protected>} />
      <Route path="/applications" element={<Protected><Applications /></Protected>} />
      <Route path="/loans" element={<Protected><Applications /></Protected>} />
      <Route path="/applications/new" element={<Protected><LoanForm /></Protected>} />
      <Route path="/loans/new" element={<Protected><LoanForm /></Protected>} />
      <Route path="/applications/:id" element={<Protected><LoanDecision /></Protected>} />
      <Route path="/loans/:id" element={<Protected><LoanDecision /></Protected>} />
      <Route path="/analytics" element={<Protected><Analytics /></Protected>} />
      <Route path="/simulation" element={<Protected><Simulation /></Protected>} />
      <Route path="/assistant" element={<Protected><Assistant /></Protected>} />
      <Route path="/batch" element={<Protected><BatchPredict /></Protected>} />
      <Route path="/profile" element={<Protected><Profile /></Protected>} />
      <Route path="*" element={<Navigate to={fallback} replace />} />
    </Routes>
  );
}
