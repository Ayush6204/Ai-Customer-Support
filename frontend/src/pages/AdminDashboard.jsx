import {
  Box,
  Card,
  CardContent,
  Chip,
  Grid,
  LinearProgress,
  Typography,
} from "@mui/material";

import PeopleAltIcon from "@mui/icons-material/PeopleAlt";
import DescriptionIcon from "@mui/icons-material/Description";
import StorageIcon from "@mui/icons-material/Storage";
import TimelineIcon from "@mui/icons-material/Timeline";
import AdminPanelSettingsIcon from "@mui/icons-material/AdminPanelSettings";

import DashboardLayout from "../layouts/DashboardLayout";

function AdminStatCard({ title, value, icon, description, color = "primary" }) {
  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-start justify-between gap-4">
          <div>
            <Typography color="text.secondary" variant="body2">
              {title}
            </Typography>

            <Typography variant="h4" className="mt-2 font-extrabold">
              {value}
            </Typography>

            <Typography color="text.secondary" variant="body2" className="mt-2">
              {description}
            </Typography>
          </div>

          <div
            className={`flex h-12 w-12 items-center justify-center rounded-2xl ${
              color === "error"
                ? "bg-red-50 text-red-600"
                : color === "success"
                ? "bg-green-50 text-green-600"
                : color === "warning"
                ? "bg-orange-50 text-orange-600"
                : "bg-indigo-50 text-indigo-600"
            }`}
          >
            {icon}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function ActivityItem({ title, description, time, type }) {
  return (
    <div className="flex items-start justify-between gap-4 rounded-2xl border border-slate-200 p-4 hover:bg-slate-50">
      <div>
        <Typography className="font-semibold">{title}</Typography>

        <Typography variant="body2" color="text.secondary" className="mt-1">
          {description}
        </Typography>

        <Typography variant="caption" color="text.secondary" className="mt-2 block">
          {time}
        </Typography>
      </div>

      <Chip label={type} size="small" variant="outlined" />
    </div>
  );
}

function AdminDashboard() {
  return (
    <DashboardLayout>
      <Box className="mb-8">
        <div className="flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-red-50 text-red-600">
            <AdminPanelSettingsIcon />
          </div>

          <div>
            <Typography variant="h4" className="font-extrabold">
              Admin Dashboard
            </Typography>

            <Typography color="text.secondary" className="mt-1">
              Monitor users, documents, system usage, and recent activity.
            </Typography>
          </div>
        </div>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <AdminStatCard
            title="Total Users"
            value="0"
            description="Registered users"
            icon={<PeopleAltIcon />}
          />
        </Grid>

        <Grid item xs={12} md={3}>
          <AdminStatCard
            title="Total Documents"
            value="0"
            description="Uploaded documents"
            icon={<DescriptionIcon />}
            color="success"
          />
        </Grid>

        <Grid item xs={12} md={3}>
          <AdminStatCard
            title="Vector Storage"
            value="0"
            description="Stored document chunks"
            icon={<StorageIcon />}
            color="warning"
          />
        </Grid>

        <Grid item xs={12} md={3}>
          <AdminStatCard
            title="System Usage"
            value="0%"
            description="Current usage level"
            icon={<TimelineIcon />}
            color="error"
          />
        </Grid>
      </Grid>

      <Grid container spacing={3} className="mt-1">
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent className="p-6">
              <Typography variant="h6" className="font-bold">
                Recent Activity
              </Typography>

              <Typography color="text.secondary" variant="body2" className="mt-1">
                Latest system events and user actions.
              </Typography>

              <div className="mt-5 space-y-4">
                <ActivityItem
                  title="No activity yet"
                  description="Admin activity logs will appear here after backend integration."
                  time="Waiting for data"
                  type="Empty"
                />
              </div>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent className="p-6">
              <Typography variant="h6" className="font-bold">
                System Usage
              </Typography>

              <Typography color="text.secondary" variant="body2" className="mt-1">
                Storage and usage overview.
              </Typography>

              <div className="mt-6 space-y-5">
                <div>
                  <div className="mb-2 flex justify-between">
                    <Typography variant="body2">Users</Typography>
                    <Typography variant="body2">0%</Typography>
                  </div>
                  <LinearProgress variant="determinate" value={0} />
                </div>

                <div>
                  <div className="mb-2 flex justify-between">
                    <Typography variant="body2">Documents</Typography>
                    <Typography variant="body2">0%</Typography>
                  </div>
                  <LinearProgress variant="determinate" value={0} />
                </div>

                <div>
                  <div className="mb-2 flex justify-between">
                    <Typography variant="body2">ChromaDB</Typography>
                    <Typography variant="body2">0%</Typography>
                  </div>
                  <LinearProgress variant="determinate" value={0} />
                </div>

                <div>
                  <div className="mb-2 flex justify-between">
                    <Typography variant="body2">LLM Requests</Typography>
                    <Typography variant="body2">0%</Typography>
                  </div>
                  <LinearProgress variant="determinate" value={0} />
                </div>
              </div>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </DashboardLayout>
  );
}

export default AdminDashboard;