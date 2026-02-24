import React from "react";

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="logo">⚡ GenAI</div>

      <button className="new-chat-btn">
        + New Chat
      </button>

      <div className="menu">
        <div className="menu-item">💬 Chats</div>
        <div className="menu-item">🛠 Tools</div>
      </div>
    </aside>
  );
}

export default Sidebar;
