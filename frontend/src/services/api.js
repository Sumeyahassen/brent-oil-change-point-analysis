import axios from "axios";

const API_BASE = "http://127.0.0.1:5000";

const api = axios.create({ baseURL: API_BASE });

export const getPrices = async (startDate, endDate) => {
  const params = {};
  if (startDate) params.start_date = startDate;
  if (endDate) params.end_date = endDate;
  const res = await api.get("/api/prices", { params });
  return res.data;
};

export const getEvents = async () => {
  const res = await api.get("/api/events");
  return res.data;
};

export const getChangepoints = async () => {
  const res = await api.get("/api/changepoints");
  return res.data;
};

export const getEventCorrelation = async (window = 30) => {
  const res = await api.get("/api/events/correlation", { params: { window } });
  return res.data;
};

export const getStats = async () => {
  const res = await api.get("/api/stats");
  return res.data;
};

export default api;