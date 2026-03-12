import { useState } from "react";
import { sendMessage, logConversation } from "../api/chatApi";
import MessageBubble from "./MessageBubble";

export default function ChatWidget() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSend() {
    const text = input.trim();
    if (!text || loading) return;

    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setLoading(true);

    try {
      const history = messages.slice(-10);
      const data = await sendMessage({ message: text, history });

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.answer },
      ]);

      logConversation({
        userId: "web-user",
        channel: "web",
        message: text,
        response: data.answer,
        summary: data.summary ?? "",
      }).catch(() => {});
    } catch (e) {
      const msg = e?.message || "";
      const friendlyMessage =
        msg.toLowerCase().includes("timeout") ||
        msg.toLowerCase().includes("time-out")
          ? "Estoy tardando más de lo normal. Probá de nuevo en unos segundos."
          : "Hubo un error al responder. Si persiste, contactá a soporte.";

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: friendlyMessage },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col h-full min-h-screen w-full bg-[#0a0a0a]">
      {/* Header: solo fondo y sombra suave, sin líneas */}
      <header className="flex-shrink-0 px-6 py-4 bg-[#0f0f0f] shadow-[0_1px_0_0_rgba(255,255,255,0.05)]">
        <div className="flex items-center gap-3 w-full">
          <div className="w-10 h-10 rounded-xl bg-green-600 flex items-center justify-center text-white font-bold text-lg shrink-0">
            S
          </div>
          <div>
            <h1 className="text-white font-semibold text-lg">
              Soporte técnico
            </h1>
            <p className="text-green-400/80 text-sm">Asistente nivel 1</p>
          </div>
        </div>
      </header>

      {/* Área de mensajes */}
      <div className="flex-1 overflow-auto px-4 sm:px-6 py-6 flex flex-col gap-4 min-h-0 w-full">
        {messages.length === 0 && (
          <div className="flex-1 flex flex-col items-center justify-center text-center min-h-[60vh]">
            <div className="w-16 h-16 rounded-2xl bg-green-600/20 flex items-center justify-center mb-5 text-3xl">
              💬
            </div>
            <p className="text-lg font-medium text-gray-300">
              ¿En qué podemos ayudarte?
            </p>
            <p className="text-gray-500 text-sm mt-1">Escribí tu consulta abajo.</p>
          </div>
        )}
        {messages.map((m, i) => (
          <MessageBubble key={i} text={m.content} isUser={m.role === "user"} />
        ))}
        {loading && (
          <div className="self-start px-4 py-3 rounded-2xl rounded-bl-md bg-gray-800/80 text-green-400 flex gap-1">
            <span className="animate-bounce">.</span>
            <span className="animate-bounce delay-100">.</span>
            <span className="animate-bounce delay-200">.</span>
          </div>
        )}
      </div>

      {/* Input: mismo estilo que header, sin borde */}
      <div className="flex-shrink-0 p-4 bg-[#0f0f0f] shadow-[0_-1px_0_0_rgba(255,255,255,0.05)]">
        <div className="flex gap-3 w-full">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSend()}
            placeholder="Escribí tu mensaje..."
            className="flex-1 px-4 py-3 rounded-xl bg-gray-900 border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-green-500/50 focus:border-green-500/50 transition"
          />
          <button
            onClick={handleSend}
            disabled={loading}
            className="px-6 py-3 bg-green-600 hover:bg-green-500 text-white font-medium rounded-xl disabled:opacity-50 disabled:cursor-not-allowed transition-colors shrink-0"
          >
            Enviar
          </button>
        </div>
      </div>
    </div>
  );
}
