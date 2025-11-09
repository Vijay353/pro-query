import React from 'react';

export default function MessageItem({ role, text, links=[], chips=[] }){
  const isUser = role==='user';
  return (
    <div className="message">
      <div className={`message-avatar ${isUser?'user-avatar':'assistant-avatar'}`}>
        {isUser?'U':'AI'}
      </div>
      <div className="message-content">
        <div className="message-text">{text}</div>
        {chips.length>0 &&
          <div className="message-chips">
            {chips.map(c=><span key={c} className="chip">{c}</span>)}
          </div>}
        {links.length>0 &&
          <div className="message-links">
            {links.map(l=>
              <a key={l.url} className="message-link" href={l.url} target="_blank" rel="noreferrer">{l.label}</a>)}
          </div>}
      </div>
    </div>
  );
}