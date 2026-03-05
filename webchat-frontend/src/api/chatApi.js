const API_BASE = "http://localhost:5048";
export async function sendMessage(message) {
  const res = await fetch(`${API_BASE}/api/chat`, {
    // ← tiene que ser /api/chat
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ datail: res.statusText }));
    throw new Error(err.datail || "Error al enviar el mesaje");
  }
  return res.json();
}
