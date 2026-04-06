import axios from "axios";

import { clearSession, getAccessToken, getRefreshToken, setSession } from "./session";

const API_BASE_URL =
  process.env.VUE_APP_API_URL || "http://127.0.0.1:8000/api/";

const api = axios.create({
  baseURL: API_BASE_URL,
});

let refreshingToken = null;

api.interceptors.request.use((config) => {
  const token = getAccessToken();

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status === 401 &&
      !originalRequest?._retry &&
      getRefreshToken()
    ) {
      originalRequest._retry = true;

      try {
        refreshingToken =
          refreshingToken ||
          axios.post(`${API_BASE_URL}token/refresh/`, {
            refresh: getRefreshToken(),
          });

        const { data } = await refreshingToken;
        setSession({
          access: data.access,
          refresh: getRefreshToken(),
        });
        refreshingToken = null;

        originalRequest.headers.Authorization = `Bearer ${data.access}`;
        return api(originalRequest);
      } catch (refreshError) {
        refreshingToken = null;
        clearSession();
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
