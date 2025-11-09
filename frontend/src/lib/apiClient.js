// src/lib/apiClient.js  (LIVE version)
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

export async function apiChat({ question, section, conversationId }) {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, section, conversationId })
  });
  if (!res.ok) throw new Error('Chat API failed');
  return res.json();               // ← { answer, links[], chips[] }
}

export async function apiSections() {
  const res = await fetch(`${API_BASE}/api/sections`);
  if (!res.ok) throw new Error('Sections API failed');
  return res.json();               // ← full portfolio JSON
}