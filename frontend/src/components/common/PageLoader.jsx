import { Box, CircularProgress, Typography } from "@mui/material";

function PageLoader({ message = "Loading..." }) {
  return (
    <Box className="flex min-h-80 flex-col items-center justify-center gap-4">
      <CircularProgress />
      <Typography color="text.secondary">{message}</Typography>
    </Box>
  );
}

export default PageLoader;