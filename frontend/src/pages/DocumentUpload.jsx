import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  FormControl,
  InputLabel,
  LinearProgress,
  MenuItem,
  Select,
  Typography,
} from "@mui/material";

import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import DescriptionIcon from "@mui/icons-material/Description";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import RefreshIcon from "@mui/icons-material/Refresh";

import DashboardLayout from "../layouts/DashboardLayout";
import { uploadDocument } from "../api/documentApi";
import { getSessions } from "../api/sessionApi";
import { useToast } from "../context/ToastContext";
import ErrorState from "../components/common/ErrorState";
import PageLoader from "../components/common/PageLoader";

const ALLOWED_TYPES = [".pdf", ".txt", ".docx"];
const MAX_FILE_SIZE_MB = 10;

function getFileExtension(filename) {
  return filename.substring(filename.lastIndexOf(".")).toLowerCase();
}

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

function DocumentUpload() {
  const { showToast } = useToast();
  const fileInputRef = useRef(null);

  const [sessions, setSessions] = useState([]);
  const [selectedSessionId, setSelectedSessionId] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);

  const [dragActive, setDragActive] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const [loadingSessions, setLoadingSessions] = useState(false);
  const [uploading, setUploading] = useState(false);

  const [successMessage, setSuccessMessage] = useState("");
  const [error, setError] = useState("");

  const loadSessions = async () => {
    try {
      setLoadingSessions(true);
      setError("");

      const data = await getSessions();
      const sessionList = normalizeList(data);

      setSessions(sessionList);
    } catch (error) {
      const message = getErrorMessage(error, "Failed to load chat sessions.");
      setError(message);
      showToast(message, "error");
    } finally {
      setLoadingSessions(false);
    }
  };

  useEffect(() => {
    loadSessions();
  }, []);

  const validateFile = (file) => {
    if (!file) return "Please select a file.";

    const extension = getFileExtension(file.name);

    if (!ALLOWED_TYPES.includes(extension)) {
      return "Invalid file type. Only PDF, TXT, and DOCX files are allowed.";
    }

    const fileSizeMB = file.size / (1024 * 1024);

    if (fileSizeMB > MAX_FILE_SIZE_MB) {
      return `File size must be less than ${MAX_FILE_SIZE_MB} MB.`;
    }

    return "";
  };

  const handleFileSelect = (file) => {
    setError("");
    setSuccessMessage("");

    const validationError = validateFile(file);

    if (validationError) {
      setSelectedFile(null);
      setError(validationError);
      showToast(validationError, "error");
      return;
    }

    setSelectedFile(file);
  };

  const handleInputChange = (event) => {
    const file = event.target.files?.[0];
    handleFileSelect(file);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    event.stopPropagation();

    setDragActive(false);

    const file = event.dataTransfer.files?.[0];
    handleFileSelect(file);
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setDragActive(true);
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setDragActive(false);
  };

  const handleUpload = async () => {
    setError("");
    setSuccessMessage("");

    if (!selectedSessionId) {
      const message = "Please select a chat session before uploading.";
      setError(message);
      showToast(message, "error");
      return;
    }

    const validationError = validateFile(selectedFile);

    if (validationError) {
      setError(validationError);
      showToast(validationError, "error");
      return;
    }

    try {
      setUploading(true);
      setUploadProgress(0);

      await uploadDocument(selectedFile, selectedSessionId, (progressEvent) => {
        if (!progressEvent.total) return;

        const percent = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );

        setUploadProgress(percent);
      });

      const message =
        "Document uploaded successfully. Backend will process and store chunks in ChromaDB.";

      setSuccessMessage(message);
      showToast("Document uploaded successfully.", "success");

      setSelectedFile(null);
      setUploadProgress(100);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    } catch (error) {
      const message = getErrorMessage(error, "Document upload failed.");
      setError(message);
      showToast(message, "error");
    } finally {
      setUploading(false);
    }
  };

  return (
    <DashboardLayout>
      <Box className="mb-6 flex flex-col justify-between gap-4 md:flex-row md:items-center">
        <div>
          <Typography variant="h4" className="font-extrabold">
            Upload Document
          </Typography>

          <Typography color="text.secondary" className="mt-1">
            Upload PDF, TXT, or DOCX files inside a selected chat session.
          </Typography>
        </div>

        <Button
          component={Link}
          to="/documents"
          variant="outlined"
          startIcon={<ArrowBackIcon />}
        >
          Back to Documents
        </Button>
      </Box>

      <Card>
        <CardContent className="p-6">
          {error && (
            <div className="mb-5">
              <ErrorState message={error} onRetry={loadSessions} />
            </div>
          )}

          {successMessage && (
            <Alert severity="success" className="mb-5">
              {successMessage}
            </Alert>
          )}

          {loadingSessions ? (
            <PageLoader message="Loading chat sessions..." />
          ) : (
            <>
              <FormControl fullWidth className="mb-6">
                <InputLabel>Select Chat Session</InputLabel>
                <Select
                  value={selectedSessionId}
                  label="Select Chat Session"
                  onChange={(event) => setSelectedSessionId(event.target.value)}
                  disabled={loadingSessions || uploading}
                >
                  {sessions.map((session) => (
                    <MenuItem key={session.id} value={session.id}>
                      {session.title || `Chat Session ${session.id}`}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              {sessions.length === 0 && (
                <Alert severity="warning" className="mb-6">
                  No chat session found. Please create a chat session first.
                </Alert>
              )}

              <Box
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onClick={() => fileInputRef.current?.click()}
                className={`cursor-pointer rounded-3xl border-2 border-dashed p-10 text-center transition ${
                  dragActive
                    ? "border-indigo-600 bg-indigo-50"
                    : "border-slate-300 bg-slate-50 hover:border-indigo-400 hover:bg-indigo-50"
                }`}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  hidden
                  accept=".pdf,.txt,.docx"
                  onChange={handleInputChange}
                />

                <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-3xl bg-indigo-100 text-indigo-600">
                  <CloudUploadIcon fontSize="large" />
                </div>

                <Typography variant="h6" className="font-bold">
                  Drag and drop your document here
                </Typography>

                <Typography color="text.secondary" className="mt-2">
                  or click to browse files from your computer
                </Typography>

                <div className="mt-4 flex justify-center gap-2">
                  {ALLOWED_TYPES.map((type) => (
                    <Chip
                      key={type}
                      label={type}
                      size="small"
                      variant="outlined"
                    />
                  ))}
                </div>

                <Typography
                  variant="caption"
                  color="text.secondary"
                  className="mt-4 block"
                >
                  Maximum file size: {MAX_FILE_SIZE_MB} MB
                </Typography>
              </Box>

              {selectedFile && (
                <Box className="mt-6 rounded-2xl border border-slate-200 p-4">
                  <div className="flex items-center gap-4">
                    <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-100 text-slate-600">
                      <DescriptionIcon />
                    </div>

                    <div className="flex-1">
                      <Typography className="font-semibold">
                        {selectedFile.name}
                      </Typography>

                      <Typography variant="body2" color="text.secondary">
                        {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
                      </Typography>
                    </div>

                    <CheckCircleIcon className="text-green-600" />
                  </div>
                </Box>
              )}

              {uploading && (
                <Box className="mt-6">
                  <div className="mb-2 flex justify-between">
                    <Typography variant="body2">Uploading...</Typography>
                    <Typography variant="body2">{uploadProgress}%</Typography>
                  </div>

                  <LinearProgress variant="determinate" value={uploadProgress} />
                </Box>
              )}

              <div className="mt-6 flex justify-between gap-3">
                <Button
                  variant="outlined"
                  startIcon={<RefreshIcon />}
                  onClick={loadSessions}
                  disabled={loadingSessions || uploading}
                >
                  Refresh Sessions
                </Button>

                <Button
                  variant="contained"
                  size="large"
                  startIcon={<CloudUploadIcon />}
                  onClick={handleUpload}
                  disabled={uploading || !selectedFile || !selectedSessionId}
                >
                  {uploading ? "Uploading..." : "Upload Document"}
                </Button>
              </div>
            </>
          )}
        </CardContent>
      </Card>
    </DashboardLayout>
  );
}

export default DocumentUpload;