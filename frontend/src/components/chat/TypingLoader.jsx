import { Avatar, Box, CircularProgress, Typography } from "@mui/material";
import SmartToyIcon from "@mui/icons-material/SmartToy";

function TypingLoader() {
  return (
    <Box className="mb-5 flex justify-start">
      <div className="flex items-start gap-3">
        <Avatar className="bg-cyan-600">
          <SmartToyIcon />
        </Avatar>

        <div className="flex items-center gap-3 rounded-3xl rounded-tl-md bg-white px-5 py-3 shadow-sm ring-1 ring-slate-200">
          <CircularProgress size={18} />
          <Typography color="text.secondary">AI is thinking...</Typography>
        </div>
      </div>
    </Box>
  );
}

export default TypingLoader;