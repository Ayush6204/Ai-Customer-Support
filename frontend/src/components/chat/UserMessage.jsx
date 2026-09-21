import { Avatar, Box, Typography } from "@mui/material";
import PersonIcon from "@mui/icons-material/Person";

function UserMessage({ message }) {
  return (
    <Box className="mb-5 flex justify-end">
      <div className="flex max-w-3xl items-start gap-3">
        <div className="rounded-3xl rounded-tr-md bg-indigo-600 px-5 py-3 text-white shadow-sm">
          <Typography className="whitespace-pre-wrap">
            {message.content || message.question || message.text}
          </Typography>
        </div>

        <Avatar className="bg-indigo-600">
          <PersonIcon />
        </Avatar>
      </div>
    </Box>
  );
}

export default UserMessage;