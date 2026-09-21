import { Link } from "react-router-dom";
import { Box, Button, Card, CardContent, Container, Typography } from "@mui/material";
import BlockIcon from "@mui/icons-material/Block";
import DashboardIcon from "@mui/icons-material/Dashboard";

function AccessDenied() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Container maxWidth="sm">
        <Box className="flex min-h-screen items-center justify-center">
          <Card className="w-full">
            <CardContent className="p-10 text-center">
              <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-3xl bg-red-100 text-red-600">
                <BlockIcon fontSize="large" />
              </div>

              <Typography variant="h4" className="font-extrabold">
                Access Denied
              </Typography>

              <Typography color="text.secondary" className="mt-3">
                You do not have permission to access this page or resource.
              </Typography>

              <Button
                component={Link}
                to="/dashboard"
                variant="contained"
                className="mt-6"
                startIcon={<DashboardIcon />}
              >
                Back to Dashboard
              </Button>
            </CardContent>
          </Card>
        </Box>
      </Container>
    </div>
  );
}

export default AccessDenied;