// api.js
const API_BASE = 'http://127.0.0.1:8001';

export async function apiAddUser(formData) {
  const response = await fetch(`${API_BASE}/add_user`, {
    method: 'POST',
    body: formData
  });
  return response.json();
}

export async function apiUpdateUser(userId, formData) {
  const response = await fetch(`${API_BASE}/update_user/${userId}`, {
    method: 'PUT',
    body: formData
  });
  return response.json();
}

export async function apiToggleBlockUser(userId) {
  const response = await fetch(`${API_BASE}/toggle_block_user/${userId}`, {
    method: 'PATCH'
  });
  return response.json();
}

export async function apiDeleteUser(userId) {
  const response = await fetch(`${API_BASE}/delete_user/${userId}`, {
    method: 'DELETE'
  });
  return response.json();
}

export async function apiGetUsers() {
  const response = await fetch(`${API_BASE}/get_users`);
  return response.json();
}
