import { Link, useLocation } from "react-router-dom";
import {
  Box,
  Button,
  Divider,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
} from "@mui/material";

import DashboardIcon from "@mui/icons-material/Dashboard";
import ChatIcon from "@mui/icons-material/Chat";
import DescriptionIcon from "@mui/icons-material/Description";
import HistoryIcon from "@mui/icons-material/History";
import AdminPanelSettingsIcon from "@mui/icons-material/AdminPanelSettings";
import LogoutIcon from "@mui/icons-material/Logout";

import { useAuth } from "../context/AuthContext";

function Sidebar({ onLogout }) {
  const location = useLocation();
  const { role } = useAuth();

  const menuItems = [
    {
      label: "Dashboard",
      path: "/dashboard",
      icon: <DashboardIcon />,
      roles: ["user", "admin"],
    },
    {
      label: "Chats",
      path: "/chats",
      icon: <ChatIcon />,
      roles: ["user", "admin"],
    },
    {
      label: "Documents",
      path: "/documents",
      icon: <DescriptionIcon />,
      roles: ["user", "admin"],
    },
    // {
    //   label: "History",
    //   path: "/history",
    //   icon: <HistoryIcon />,
    //   roles: ["user", "admin"],
    // },
    {
      label: "Admin",
      path: "/admin",
      icon: <AdminPanelSettingsIcon />,
      roles: ["admin"],
    },
  ];

  const visibleMenuItems = menuItems.filter((item) =>
    item.roles.includes(role || "user"),
  );

  return (
    <Box className="flex h-full w-72 flex-col border-r border-slate-200 bg-white">
      <div className="p-6">
        <Typography variant="h5" className="font-extrabold text-indigo-600">
          RAG Assistant
        </Typography>

        <Typography variant="body2" color="text.secondary" className="mt-1">
          Secure document chat
        </Typography>
      </div>

      <Divider />

      <List className="flex-1 px-3 py-4">
        {visibleMenuItems.map((item) => {
          const isActive = location.pathname === item.path;

          return (
            <ListItemButton
              key={item.path}
              component={Link}
              to={item.path}
              className={`mb-2 rounded-xl ${
                isActive
                  ? "bg-indigo-50 text-indigo-700"
                  : "text-slate-600 hover:bg-slate-100"
              }`}
            >
              <ListItemIcon
                className={isActive ? "text-indigo-700" : "text-slate-500"}
              >
                {item.icon}
              </ListItemIcon>

              <ListItemText
                primary={
                  <Typography
                    component="span"
                    className={isActive ? "font-bold" : "font-medium"}
                  >
                    {item.label}
                  </Typography>
                }
              />
            </ListItemButton>
          );
        })}
      </List>

      <div className="p-4">
        <Button
          fullWidth
          variant="outlined"
          color="error"
          startIcon={<LogoutIcon />}
          onClick={onLogout}
        >
          Logout
        </Button>
      </div>
    </Box>
  );
}

export default Sidebar;
