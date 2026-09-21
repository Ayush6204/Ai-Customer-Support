import axiosInstance from "./axiosInstance";

export const uploadDocument = async (file, sessionId, onUploadProgress) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axiosInstance.post(
    `/documents/upload?session_id=${sessionId}`,
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      onUploadProgress,
    }
  );

  return response.data;
};

export const getDocuments = async () => {
  const response = await axiosInstance.get("/documents");
  return response.data;
};

export const getDocumentById = async (documentId) => {
  const response = await axiosInstance.get(`/documents/${documentId}`);
  return response.data;
};

export const deleteDocument = async (documentId) => {
  const response = await axiosInstance.delete(`/documents/${documentId}`);
  return response.data;
};

export const reprocessDocument = async (documentId) => {
  const response = await axiosInstance.post(`/documents/${documentId}/reprocess`);
  return response.data;
};