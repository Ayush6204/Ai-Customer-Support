import { useEffect, useMemo, useRef, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";

import {
  Alert,
  Box,
  Button,
  Chip,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Drawer,
  IconButton,
  TextField,
  Typography,
} from "@mui/material";

import SendIcon from "@mui/icons-material/Send";
import MenuIcon from "@mui/icons-material/Menu";
import DeleteIcon from "@mui/icons-material/Delete";
import UploadFileIcon from "@mui/icons-material/UploadFile";

import DashboardLayout from "../layouts/DashboardLayout";

import { createSession, deleteSession, getSessions } from "../api/sessionApi";
import { askQuestion } from "../api/chatApi";
import { deleteMessage, getSessionMessages } from "../api/historyApi";
import { getDocuments } from "../api/documentApi";

import UserMessage from "../components/chat/UserMessage";
import AIMessage from "../components/chat/AIMessage";
import TypingLoader from "../components/chat/TypingLoader";
import SourceCard from "../components/chat/SourceCard";
import SessionSidebar from "../components/chat/SessionSidebar";

import { useToast } from "../context/ToastContext";
import ErrorState from "../components/common/ErrorState";

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

function isProcessingDocument(document) {
  return document.status === "uploaded" || document.status === "processing";
}

function isCompletedDocument(document) {
  return document.status === "completed";
}

function isFailedDocument(document) {
  return document.status === "failed";
}

function getDocumentDisplayName(document) {
  return (
    document.original_filename ||
    document.filename ||
    document.file_name ||
    `Document ${document.id}`
  );
}

function getStatusChip(document) {
  if (isCompletedDocument(document)) {
    return <Chip label="Completed" size="small" color="success" />;
  }

  if (isProcessingDocument(document)) {
    return <Chip label="Processing" size="small" color="warning" />;
  }

  if (isFailedDocument(document)) {
    return <Chip label="Failed" size="small" color="error" />;
  }

  return <Chip label={document.status || "Unknown"} size="small" />;
}

function Chat() {
  const { showToast } = useToast();
  const [searchParams, setSearchParams] = useSearchParams();

  const initialSessionId = searchParams.get("session_id") || "";

  const bottomRef = useRef(null);

  const [sessions, setSessions] = useState([]);
  const [documents, setDocuments] = useState([]);

  const [activeSessionId, setActiveSessionId] = useState(initialSessionId);

  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");

  const [loadingSessions, setLoadingSessions] = useState(false);
  const [loadingMessages, setLoadingMessages] = useState(false);
  const [loadingDocuments, setLoadingDocuments] = useState(false);
  const [sending, setSending] = useState(false);

  const [mobileSidebarOpen, setMobileSidebarOpen] = useState(false);
  const [createChatDialogOpen, setCreateChatDialogOpen] = useState(false);
  const [newChatTitle, setNewChatTitle] = useState("");

  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const activeSession = useMemo(
    () =>
      sessions.find(
        (session) => Number(session.id) === Number(activeSessionId)
      ),
    [sessions, activeSessionId]
  );

  const sessionDocuments = useMemo(
    () =>
      documents.filter(
        (document) => Number(document.session_id) === Number(activeSessionId)
      ),
    [documents, activeSessionId]
  );

  const processingDocuments = useMemo(
    () => sessionDocuments.filter(isProcessingDocument),
    [sessionDocuments]
  );

  const completedDocuments = useMemo(
    () => sessionDocuments.filter(isCompletedDocument),
    [sessionDocuments]
  );

  const failedDocuments = useMemo(
    () => sessionDocuments.filter(isFailedDocument),
    [sessionDocuments]
  );

  const usableDocuments = completedDocuments;

  const hasProcessingDocuments = processingDocuments.length > 0;
  const hasCompletedDocuments = completedDocuments.length > 0;
  const hasFailedDocuments = failedDocuments.length > 0;

  const canAskQuestion =
    Boolean(activeSessionId) && !sending && !hasProcessingDocuments;

  const inputPlaceholder = hasProcessingDocuments
    ? "Document is processing. Please wait until it is completed..."
    : hasCompletedDocuments
      ? "Ask a question from this chat session's uploaded documents..."
      : "Say hi, or upload a document before asking document questions...";

  const activeSources = useMemo(() => {
    const latestAIMessage = [...messages]
      .reverse()
      .find((message) => message.role === "assistant" || message.type === "ai");

    return latestAIMessage?.sources || [];
  }, [messages]);

  const scrollToBottom = () => {
    setTimeout(() => {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, 100);
  };

  const loadSessions = async () => {
    try {
      setLoadingSessions(true);
      setError("");

      const data = await getSessions();
      const sessionList = normalizeList(data);

      setSessions(sessionList);

      if (!activeSessionId && sessionList.length > 0) {
        const sessionIdFromParams = searchParams.get("session_id");

        if (sessionIdFromParams) {
          setActiveSessionId(sessionIdFromParams);
        } else {
          const firstSessionId = sessionList[0].id;
          setActiveSessionId(firstSessionId);
          setSearchParams({ session_id: firstSessionId });
        }
      }
    } catch (error) {
      const message = getErrorMessage(error, "Failed to load chat sessions.");
      setError(message);
      showToast(message, "error");
    } finally {
      setLoadingSessions(false);
    }
  };

  const loadDocuments = async ({ silent = false } = {}) => {
    try {
      if (!silent) {
        setLoadingDocuments(true);
      }

      const data = await getDocuments();
      const documentList = normalizeList(data);

      setDocuments(documentList);
    } catch (error) {
      const message = getErrorMessage(error, "Failed to load documents.");
      showToast(message, "error");
    } finally {
      if (!silent) {
        setLoadingDocuments(false);
      }
    }
  };

  const loadMessages = async (sessionId) => {
    if (!sessionId) {
      setMessages([]);
      return;
    }

    try {
      setLoadingMessages(true);
      setError("");

      const data = await getSessionMessages(sessionId);
      const messageList = normalizeList(data);

      const normalizedMessages = [];

      messageList.forEach((message) => {
        if (message.question) {
          normalizedMessages.push({
            id: `${message.id}-user`,
            messageId: message.id,
            role: "user",
            content: message.question,
            sources: [],
            created_at: message.created_at,
          });
        }

        if (message.answer) {
          normalizedMessages.push({
            id: `${message.id}-assistant`,
            messageId: message.id,
            role: "assistant",
            content: message.answer,
            sources: message.sources || message.source_references || [],
            created_at: message.created_at,
          });
        }
      });

      setMessages(normalizedMessages);
      scrollToBottom();
    } catch (error) {
      const message = getErrorMessage(error, "Failed to load chat messages.");
      setError(message);
      showToast(message, "error");
    } finally {
      setLoadingMessages(false);
    }
  };

  useEffect(() => {
    loadSessions();
    loadDocuments();
  }, []);

  useEffect(() => {
    if (activeSessionId) {
      loadMessages(activeSessionId);
      loadDocuments({ silent: true });
    }
  }, [activeSessionId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages, sending]);

  useEffect(() => {
    if (!activeSessionId || !hasProcessingDocuments) return;

    const intervalId = setInterval(() => {
      loadDocuments({ silent: true });
    }, 3000);

    return () => clearInterval(intervalId);
  }, [activeSessionId, hasProcessingDocuments]);

  useEffect(() => {
    if (!activeSessionId) return;

    if (hasProcessingDocuments) {
      setSuccessMessage(
        "Your document is processing. You can ask questions after processing is completed."
      );
      return;
    }

    if (hasCompletedDocuments) {
      setSuccessMessage("Document processing completed. You can ask questions now.");
      return;
    }
  }, [activeSessionId, hasProcessingDocuments, hasCompletedDocuments]);

  const handleRetry = () => {
    loadSessions();
    loadDocuments();

    if (activeSessionId) {
      loadMessages(activeSessionId);
    }
  };

  const handleSelectSession = (sessionId) => {
    setActiveSessionId(sessionId);
    setError("");
    setSuccessMessage("");

    setSearchParams({
      session_id: sessionId,
    });

    setMobileSidebarOpen(false);
  };

  const handleCreateSessionClick = () => {
    setNewChatTitle("");
    setCreateChatDialogOpen(true);
  };

  const handleCreateSessionConfirm = async () => {
    const title = newChatTitle.trim() || "New Chat";

    try {
      setError("");
      setSuccessMessage("");
      setCreateChatDialogOpen(false);

      const newSession = await createSession(title);

      const normalizedNewSession = {
        ...newSession,
        id: newSession.id || newSession.session_id,
      };

      setSessions((prev) => [normalizedNewSession, ...prev]);
      setActiveSessionId(normalizedNewSession.id);
      setMessages([]);

      setSearchParams({
        session_id: normalizedNewSession.id,
      });

      const message = `Chat session "${title}" created.`;
      setSuccessMessage(message);
      showToast(message, "success");

      setMobileSidebarOpen(false);
    } catch (error) {
      const message = getErrorMessage(
        error,
        "Failed to create new chat session."
      );
      setError(message);
      showToast(message, "error");
    }

    setNewChatTitle("");
  };

  const handleCreateSessionCancel = () => {
    setCreateChatDialogOpen(false);
    setNewChatTitle("");
  };

  const handleDeleteSession = async (sessionId) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this chat session?"
    );

    if (!confirmDelete) return;

    try {
      setError("");
      setSuccessMessage("");

      await deleteSession(sessionId);

      const updatedSessions = sessions.filter(
        (session) => Number(session.id) !== Number(sessionId)
      );

      setSessions(updatedSessions);

      if (Number(activeSessionId) === Number(sessionId)) {
        const nextSession = updatedSessions[0];

        if (nextSession) {
          setActiveSessionId(nextSession.id);
          setSearchParams({ session_id: nextSession.id });
        } else {
          setActiveSessionId("");
          setMessages([]);
          setSearchParams({});
        }
      }

      const message = "Chat session deleted successfully.";
      setSuccessMessage(message);
      showToast(message, "success");
    } catch (error) {
      const message = getErrorMessage(
        error,
        "Failed to delete chat session."
      );
      setError(message);
      showToast(message, "error");
    }
  };

  const handleDeleteMessage = async (message) => {
    const messageId = message.messageId || message.id;

    if (!messageId) return;

    const confirmDelete = window.confirm(
      "Are you sure you want to delete this message?"
    );

    if (!confirmDelete) return;

    try {
      await deleteMessage(messageId);

      setMessages((prev) =>
        prev.filter((item) => item.messageId !== messageId)
      );

      showToast("Message deleted successfully.", "success");
    } catch (error) {
      const message = getErrorMessage(error, "Failed to delete message.");
      setError(message);
      showToast(message, "error");
    }
  };

  const handleSendQuestion = async (event) => {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion) return;

    if (!activeSessionId) {
      const message = "Please create or select a chat session first.";
      setError(message);
      showToast(message, "error");
      return;
    }

    if (hasProcessingDocuments) {
      const message =
        "Your document is still processing. Please wait until processing is completed before asking questions.";
      setError(message);
      showToast(message, "warning");
      return;
    }

    const tempUserMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      content: trimmedQuestion,
      sources: [],
    };

    setMessages((prev) => [...prev, tempUserMessage]);
    setQuestion("");
    setSending(true);
    setError("");
    setSuccessMessage("");

    try {
      const data = await askQuestion({
        sessionId: activeSessionId,
        documentId: null,
        question: trimmedQuestion,
      });

      const aiMessage = {
        id: data.message_id || `ai-${Date.now()}`,
        messageId: data.message_id,
        role: "assistant",
        content:
          data.answer ||
          data.response ||
          data.message ||
          "No answer returned from backend.",
        sources: data.sources || data.source_references || [],
      };

      setMessages((prev) => [...prev, aiMessage]);
      showToast("Answer generated successfully.", "success");

      loadDocuments({ silent: true });
    } catch (error) {
      const backendMessage = getErrorMessage(
        error,
        "Failed to get answer from backend."
      );

      const errorAIMessage = {
        id: `ai-error-${Date.now()}`,
        role: "assistant",
        content: backendMessage,
        sources: [],
      };

      setMessages((prev) => [...prev, errorAIMessage]);
      setError(backendMessage);
      showToast(backendMessage, "error");

      loadDocuments({ silent: true });
    } finally {
      setSending(false);
    }
  };

  const renderMessage = (message) => {
    const isUser =
      message.role === "user" ||
      message.role === "human" ||
      message.type === "user";

    return (
      <div
        key={message.id || `${message.role}-${Math.random()}`}
        className="group relative"
      >
        {isUser ? (
          <UserMessage message={message} />
        ) : (
          <AIMessage message={message} />
        )}

        {message.messageId && (
          <IconButton
            size="small"
            color="error"
            className="absolute right-2 top-0 opacity-0 transition group-hover:opacity-100"
            onClick={() => handleDeleteMessage(message)}
          >
            <DeleteIcon fontSize="small" />
          </IconButton>
        )}
      </div>
    );
  };

  return (
    <DashboardLayout>
      <Box className="flex h-[calc(100vh-9rem)] overflow-hidden rounded-3xl bg-white shadow-sm ring-1 ring-slate-200">
        <div className="hidden lg:block">
          <SessionSidebar
            sessions={sessions}
            activeSessionId={activeSessionId}
            onSelectSession={handleSelectSession}
            onCreateSession={handleCreateSessionClick}
            onDeleteSession={handleDeleteSession}
          />
        </div>

        <Drawer
          open={mobileSidebarOpen}
          onClose={() => setMobileSidebarOpen(false)}
          className="lg:hidden"
        >
          <SessionSidebar
            sessions={sessions}
            activeSessionId={activeSessionId}
            onSelectSession={handleSelectSession}
            onCreateSession={handleCreateSessionClick}
            onDeleteSession={handleDeleteSession}
          />
        </Drawer>

        <Box className="flex min-w-0 flex-1 flex-col bg-slate-50">
          <div className="flex items-center justify-between border-b border-slate-200 bg-white px-5 py-4">
            <div className="flex min-w-0 items-center gap-3">
              <IconButton
                className="lg:hidden"
                onClick={() => setMobileSidebarOpen(true)}
              >
                <MenuIcon />
              </IconButton>

              <div className="min-w-0">
                <Typography variant="h6" className="truncate font-bold">
                  {activeSession?.title || "Select or create a chat"}
                </Typography>

                <Typography variant="body2" color="text.secondary">
                  {activeSessionId
                    ? `Session ID: ${activeSessionId}`
                    : "No active session"}
                </Typography>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <Button
                component={Link}
                to={
                  activeSessionId
                    ? `/documents/upload?session_id=${activeSessionId}`
                    : "/documents/upload"
                }
                variant="outlined"
                size="small"
                startIcon={<UploadFileIcon />}
                disabled={!activeSessionId}
              >
                Upload
              </Button>

              <Button
                variant="contained"
                size="small"
                onClick={handleCreateSessionClick}
              >
                New Chat
              </Button>
            </div>
          </div>

          {(error || successMessage) && (
            <div className="border-b border-slate-200 bg-white px-5 py-3">
              {error && <ErrorState message={error} onRetry={handleRetry} />}

              {successMessage && !error && (
                <Alert severity={hasProcessingDocuments ? "info" : "success"}>
                  {successMessage}
                </Alert>
              )}
            </div>
          )}

          {activeSessionId && (
            <div className="border-b border-slate-200 bg-white px-5 py-3">
              <div className="mb-3">
                <div className="mb-2 flex items-center justify-between gap-3">
                  <Typography
                    variant="subtitle2"
                    className="font-semibold text-slate-700"
                  >
                    📄 Documents in this Chat
                  </Typography>

                  {loadingDocuments && (
                    <div className="flex items-center gap-2 text-xs text-slate-500">
                      <CircularProgress size={14} />
                      Refreshing
                    </div>
                  )}
                </div>

                {hasProcessingDocuments && (
                  <Alert severity="info" className="mb-3">
                    Your document is processing. Please wait until it becomes
                    completed before asking document questions.
                  </Alert>
                )}

                {hasFailedDocuments && (
                  <Alert severity="error" className="mb-3">
                    Some document uploads failed and are not usable. Please
                    upload the document again.
                  </Alert>
                )}

                {sessionDocuments.length === 0 ? (
                  <div className="rounded-xl border-2 border-dashed border-orange-300 bg-orange-50 p-4">
                    <Typography variant="body2" className="text-orange-900">
                      ⚠️ No documents uploaded yet. You can say hi, but upload a
                      document before asking document-based questions.
                    </Typography>

                    <Button
                      component={Link}
                      to={`/documents/upload?session_id=${activeSessionId}`}
                      variant="outlined"
                      size="small"
                      startIcon={<UploadFileIcon />}
                      className="mt-2"
                    >
                      Upload Document
                    </Button>
                  </div>
                ) : usableDocuments.length === 0 && !hasProcessingDocuments ? (
                  <div className="rounded-xl border-2 border-dashed border-red-300 bg-red-50 p-4">
                    <Typography variant="body2" className="text-red-900">
                      ❌ No usable documents in this chat. Failed documents are
                      hidden from chat. Please upload again.
                    </Typography>

                    <Button
                      component={Link}
                      to={`/documents/upload?session_id=${activeSessionId}`}
                      variant="outlined"
                      size="small"
                      startIcon={<UploadFileIcon />}
                      className="mt-2"
                    >
                      Upload Again
                    </Button>
                  </div>
                ) : (
                  <div className="space-y-2">
                    {[...processingDocuments, ...usableDocuments].map(
                      (document) => {
                        const filename = getDocumentDisplayName(document);

                        const fileSize = document.file_size
                          ? `${(document.file_size / 1024).toFixed(2)} KB`
                          : "Unknown size";

                        return (
                          <div
                            key={document.id}
                            className="flex items-center gap-3 rounded-lg border border-slate-200 bg-slate-50 p-3"
                          >
                            <div className="flex h-8 w-8 items-center justify-center rounded bg-indigo-100 text-sm font-semibold text-indigo-700">
                              📄
                            </div>

                            <div className="min-w-0 flex-1">
                              <Typography
                                variant="body2"
                                className="truncate font-semibold"
                              >
                                {filename}
                              </Typography>

                              <Typography
                                variant="caption"
                                color="text.secondary"
                              >
                                {fileSize}
                              </Typography>

                              {document.error_message && (
                                <Typography
                                  variant="caption"
                                  className="block truncate text-red-600"
                                >
                                  {document.error_message}
                                </Typography>
                              )}
                            </div>

                            {getStatusChip(document)}
                          </div>
                        );
                      }
                    )}

                    <Button
                      component={Link}
                      to={`/documents/upload?session_id=${activeSessionId}`}
                      variant="outlined"
                      size="small"
                      startIcon={<UploadFileIcon />}
                      fullWidth
                      className="mt-2"
                    >
                      Upload More Documents
                    </Button>
                  </div>
                )}
              </div>
            </div>
          )}

          <div className="flex-1 overflow-y-auto p-5">
            {loadingSessions || loadingMessages ? (
              <Box className="flex h-full items-center justify-center">
                <CircularProgress />
              </Box>
            ) : !activeSessionId ? (
              <Box className="flex h-full flex-col items-center justify-center text-center">
                <Typography variant="h5" className="font-bold">
                  Start a new chat
                </Typography>

                <Typography color="text.secondary" className="mt-2 max-w-md">
                  Create a chat session first. Then upload documents inside that
                  session and ask questions from them.
                </Typography>

                <Button
                  variant="contained"
                  className="mt-5"
                  onClick={handleCreateSessionClick}
                >
                  Create New Chat
                </Button>
              </Box>
            ) : messages.length === 0 ? (
              <Box className="flex h-full flex-col items-center justify-center text-center">
                <Typography variant="h5" className="font-bold">
                  No messages yet
                </Typography>

                <Typography color="text.secondary" className="mt-2 max-w-md">
                  {hasProcessingDocuments
                    ? "Your document is processing. You can ask questions after it is completed."
                    : hasCompletedDocuments
                      ? "Ask your first question from documents uploaded in this chat session."
                      : "Say hi, or upload a document before asking document-based questions."}
                </Typography>

                <div className="mt-4 flex gap-2">
                  <Chip label="PDF" variant="outlined" />
                  <Chip label="TXT" variant="outlined" />
                  <Chip label="DOCX" variant="outlined" />
                </div>
              </Box>
            ) : (
              <>
                {messages.map(renderMessage)}
                {sending && <TypingLoader />}
                <div ref={bottomRef} />
              </>
            )}
          </div>

          <form
            onSubmit={handleSendQuestion}
            className="border-t border-slate-200 bg-white p-4"
          >
            <div className="flex gap-3">
              <TextField
                fullWidth
                multiline
                maxRows={4}
                placeholder={inputPlaceholder}
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                disabled={sending || !activeSessionId || hasProcessingDocuments}
              />

              <Button
                type="submit"
                variant="contained"
                disabled={
                  !canAskQuestion || !question.trim() || !activeSessionId
                }
                endIcon={<SendIcon />}
                className="min-w-28"
              >
                {hasProcessingDocuments ? "Wait" : "Send"}
              </Button>
            </div>

            {hasProcessingDocuments && (
              <Typography variant="caption" className="mt-2 block text-amber-700">
                Document processing is running. Chat will be available after
                processing is completed.
              </Typography>
            )}
          </form>
        </Box>

        <Box className="hidden w-96 flex-col border-l border-slate-200 bg-white xl:flex">
          <div className="border-b border-slate-200 p-5">
            <Typography variant="h6" className="font-bold">
              Source References
            </Typography>

            <Typography variant="body2" color="text.secondary">
              Sources from the latest AI answer.
            </Typography>
          </div>

          <div className="flex-1 overflow-y-auto p-4">
            {activeSources.length === 0 ? (
              <div className="rounded-2xl border border-dashed border-slate-300 p-5 text-center">
                <Typography className="font-semibold">No sources yet</Typography>

                <Typography
                  variant="body2"
                  color="text.secondary"
                  className="mt-1"
                >
                  Ask a question and retrieved document chunks will appear here.
                </Typography>
              </div>
            ) : (
              activeSources.map((source, index) => (
                <SourceCard key={index} source={source} index={index} />
              ))
            )}
          </div>
        </Box>
      </Box>

      <Dialog
        open={createChatDialogOpen}
        onClose={handleCreateSessionCancel}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Create New Chat</DialogTitle>

        <DialogContent className="mt-4">
          <TextField
            autoFocus
            fullWidth
            label="Chat Title"
            placeholder="Enter a title for your chat session"
            value={newChatTitle}
            onChange={(event) => setNewChatTitle(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                handleCreateSessionConfirm();
              }
            }}
            helperText="Give your chat a meaningful name, for example Project Documentation or Q&A Session."
          />
        </DialogContent>

        <DialogActions>
          <Button onClick={handleCreateSessionCancel}>Cancel</Button>

          <Button
            onClick={handleCreateSessionConfirm}
            variant="contained"
            disabled={!newChatTitle.trim()}
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </DashboardLayout>
  );
}

export default Chat;