import axiosInstance from "./axiosInstance";

export const getSessions = async () => {
  const response = await axiosInstance.get("/sessions");
  return response.data;
};

export const getSessionById = async (sessionId) => {
  const response = await axiosInstance.get(`/sessions/${sessionId}`);
  return response.data;
};

export const createSession = async (title = "New Chat") => {
  const response = await axiosInstance.post("/sessions", {
    title,
  });
  return response.data;
};

export const updateSession = async (sessionId, title) => {
  const response = await axiosInstance.patch(`/sessions/${sessionId}`, {
    title,
  });
  return response.data;
};

export const deleteSession = async (sessionId) => {
  const response = await axiosInstance.delete(`/sessions/${sessionId}`);
  return response.data;
};