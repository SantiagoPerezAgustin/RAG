const API_BASE = "http://localhost:5048";

export async function sendMessage({ message, history }) {
  const payload = { message };
  if (Array.isArray(history) && history.length > 0) {
    payload.history = history;
  }

  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Error al enviar el mensaje");
  }
  return res.json();
}

export async function logConversation({
  userId,
  channel,
  message,
  response,
  summary,
}) {
  const res = await fetch(`${API_BASE}/api/conversations/log`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ userId, channel, message, response, summary }),
  });
  if (!res.ok) throw new Error("Error al guardar el log");
}
