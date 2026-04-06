const ACCESS_KEY = "clinic_access";
const REFRESH_KEY = "clinic_refresh";
const USER_KEY = "clinic_user";

export function setSession({ access, refresh, user }) {
  if (access) {
    localStorage.setItem(ACCESS_KEY, access);
  }
  if (refresh) {
    localStorage.setItem(REFRESH_KEY, refresh);
  }
  if (user) {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }
}

export function getAccessToken() {
  return localStorage.getItem(ACCESS_KEY);
}

export function getRefreshToken() {
  return localStorage.getItem(REFRESH_KEY);
}

export function getStoredUser() {
  const raw = localStorage.getItem(USER_KEY);

  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function clearSession() {
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
  localStorage.removeItem(USER_KEY);
}

export function hasSession() {
  return Boolean(getAccessToken());
}
