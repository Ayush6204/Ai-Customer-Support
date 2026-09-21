import { Avatar, Box, Typography } from "@mui/material";
import SmartToyIcon from "@mui/icons-material/SmartToy";

function AIMessage({ message }) {
  const answer = message.content || message.answer || message.text;

  return (
    <Box className="mb-5 flex justify-start">
      <div className="flex max-w-4xl items-start gap-3">
        <Avatar className="bg-cyan-600">
          <SmartToyIcon />
        </Avatar>

        <div>
          <div className="rounded-3xl rounded-tl-md bg-white px-5 py-3 shadow-sm ring-1 ring-slate-200">
            <Typography className="whitespace-pre-wrap text-slate-800">
              {answer}
            </Typography>
          </div>
        </div>
      </div>
    </Box>
  );
}

export default AIMessage;