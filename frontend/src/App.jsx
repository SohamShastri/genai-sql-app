import { useState } from "react";
import "./index.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  return (
    <div className="app">
      <header className="header">
        <h2>GenAI SQL Chatbot</h2>
        <p>Ask questions about your data (upload your files)</p>
      </header>

      <div className="chat-window">
        {messages.length === 0 && (
          <div className="empty">Start by asking something 👇</div>
        )}

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.sender}`}
          >
            {msg.text}
          </div>
        ))}

        {loading && (
          <div className="message bot">AI is thinking...</div>
        )}
      </div>

      <div className="input-bar">
        <input
          type="text"
          placeholder="Ask something about your data..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );

  async function sendMessage() {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await res.json();

      const botMessage = {
        sender: "bot",
        text: data.reply || "No response",
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Error connecting to backend" },
      ]);
    } finally {
      setLoading(false);
    }
  }
}

export default App;
