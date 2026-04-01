import React, { useState, useRef, useEffect } from 'react';
import ChatMessage from './components/ChatMessage.jsx';
import TypingIndicator from './components/TypingIndicator.jsx';
import './App.css';

const BOT_NAME = 'Nexus';
const SUGGESTIONS = [
  'What can you help me with?',
  'Tell me about Anervea AI',
  'How does competitive intelligence work?',
  'What is AlfaKinetic?',
];

const BOT_RESPONSES = [
  "I'm Nexus, your AI assistant powered by Anervea. I can help with competitive intelligence, research, and strategic insights.",
  "Anervea AI builds intelligent platforms that transform how organizations understand their competitive landscape.",
  "Competitive intelligence involves gathering, analyzing, and acting on information about competitors, markets, and industry trends to drive better decisions.",
  "AlfaKinetic is Anervea's flagship competitive intelligence platform — it synthesizes signals from multiple data sources into actionable insights for pharma and life sciences.",
  "Great question! I'm here to assist you around the clock. Ask me anything about markets, competitors, or industry trends.",
  "I can analyze data patterns, summarize research, and provide strategic recommendations tailored to your needs.",
  "Could you clarify that a bit more? I want to make sure I give you the most precise and useful answer possible.",
];

function getBotResponse(input) {
  const lower = input.toLowerCase();
  if (lower.includes('anervea')) return BOT_RESPONSES[1];
  if (lower.includes('competitive') || lower.includes('intelligence')) return BOT_RESPONSES[2];
  if (lower.includes('alfakinetic') || lower.includes('alfa')) return BOT_RESPONSES[3];
  if (lower.includes('help') || lower.includes('what can')) return BOT_RESPONSES[0];
  if (lower.includes('analyze') || lower.includes('data')) return BOT_RESPONSES[5];
  return BOT_RESPONSES[Math.floor(Math.random() * BOT_RESPONSES.length)];
}

export default function App() {
  const [messages, setMessages] = useState([
    { id: 1, role: 'bot', text: 'Hello! I am **Nexus**, your intelligent AI assistant by Anervea. How can I help you today?', ts: new Date() }
  ]);
  const [input, setInput] = useState('');
  const [typing, setTyping] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, typing]);

  const sendMessage = (text) => {
    const trimmed = (text || input).trim();
    if (!trimmed) return;
    const userMsg = { id: Date.now(), role: 'user', text: trimmed, ts: new Date() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setTyping(true);
    setTimeout(() => {
      setTyping(false);
      const botMsg = { id: Date.now() + 1, role: 'bot', text: getBotResponse(trimmed), ts: new Date() };
      setMessages(prev => [...prev, botMsg]);
    }, 1200 + Math.random() * 800);
    inputRef.current?.focus();
  };

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([{ id: Date.now(), role: 'bot', text: 'Chat cleared. Start a new conversation!', ts: new Date() }]);
  };

  return (
    <div className="app-shell">
      <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <span className="logo-mark">N</span>
          <span className="logo-text">Nexus</span>
        </div>
        <nav className="sidebar-nav">
          <button className="nav-item active"><span className="nav-icon">💬</span>Chat</button>
          <button className="nav-item" onClick={clearChat}><span className="nav-icon">🗑</span>Clear Chat</button>
        </nav>
        <div className="sidebar-footer">
          <span className="powered">Powered by <strong>Anervea AI</strong></span>
        </div>
      </aside>

      {sidebarOpen && <div className="overlay" onClick={() => setSidebarOpen(false)} />}

      <main className="chat-main">
        <header className="chat-header">
          <button className="menu-btn" onClick={() => setSidebarOpen(!sidebarOpen)}>
            <span /><span /><span />
          </button>
          <div className="header-title">
            <div className="bot-avatar-sm"><span>N</span><div className="pulse" /></div>
            <div>
              <div className="header-name">{BOT_NAME}</div>
              <div className="header-status">Online · Anervea AI</div>
            </div>
          </div>
          <button className="clear-btn" onClick={clearChat} title="Clear chat">✕</button>
        </header>

        <div className="messages-area">
          <div className="messages-inner">
            {messages.map(msg => (
              <ChatMessage key={msg.id} message={msg} />
            ))}
            {typing && <TypingIndicator />}
            <div ref={bottomRef} />
          </div>
        </div>

        {messages.length <= 2 && (
          <div className="suggestions">
            {SUGGESTIONS.map((s, i) => (
              <button key={i} className="suggestion-chip" onClick={() => sendMessage(s)}>{s}</button>
            ))}
          </div>
        )}

        <div className="input-area">
          <div className="input-box">
            <textarea
              ref={inputRef}
              className="chat-input"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKey}
              placeholder="Message Nexus..."
              rows={1}
            />
            <button
              className={`send-btn ${input.trim() ? 'active' : ''}`}
              onClick={() => sendMessage()}
              disabled={!input.trim()}
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 2L11 13" />
                <path d="M22 2L15 22L11 13L2 9L22 2Z" />
              </svg>
            </button>
          </div>
          <p className="input-hint">Press Enter to send · Shift+Enter for new line</p>
        </div>
      </main>
    </div>
  );
}
