export default function MessageBubble({ text, isUser }) {
  return (
    <div
      className={`max-w-[85%] sm:max-w-[75%] px-4 py-3 rounded-2xl text-[15px] leading-relaxed ${
        isUser
          ? "self-end bg-green-600 text-white rounded-br-md"
          : "self-start bg-gray-800/90 text-gray-100 rounded-bl-md"
      }`}
    >
      {text}
    </div>
  );
}
