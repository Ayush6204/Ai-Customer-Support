import { Card, CardContent, Typography } from "@mui/material";
import DashboardLayout from "../layouts/DashboardLayout";

function ComingSoon({ title }) {
  return (
    <DashboardLayout>
      <Card>
        <CardContent className="p-8">
          <Typography variant="h5" className="font-bold">
            {title}
          </Typography>

          <Typography color="text.secondary" className="mt-2">
            This page will be completed in the upcoming frontend phase.
          </Typography>
        </CardContent>
      </Card>
    </DashboardLayout>
  );
}

export default ComingSoon;