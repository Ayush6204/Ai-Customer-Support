import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  IconButton,
  Skeleton,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Tooltip,
  Typography,
} from "@mui/material";

import UploadFileIcon from "@mui/icons-material/UploadFile";
import DeleteIcon from "@mui/icons-material/Delete";
import QuestionAnswerIcon from "@mui/icons-material/QuestionAnswer";
import VisibilityIcon from "@mui/icons-material/Visibility";
import RefreshIcon from "@mui/icons-material/Refresh";

import DashboardLayout from "../layouts/DashboardLayout";
import { deleteDocument, getDocuments } from "../api/documentApi";
import { useToast } from "../context/ToastContext";
import ErrorState from "../components/common/ErrorState";
import EmptyState from "../components/common/EmptyState";

function getStatusColor(status) {
  if (status === "completed") return "success";
  if (status === "processing") return "warning";
  if (status === "failed") return "error";
  return "default";
}

function getFileType(filename) {
  if (!filename) return "unknown";
  return filename.substring(filename.lastIndexOf(".") + 1).toUpperCase();
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

function normalizeList(data) {
  if (Array.isArray(data)) return data;
  return data?.items || data?.data || data?.results || [];
}

function DocumentsTableSkeleton() {
  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Filename</TableCell>
          <TableCell>File Type</TableCell>
          <TableCell>Status</TableCell>
          <TableCell>Uploaded Date</TableCell>
          <TableCell align="right">Actions</TableCell>
        </TableRow>
      </TableHead>

      <TableBody>
        {[1, 2, 3, 4].map((row) => (
          <TableRow key={row}>
            <TableCell>
              <Skeleton width="70%" />
              <Skeleton width="35%" />
            </TableCell>

            <TableCell>
              <Skeleton width={70} height={32} />
            </TableCell>

            <TableCell>
              <Skeleton width={90} height={32} />
            </TableCell>

            <TableCell>
              <Skeleton width="70%" />
            </TableCell>

            <TableCell align="right">
              <Skeleton width={120} className="ml-auto" />
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}

function Documents() {
  const { showToast } = useToast();

  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [deletingId, setDeletingId] = useState(null);
  const [error, setError] = useState("");

  const loadDocuments = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getDocuments();
      const documentList = normalizeList(data);

      setDocuments(documentList);
    } catch (error) {
      const message = getErrorMessage(error, "Failed to load documents.");

      setError(message);
      showToast(message, "error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  const handleDelete = async (documentId) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this document?"
    );

    if (!confirmDelete) return;

    try {
      setDeletingId(documentId);
      setError("");

      await deleteDocument(documentId);

      setDocuments((prev) => prev.filter((doc) => doc.id !== documentId));
      showToast("Document deleted successfully.", "success");
    } catch (error) {
      const message = getErrorMessage(error, "Failed to delete document.");

      setError(message);
      showToast(message, "error");
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <DashboardLayout>
      <Box className="mb-6 flex flex-col justify-between gap-4 md:flex-row md:items-center">
        <div>
          <Typography variant="h4" className="font-extrabold">
            Documents
          </Typography>

          <Typography color="text.secondary" className="mt-1">
            Only your uploaded documents are shown here.
          </Typography>
        </div>

        <div className="flex gap-3">
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={loadDocuments}
            disabled={loading}
          >
            Retry / Refresh
          </Button>

          <Button
            component={Link}
            to="/documents/upload"
            variant="contained"
            startIcon={<UploadFileIcon />}
          >
            Upload Document
          </Button>
        </div>
      </Box>

      {error && <ErrorState message={error} onRetry={loadDocuments} />}

      <Card className="mt-5">
        <CardContent className="p-0">
          {loading ? (
            <Box className="overflow-x-auto">
              <DocumentsTableSkeleton />
            </Box>
          ) : documents.length === 0 ? (
            <EmptyState
              icon={<UploadFileIcon fontSize="large" />}
              title="No documents uploaded yet"
              description="Upload a document inside a chat session to start asking RAG questions."
              actionLabel="Upload First Document"
              actionTo="/documents/upload"
              component={Link}
            />
          ) : (
            <Box className="overflow-x-auto">
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Filename</TableCell>
                    <TableCell>File Type</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Uploaded Date</TableCell>
                    <TableCell align="right">Actions</TableCell>
                  </TableRow>
                </TableHead>

                <TableBody>
                  {documents.map((document) => {
                    const filename =
                      document.original_filename ||
                      document.filename ||
                      document.file_name ||
                      "Unknown file";

                    const status = document.status || "uploaded";

                    return (
                      <TableRow key={document.id} hover>
                        <TableCell>
                          <Typography className="font-semibold">
                            {filename}
                          </Typography>

                          <Typography variant="caption" color="text.secondary">
                            ID: {document.id}
                          </Typography>
                        </TableCell>

                        <TableCell>
                          <Chip
                            label={document.file_type || getFileType(filename)}
                            size="small"
                            variant="outlined"
                          />
                        </TableCell>

                        <TableCell>
                          <Chip
                            label={status}
                            color={getStatusColor(status)}
                            size="small"
                          />
                        </TableCell>

                        <TableCell>
                          {formatDate(
                            document.created_at || document.uploaded_at
                          )}
                        </TableCell>

                        <TableCell align="right">
                          <Tooltip title="View details">
                            <IconButton
                              component={Link}
                              to={`/documents/${document.id}`}
                            >
                              <VisibilityIcon />
                            </IconButton>
                          </Tooltip>

                          <Tooltip title="Ask question">
                            <span>
                              <IconButton
                                component={Link}
                                to={`/chats?session_id=${
                                  document.session_id || ""
                                }&document_id=${document.id}`}
                                disabled={status !== "completed"}
                              >
                                <QuestionAnswerIcon />
                              </IconButton>
                            </span>
                          </Tooltip>

                          <Tooltip title="Delete document">
                            <span>
                              <IconButton
                                color="error"
                                onClick={() => handleDelete(document.id)}
                                disabled={deletingId === document.id}
                              >
                                <DeleteIcon />
                              </IconButton>
                            </span>
                          </Tooltip>
                        </TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </Box>
          )}
        </CardContent>
      </Card>
    </DashboardLayout>
  );
}

export default Documents;