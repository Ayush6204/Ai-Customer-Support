import axiosInstance from "./axiosInstance";

export const askQuestion = async ({ sessionId, documentId, question }) => {
  const payload = {
    session_id: Number(sessionId),
    question,
  };

  if (documentId) {
    payload.document_id = Number(documentId);
  }

  const response = await axiosInstance.post("/chat/ask", payload);
  return response.data;
};