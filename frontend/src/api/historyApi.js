import axiosInstance from "./axiosInstance";

export const getSessionMessages = async (sessionId) => {
  const response = await axiosInstance.get(`/sessions/${sessionId}/messages`);
  return response.data;
};

export const getAllHistory = async () => {
  const response = await axiosInstance.get("/history");
  return response.data;
};

export const deleteMessage = async (messageId) => {
  const response = await axiosInstance.delete(`/history/${messageId}`);
  return response.data;
};