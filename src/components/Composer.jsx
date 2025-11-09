import React, { useContext, useState } from 'react';
import { AppCtx } from '../App';
import { apiChat } from '../lib/apiClient';  // ← Import API client

const SECTIONS = ['ABOUT','EXPERIENCE','PROJECTS','CASE STUDIES','SKILLS','CERTIFICATIONS','EDUCATION'];

export default function Composer(){
  const { activeConvo, append, setSection } = useContext(AppCtx);
  const [open, setOpen] = useState(false);
  const [text, setText] = useState('');
  const [busy, setBusy] = useState(false);

  const send = async () => {  // ← Make async
    const q = text.trim();
    if (!q || !activeConvo) return;
    
    setText('');
    
    // Add user message immediately
    append(activeConvo.id, {role:'user', text:q});
    
    // Call real backend
    setBusy(true);
    try {
      const response = await apiChat({
        question: q,
        section: activeConvo.activeSection,
        conversationId: activeConvo.id
      });
      
      // Add assistant response
      append(activeConvo.id, {
        role: 'assistant',
        text: response.answer,
        chips: response.chips || [],
        links: response.links || []
      });
    } catch (error) {
      console.error('API Error:', error);
      // Add error message
      append(activeConvo.id, {
        role: 'assistant',
        text: `⚠️ Sorry, I encountered an error: ${error.message}. Please make sure the backend is running.`,
        chips: ['Error'],
        links: []
      });
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="composer">
      <div className="composer-header">
        <div className="section-picker">
          <button className="section-picker-btn" onClick={()=>setOpen(v=>!v)}>
            {activeConvo?.activeSection || 'Select Section'} ▼
          </button>
          <div className={`section-picker-dropdown ${open?'show':''}`}>
            <div className="dropdown-item" onClick={()=>{setSection(activeConvo.id,null); setOpen(false);}}>All Sections</div>
            {SECTIONS.map(s=>
              <div key={s} className="dropdown-item" onClick={()=>{setSection(activeConvo.id,s); setOpen(false);}}>{s}</div>)}
          </div>
        </div>
      </div>

      <div className="composer-input-container">
        <textarea
          className="composer-input"
          placeholder="Ask anything about the candidate…"
          rows="1"
          value={text}
          onChange={e=>setText(e.target.value)}
          onKeyDown={e=>{if(e.key==='Enter' && !e.shiftKey){e.preventDefault(); send();}}}
          disabled={busy}
        />
        <button className="send-btn" disabled={busy} onClick={send}>➤</button>
      </div>
    </div>
  );
}