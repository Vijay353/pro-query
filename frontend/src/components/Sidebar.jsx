import React, { useContext } from 'react';
import { AppCtx } from '../App';

export default function Sidebar({ isOpen }){
  const { newChat, conversations, activeId, setActiveId } = useContext(AppCtx);
  return (
    <aside className={`sidebar ${isOpen?'show':''}`}>
      <div className="sb-header">
        <span className="logo">Portfolio AI</span>
        <span className="version">v1</span>
      </div>

      <button className="new-chat-btn" onClick={newChat}>New Chat</button>
      <input className="search-input" placeholder="Search chats…" readOnly />

      <div className="library-section">
        <div className="library-header">📚 LIBRARY</div>
        <div className="library-item">FAQ / Sample Prompts</div>
      </div>

      <a className="github-link" href="https://github.com/yourhandle" target="_blank" rel="noreferrer">GitHub (@yourhandle)</a>

      <div className="section-list">
        <div className="section-header">SECTIONS</div>
        {['About','Experience','Projects','Case Studies','Skills','Certifications','Education'].map(s =>
          <div key={s} className="section-item">{s}</div>)}
      </div>

      <div className="chat-list">
        <div className="chat-header">CHATS</div>
        {conversations.map(c =>
          <div key={c.id} className={`chat-item ${c.id===activeId?'active':''}`} onClick={()=>setActiveId(c.id)}>
            • {c.messages[0]?.text.slice(0,28) || 'New chat'}
          </div>)}
      </div>
    </aside>
  );
}