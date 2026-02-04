import { useState } from "react";
import "./index.css";


function App(
) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploadStatus,  setUploadStatus] = useState(""); 

  async function handleFileUpload(e) {
  const file = e.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    if (data.error) {
      setUploadStatus(`❌ ${data.error}`);
    } else {
      setUploadStatus(
        `✅ Using uploaded dataset: ${file.name} (${data.rows} rows)`
      );
    }
  } catch (err) {
    setUploadStatus("❌ Upload failed");
  }
}



  return (
    <div className="app">
      <header className="header">
        <h2>GenAI SQL Chatbot</h2>
        <p>Ask questions about your data after uploading (CSV/XLSX)</p>
        
      </header>

      <div className="chat-window">
        {messages.length === 0 && (
          <div className="empty">Upload Data and start chatting naturally👇</div>
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
{uploadStatus && (
  <div style={{ padding: "0 16px", fontSize: "14px", color: "#080809" }}>
    {uploadStatus}
  </div>
)}
      <div className="input-bar">
  <input
        type="text"
        placeholder="Ask something about your data..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && sendMessage()}
      />

      {/* Upload button */}
      <label className="upload-btn">
        📁
        <input
          type="file"
          accept=".csv,.xlsx"
          onChange={handleFileUpload}
         hidden
        />
      </label>

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
