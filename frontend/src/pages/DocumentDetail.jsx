import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  Grid,
  Typography,
} from "@mui/material";

import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import QuestionAnswerIcon from "@mui/icons-material/QuestionAnswer";
import RefreshIcon from "@mui/icons-material/Refresh";
import DescriptionIcon from "@mui/icons-material/Description";
import StorageIcon from "@mui/icons-material/Storage";
import ChatIcon from "@mui/icons-material/Chat";

import DashboardLayout from "../layouts/DashboardLayout";
import { getDocumentById, reprocessDocument } from "../api/documentApi";
import PageLoader from "../components/common/PageLoader";
import ErrorState from "../components/common/ErrorState";
import { useToast } from "../context/ToastContext";

function getStatusColor(status) {
  if (status === "completed") return "success";
  if (status === "processing") return "warning";
  if (status === "failed") return "error";
  return "default";
}

function formatDate(dateValue) {
  if (!dateValue) return "N/A";

  return new Date(dateValue).toLocaleString("en-IN", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

function getErrorMessage(error, fallbackMessage) {
  return (
    error.response?.data?.detail ||
    error.response?.data?.message ||
    fallbackMessage
  );
}

function InfoRow({ label, value }) {
  return (
    <div className="flex flex-col gap-1 rounded-2xl bg-slate-50 p-4">
      <Typography variant="body2" color="text.secondary">
        {label}
      </Typography>

      <Typography className="break-words font-semibold">
        {value || "N/A"}
      </Typography>
    </div>
  );
}

function DocumentDetail() {
  const { showToast } = useToast();
  const { documentId } = useParams();

  const [document, setDocument] = useState(null);
  const [loading, setLoading] = useState(false);
  const [reprocessing, setReprocessing] = useState(false);

  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const loadDocument = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getDocumentById(documentId);
      setDocument(data);
    } catch (error) {
      const message = getErrorMessage(
        error,
        "Failed to load document detail."
      );

      setError(message);
      showToast(message, "error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDocument();
  }, [documentId]);

  const handleReprocess = async () => {
    const confirmReprocess = window.confirm(
      "Are you sure you want to reprocess this document? Old vectors should be replaced."
    );

    if (!confirmReprocess) return;

    try {
      setReprocessing(true);
      setError("");
      setSuccessMessage("");

      await reprocessDocument(documentId);

      const message = "Document reprocessing started successfully.";

      setSuccessMessage(message);
      showToast(message, "success");

      await loadDocument();
    } catch (error) {
      const message = getErrorMessage(error, "Failed to reprocess document.");

      setError(message);
      showToast(message, "error");
    } finally {
      setReprocessing(false);
    }
  };

  const filename =
    document?.original_filename ||
    document?.filename ||
    document?.file_name ||
    "Unknown file";

  const status = document?.status || "uploaded";

  return (
    <DashboardLayout>
      <Box className="mb-6 flex flex-col justify-between gap-4 md:flex-row md:items-center">
        <div>
          <Typography variant="h4" className="font-extrabold">
            Document Detail
          </Typography>

          <Typography color="text.secondary" className="mt-1">
            View document metadata, processing status, and related session info.
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

      {error && (
        <div className="mb-5">
          <ErrorState message={error} onRetry={loadDocument} />
        </div>
      )}

      {successMessage && (
        <Alert severity="success" className="mb-5">
          {successMessage}
        </Alert>
      )}

      {loading ? (
        <PageLoader message="Loading document details..." />
      ) : !document ? (
        <Alert severity="warning">Document not found.</Alert>
      ) : (
        <>
          <Card className="mb-6">
            <CardContent className="p-6">
              <div className="flex flex-col gap-5 md:flex-row md:items-start">
                <div className="flex h-16 w-16 items-center justify-center rounded-3xl bg-indigo-100 text-indigo-600">
                  <DescriptionIcon fontSize="large" />
                </div>

                <div className="flex-1">
                  <Typography variant="h5" className="font-extrabold">
                    {filename}
                  </Typography>

                  <Typography color="text.secondary" className="mt-1">
                    Document ID: {document.id}
                  </Typography>

                  <div className="mt-4 flex flex-wrap gap-2">
                    <Chip label={status} color={getStatusColor(status)} />

                    <Chip
                      label={document.file_type || "Document"}
                      variant="outlined"
                    />

                    {document.session_id && (
                      <Chip
                        label={`Session ${document.session_id}`}
                        variant="outlined"
                        color="primary"
                      />
                    )}
                  </div>
                </div>

                <div className="flex flex-col gap-3 sm:flex-row md:flex-col">
                  <Button
                    component={Link}
                    to={`/chats?session_id=${
                      document.session_id || ""
                    }&document_id=${document.id}`}
                    variant="contained"
                    startIcon={<QuestionAnswerIcon />}
                    disabled={status !== "completed"}
                  >
                    Ask Question
                  </Button>

                  <Button
                    variant="outlined"
                    startIcon={<RefreshIcon />}
                    onClick={handleReprocess}
                    disabled={reprocessing}
                  >
                    {reprocessing ? "Reprocessing..." : "Reprocess"}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Card>
                <CardContent className="p-6">
                  <Typography variant="h6" className="font-bold">
                    Document Metadata
                  </Typography>

                  <Typography
                    color="text.secondary"
                    variant="body2"
                    className="mt-1"
                  >
                    Core SQL metadata stored for this document.
                  </Typography>

                  <div className="mt-5 grid gap-4 md:grid-cols-2">
                    <InfoRow label="Filename" value={filename} />
                    <InfoRow label="File Type" value={document.file_type} />
                    <InfoRow
                      label="File Size"
                      value={
                        document.file_size
                          ? `${document.file_size} bytes`
                          : "N/A"
                      }
                    />
                    <InfoRow
                      label="Storage Path"
                      value={document.file_path || document.path}
                    />
                    <InfoRow label="User ID" value={document.user_id} />
                    <InfoRow label="Session ID" value={document.session_id} />
                    <InfoRow
                      label="Created At"
                      value={formatDate(document.created_at)}
                    />
                    <InfoRow
                      label="Updated At"
                      value={formatDate(document.updated_at)}
                    />
                  </div>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={4}>
              <Card>
                <CardContent className="p-6">
                  <div className="mb-5 flex items-center gap-3">
                    <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-cyan-50 text-cyan-600">
                      <StorageIcon />
                    </div>

                    <div>
                      <Typography variant="h6" className="font-bold">
                        Processing Status
                      </Typography>

                      <Typography variant="body2" color="text.secondary">
                        RAG pipeline status
                      </Typography>
                    </div>
                  </div>

                  <Divider className="mb-5" />

                  <div className="space-y-4">
                    <InfoRow label="Status" value={status} />
                    <InfoRow
                      label="Chunks Count"
                      value={document.chunks_count || document.chunk_count}
                    />
                    <InfoRow
                      label="Embedding Provider"
                      value={document.embedding_provider || "Hugging Face"}
                    />
                    <InfoRow label="Vector DB" value="ChromaDB" />
                  </div>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card>
                <CardContent className="p-6">
                  <div className="mb-4 flex items-center gap-3">
                    <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-indigo-50 text-indigo-600">
                      <ChatIcon />
                    </div>

                    <div>
                      <Typography variant="h6" className="font-bold">
                        Related Chat Session
                      </Typography>

                      <Typography variant="body2" color="text.secondary">
                        This document belongs to one isolated chat session.
                      </Typography>
                    </div>
                  </div>

                  <div className="rounded-2xl border border-slate-200 p-4">
                    <Typography className="font-semibold">
                      Session ID: {document.session_id || "N/A"}
                    </Typography>

                    <Typography
                      variant="body2"
                      color="text.secondary"
                      className="mt-1"
                    >
                      Because your backend uses session-level isolation, this
                      document can only be used inside this chat session.
                    </Typography>

                    {document.session_id && (
                      <Button
                        component={Link}
                        to={`/chats?session_id=${document.session_id}&document_id=${document.id}`}
                        variant="outlined"
                        className="mt-4"
                        startIcon={<QuestionAnswerIcon />}
                      >
                        Open Related Chat
                      </Button>
                    )}
                  </div>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card>
                <CardContent className="p-6">
                  <Typography variant="h6" className="font-bold">
                    Source References
                  </Typography>

                  <Typography
                    color="text.secondary"
                    variant="body2"
                    className="mt-1"
                  >
                    Source references will appear after asking questions.
                  </Typography>

                  <div className="mt-5 rounded-2xl border border-dashed border-slate-300 p-5 text-center">
                    <Typography className="font-semibold">
                      No source references yet
                    </Typography>

                    <Typography
                      color="text.secondary"
                      variant="body2"
                      className="mt-1"
                    >
                      Ask a question from this document. The backend will return
                      sources with filename, chunk index, preview, and
                      similarity score.
                    </Typography>
                  </div>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </>
      )}
    </DashboardLayout>
  );
}

export default DocumentDetail;