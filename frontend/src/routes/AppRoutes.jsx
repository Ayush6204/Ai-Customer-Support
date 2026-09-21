import { Routes, Route } from "react-router-dom";

import Home from "../pages/Home";
import Login from "../pages/Login";
import Register from "../pages/Register";
import Dashboard from "../pages/Dashboard";
import AdminDashboard from "../pages/AdminDashboard";
import ComingSoon from "../pages/ComingSoon";
import AccessDenied from "../pages/AccessDenied";

import Documents from "../pages/Documents";
import DocumentUpload from "../pages/DocumentUpload";
import DocumentDetail from "../pages/DocumentDetail";
import Chat from "../pages/Chat";

import ProtectedRoute from "../auth/ProtectedRoute";
import RoleBasedRoute from "../auth/RoleBasedRoute";

function AppRoutes({ mode, toggleTheme }) {
  return (
    <Routes>
      <Route
        path="/"
        element={<Home mode={mode} toggleTheme={toggleTheme} />}
      />

      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/access-denied" element={<AccessDenied />} />

      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/chats"
        element={
          <ProtectedRoute>
            <Chat />
          </ProtectedRoute>
        }
      />

      <Route
        path="/documents"
        element={
          <ProtectedRoute>
            <Documents />
          </ProtectedRoute>
        }
      />

      <Route
        path="/documents/upload"
        element={
          <ProtectedRoute>
            <DocumentUpload />
          </ProtectedRoute>
        }
      />

      <Route
        path="/documents/:documentId"
        element={
          <ProtectedRoute>
            <DocumentDetail />
          </ProtectedRoute>
        }
      />

      <Route
        path="/history"
        element={
          <ProtectedRoute>
            <ComingSoon title="History" />
          </ProtectedRoute>
        }
      />

      <Route
        path="/admin"
        element={
          <RoleBasedRoute allowedRoles={["admin"]}>
            <AdminDashboard />
          </RoleBasedRoute>
        }
      />
    </Routes>
  );
}

export default AppRoutes;