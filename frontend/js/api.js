const API_BASE_URL = 'http://localhost:5000/api';

async function apiRequest(path, options = {}) {
  const isFormData = options.body instanceof FormData;
  const headers = isFormData ? { ...(options.headers || {}) } : { 'Content-Type': 'application/json', ...(options.headers || {}) };

  const response = await fetch(`${API_BASE_URL}${path}`, {
    credentials: 'include',
    ...options,
    headers,
  });

  const payload = await response.json().catch(() => ({ success: false, error: { message: 'The server returned an unexpected response.' } }));
  if (!response.ok || payload.success === false) {
    throw new Error(payload.error?.message || payload.message || 'Request failed');
  }
  return payload;
}
