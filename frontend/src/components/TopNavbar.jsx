import {
  Avatar,
  Box,
  Chip,
  IconButton,
  Tooltip,
  Typography,
} from "@mui/material";

import MenuIcon from "@mui/icons-material/Menu";
import NotificationsNoneIcon from "@mui/icons-material/NotificationsNone";

import { useAuth } from "../context/AuthContext";

function TopNavbar({ onMenuClick }) {
  const { currentUser, role } = useAuth();

  const displayName =
    currentUser?.name || currentUser?.full_name || currentUser?.email || "User";

  const avatarLetter = displayName?.[0]?.toUpperCase() || "U";

  return (
    <Box className="flex h-20 items-center justify-between border-b border-slate-200 bg-white px-6">
      <div className="flex items-center gap-4">
        <IconButton className="md:hidden" onClick={onMenuClick}>
          <MenuIcon />
        </IconButton>

        <div>
          <Typography variant="h6" className="font-bold">
            Dashboard
          </Typography>

          <Typography variant="body2" color="text.secondary">
            Manage chats, documents, and RAG answers
          </Typography>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <Tooltip title="Notifications">
          <IconButton>
            <NotificationsNoneIcon />
          </IconButton>
        </Tooltip>

        <Chip
          label={role || "user"}
          color={role === "admin" ? "error" : "primary"}
          variant="outlined"
          size="small"
        />

        <div className="hidden text-right sm:block">
          <Typography variant="body2" className="font-semibold">
            {displayName}
          </Typography>

          <Typography variant="caption" color="text.secondary">
            {currentUser?.email || "No email"}
          </Typography>
        </div>

        <Avatar className="bg-indigo-600">{avatarLetter}</Avatar>
      </div>
    </Box>
  );
}

export default TopNavbar;