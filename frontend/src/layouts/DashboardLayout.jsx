import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Box, Drawer } from "@mui/material";

import Sidebar from "../components/Sidebar";
import TopNavbar from "../components/TopNavbar";
import { useAuth } from "../context/AuthContext";

function DashboardLayout({ children }) {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const [mobileOpen, setMobileOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
    navigate("/login", { replace: true });
  };

  const handleDrawerToggle = () => {
    setMobileOpen((prev) => !prev);
  };

  return (
    <Box className="flex min-h-screen bg-slate-50">
      {/* Desktop Sidebar */}
      <Box className="hidden md:block">
        <Sidebar onLogout={handleLogout} />
      </Box>

      {/* Mobile Sidebar */}
      <Drawer
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true,
        }}
        className="md:hidden"
      >
        <Sidebar onLogout={handleLogout} />
      </Drawer>

      {/* Main Area */}
      <Box className="flex min-h-screen flex-1 flex-col">
        <TopNavbar onMenuClick={handleDrawerToggle} />

        <main className="flex-1 p-5 md:p-8">{children}</main>
      </Box>
    </Box>
  );
}

export default DashboardLayout;