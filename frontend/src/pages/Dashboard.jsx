import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  LinearProgress,
  Typography,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import DescriptionIcon from "@mui/icons-material/Description";
import ChatIcon from "@mui/icons-material/Chat";
import HistoryIcon from "@mui/icons-material/History";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import RefreshIcon from "@mui/icons-material/Refresh";

import DashboardLayout from "../layouts/DashboardLayout";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";

import { getDocuments } from "../api/documentApi";
import { getSessions } from "../api/sessionApi";
import { getAllHistory } from "../api/historyApi";

import ErrorState from "../components/common/ErrorState";
import StatCardSkeleton from "../components/common/StatCardSkeleton";
import EmptyState from "../components/common/EmptyState";

function normalizeList(data) {
  if (Array.isArray(data)) return data;
  return data?.items || data?.data || data?.results || [];
}

function getErrorMessage(error, fallbackMessage) {
  return (
    error.response?.data?.detail ||
    error.response?.data?.message ||
    fallbackMessage
  );
}

function StatCard({ title, value, icon, description }) {
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

          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-indigo-50 text-indigo-600">
            {icon}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function RecentChatItem({ title, message, time, status }) {
  return (
    <div className="flex items-start justify-between gap-4 rounded-2xl border border-slate-200 p-4 hover:bg-slate-50">
      <div className="min-w-0 flex-1">
        <Typography className="truncate font-semibold">{title}</Typography>

        <Typography
          variant="body2"
          color="text.secondary"
          className="mt-1 line-clamp-2"
        >
          {message}
        </Typography>

        <Typography
          variant="caption"
          color="text.secondary"
          className="mt-2 block"
        >
          {time}
        </Typography>
      </div>

      <Chip label={status} size="small" color="primary" variant="outlined" />
    </div>
  );
}

function Dashboard() {
  const { currentUser } = useAuth();
  const { showToast } = useToast();

  const displayName =
    currentUser?.name || currentUser?.full_name || currentUser?.email || "User";

  const [stats, setStats] = useState({
    documents: 0,
    sessions: 0,
    history: 0,
  });

  const [recentHistory, setRecentHistory] = useState([]);

  const [loadingStats, setLoadingStats] = useState(false);
  const [statsError, setStatsError] = useState("");

  const loadDashboardStats = async () => {
    try {
      setLoadingStats(true);
      setStatsError("");

      const [documentsData, sessionsData, historyData] = await Promise.all([
        getDocuments(),
        getSessions(),
        getAllHistory(),
      ]);

      const documentsList = normalizeList(documentsData);
      const sessionsList = normalizeList(sessionsData);
      const historyList = normalizeList(historyData);

      setStats({
        documents: documentsList.length,
        sessions: sessionsList.length,
        history: historyList.length,
      });

      setRecentHistory(historyList.slice(0, 5));
    } catch (error) {
      const message = getErrorMessage(error, "Failed to load dashboard data.");

      setStatsError(message);
      showToast(message, "error");
    } finally {
      setLoadingStats(false);
    }
  };

  useEffect(() => {
    loadDashboardStats();
  }, []);

  return (
    <DashboardLayout>
      <Box className="mb-8 flex flex-col justify-between gap-4 md:flex-row md:items-center">
        <div>
          <Typography variant="h4" className="font-extrabold">
            Welcome back, {displayName}
          </Typography>

          <Typography color="text.secondary" className="mt-1">
            Upload documents, create isolated chat sessions, and ask secure RAG
            questions.
          </Typography>
        </div>

        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={loadDashboardStats}
          disabled={loadingStats}
        >
          Retry / Refresh
        </Button>
      </Box>

      {statsError && (
        <div className="mb-6">
          <ErrorState message={statsError} onRetry={loadDashboardStats} />
        </div>
      )}

      <div className="mb-8 flex flex-col gap-3 sm:flex-row">
        <Button
          component={Link}
          to="/chats"
          variant="contained"
          startIcon={<AddIcon />}
        >
          Start New Chat
        </Button>

        <Button
          component={Link}
          to="/documents/upload"
          variant="outlined"
          startIcon={<UploadFileIcon />}
        >
          Upload Document
        </Button>
      </div>

      {loadingStats ? (
        <div className="grid gap-6 md:grid-cols-3">
          <StatCardSkeleton />
          <StatCardSkeleton />
          <StatCardSkeleton />
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-3">
          <StatCard
            title="Total Documents"
            value={stats.documents}
            description="Documents uploaded by you"
            icon={<DescriptionIcon />}
          />

          <StatCard
            title="Total Sessions"
            value={stats.sessions}
            description="Your isolated chat sessions"
            icon={<ChatIcon />}
          />

          <StatCard
            title="Recent Chats"
            value={stats.history}
            description="Recent questions asked"
            icon={<HistoryIcon />}
          />
        </div>
      )}

      <div className="mt-6 grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <Card>
            <CardContent className="p-6">
              <div className="mb-5 flex items-center justify-between gap-4">
                <div>
                  <Typography variant="h6" className="font-bold">
                    Recent Chats
                  </Typography>

                  <Typography color="text.secondary" variant="body2">
                    Your latest document question-answer activity.
                  </Typography>
                </div>

                <Button component={Link} to="/history" size="small">
                  View All
                </Button>
              </div>

              {loadingStats ? (
                <div className="space-y-4">
                  <div className="h-20 animate-pulse rounded-2xl bg-slate-100" />
                  <div className="h-20 animate-pulse rounded-2xl bg-slate-100" />
                  <div className="h-20 animate-pulse rounded-2xl bg-slate-100" />
                </div>
              ) : recentHistory.length === 0 ? (
                <EmptyState
                  icon={<HistoryIcon fontSize="large" />}
                  title="No recent chat yet"
                  description="Start a chat and ask questions from your uploaded documents. Recent messages will appear here."
                  actionLabel="Start First Chat"
                  actionTo="/chats"
                  component={Link}
                />
              ) : (
                <div className="space-y-4">
                  {recentHistory.map((item, index) => {
                    const title =
                      item.session_title ||
                      item.title ||
                      `Session ${item.session_id || item.id || index + 1}`;

                    const message =
                      item.question ||
                      item.content ||
                      item.message ||
                      item.answer ||
                      "Chat message";

                    const time = item.created_at
                      ? new Date(item.created_at).toLocaleString("en-IN", {
                          dateStyle: "medium",
                          timeStyle: "short",
                        })
                      : "N/A";

                    return (
                      <RecentChatItem
                        key={item.id || index}
                        title={title}
                        message={message}
                        time={time}
                        status="Recent"
                      />
                    );
                  })}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        <div>
          <Card>
            <CardContent className="p-6">
              <div className="mb-4 flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-cyan-50 text-cyan-600">
                  <TrendingUpIcon />
                </div>

                <div>
                  <Typography variant="h6" className="font-bold">
                    Usage
                  </Typography>

                  <Typography variant="body2" color="text.secondary">
                    Current project status
                  </Typography>
                </div>
              </div>

              <div className="space-y-5">
                <div>
                  <div className="mb-2 flex justify-between">
                    <Typography variant="body2">Documents</Typography>
                    <Typography variant="body2">{stats.documents}</Typography>
                  </div>

                  <LinearProgress
                    variant="determinate"
                    value={Math.min(stats.documents * 10, 100)}
                  />
                </div>

                <div>
                  <div className="mb-2 flex justify-between">
                    <Typography variant="body2">Sessions</Typography>
                    <Typography variant="body2">{stats.sessions}</Typography>
                  </div>

                  <LinearProgress
                    variant="determinate"
                    value={Math.min(stats.sessions * 10, 100)}
                  />
                </div>

                <div>
                  <div className="mb-2 flex justify-between">
                    <Typography variant="body2">Chat Activity</Typography>
                    <Typography variant="body2">{stats.history}</Typography>
                  </div>

                  <LinearProgress
                    variant="determinate"
                    value={Math.min(stats.history * 5, 100)}
                  />
                </div>
              </div>

              <div className="mt-6 rounded-2xl bg-indigo-50 p-4">
                <Typography className="font-semibold text-indigo-700">
                  User Isolation Active
                </Typography>

                <Typography variant="body2" className="mt-1 text-indigo-700">
                  This dashboard displays only data returned from your
                  authenticated backend APIs.
                </Typography>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </DashboardLayout>
  );
}

export default Dashboard;