import React, { useState } from 'react';

export default function HeaderBar({ onMenu }){
  const [open, setOpen] = useState(false);
  return (
    <header className="header">
      <div style={{display:'flex',alignItems:'center',gap:12}}>
        <button className="btn" onClick={onMenu} style={{display:'none'}} className="mobile-only">☰</button>
        <div className="header-title">Portfolio v1</div>
      </div>

      <div className="header-actions">
        <button className="btn">Share</button>
        <button className="btn">Profile</button>
        <button
  className="btn mobile-only"      // ← single prop with both classes
  onClick={onMenu}
  style={{ display: 'none' }}
></button>
        <div className="overflow">
          <button className="btn" onClick={()=>setOpen(v=>!v)}>⋯</button>
          <div className={`overflow-dropdown ${open?'show':''}`}>
            <div className="overflow-item">Delete Chat</div>
            <div className="overflow-item">Export Chat (markdown)</div>
            <div className="overflow-item">Copy Link to this Answer</div>
            <div className="overflow-item">Report Issue / Feedback</div>
          </div>
        </div>
      </div>
    </header>
  );
}