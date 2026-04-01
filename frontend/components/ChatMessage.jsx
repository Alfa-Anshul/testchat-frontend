import React from 'react';
import './ChatMessage.css';

function formatText(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>');
}

function formatTime(date) {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

export default function ChatMessage({ message }) {
  const isUser = message.role === 'user';
  return (
    <div className={`message-row ${isUser ? 'user' : 'bot'}`}>
      {!isUser && (
        <div className="avatar bot-av"><span>N</span></div>
      )}
      <div className="message-content">
        <div
          className={`bubble ${isUser ? 'user-bubble' : 'bot-bubble'}`}
          dangerouslySetInnerHTML={{ __html: formatText(message.text) }}
        />
        <div className={`msg-meta ${isUser ? 'meta-right' : ''}`}>{formatTime(message.ts)}</div>
      </div>
      {isUser && (
        <div className="avatar user-av"><span>U</span></div>
      )}
    </div>
  );
}
