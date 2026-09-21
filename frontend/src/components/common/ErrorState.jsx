import { Alert, Box, Button } from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";

function ErrorState({ message = "Something went wrong.", onRetry }) {
  return (
    <Box className="rounded-2xl border border-red-100 bg-red-50 p-5">
      <Alert
        severity="error"
        action={
          onRetry ? (
            <Button
              color="inherit"
              size="small"
              startIcon={<RefreshIcon />}
              onClick={onRetry}
            >
              Retry
            </Button>
          ) : null
        }
      >
        {message}
      </Alert>
    </Box>
  );
}

export default ErrorState;