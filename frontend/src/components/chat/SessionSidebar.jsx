import { useState } from "react";
import {
  Box,
  Button,
  Divider,
  IconButton,
  Tooltip,
  Typography,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";
import SearchIcon from "@mui/icons-material/Search";
import ChatIcon from "@mui/icons-material/Chat";

function SessionSidebar({
  sessions,
  activeSessionId,
  onSelectSession,
  onCreateSession,
  onDeleteSession,
}) {
  const [searchTerm, setSearchTerm] = useState("");

  const filteredSessions = sessions.filter((session) =>
    (session.title || `Chat ${session.id}`)
      .toLowerCase()
      .includes(searchTerm.toLowerCase()),
  );

  const formatSessionDate = (dateString) => {
    if (!dateString) return "Recently created";
    try {
      const date = new Date(dateString);
      const today = new Date();
      const yesterday = new Date(today);
      yesterday.setDate(yesterday.getDate() - 1);

      if (date.toDateString() === today.toDateString()) {
        return date.toLocaleTimeString("en-IN", {
          hour: "2-digit",
          minute: "2-digit",
        });
      } else if (date.toDateString() === yesterday.toDateString()) {
        return "Yesterday";
      } else {
        return date.toLocaleDateString("en-IN", {
          month: "short",
          day: "numeric",
        });
      }
    } catch {
      return "Recently created";
    }
  };

  return (
    <Box className="flex h-full w-80 flex-col border-r border-slate-200 bg-white">
      <div className="p-4">
        <Button
          fullWidth
          variant="contained"
          startIcon={<AddIcon />}
          onClick={onCreateSession}
        >
          New Chat
        </Button>

        <div className="relative mt-4">
          <SearchIcon
            fontSize="small"
            className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
          />

          <input
            type="text"
            placeholder="Search chats..."
            value={searchTerm}
            onChange={(event) => setSearchTerm(event.target.value)}
            className="w-full rounded-xl border border-slate-300 bg-white py-2 pl-10 pr-3 text-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
          />
        </div>
      </div>

      <Divider />

      <div className="flex-1 overflow-y-auto p-3">
        {filteredSessions.length === 0 ? (
          <div className="p-4 text-center">
            <Typography variant="body2" color="text.secondary">
              {searchTerm ? "No chats found." : "No chat sessions yet."}
            </Typography>
          </div>
        ) : (
          filteredSessions.map((session) => {
            const isActive = Number(activeSessionId) === Number(session.id);
            const sessionDate = formatSessionDate(session.created_at || session.updated_at);

            return (
              <div
                key={session.id}
                className={`mb-2 flex cursor-pointer items-center gap-3 rounded-2xl p-3 transition ${
                  isActive
                    ? "bg-indigo-50 text-indigo-700"
                    : "hover:bg-slate-50"
                }`}
                onClick={() => onSelectSession(session.id)}
              >
                <div
                  className={`flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-xl ${
                    isActive
                      ? "bg-indigo-100 text-indigo-700"
                      : "bg-slate-100 text-slate-600"
                  }`}
                >
                  <ChatIcon fontSize="small" />
                </div>

                <div className="min-w-0 flex-1">
                  <Typography className="truncate font-semibold">
                    {session.title || `Chat ${session.id}`}
                  </Typography>

                  <Typography
                    variant="caption"
                    color="text.secondary"
                    className="block truncate"
                  >
                    {sessionDate}
                  </Typography>
                </div>

                <Tooltip title="Delete session">
                  <IconButton
                    size="small"
                    color="error"
                    onClick={(event) => {
                      event.stopPropagation();
                      onDeleteSession(session.id);
                    }}
                    className="flex-shrink-0"
                  >
                    <DeleteIcon fontSize="small" />
                  </IconButton>
                </Tooltip>
              </div>
            );
          })
        )}
      </div>
    </Box>
  );
}

export default SessionSidebar;
