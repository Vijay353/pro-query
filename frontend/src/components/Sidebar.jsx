import React, { useContext, useState } from 'react';
import { AppCtx } from '../App';

// Default profile images based on gender
const DEFAULT_AVATARS = {
  male: 'https://api.dicebear.com/7.x/avataaars/svg?seed=male-pro&backgroundColor=0165E1',
  female: 'https://api.dicebear.com/7.x/avataaars/svg?seed=female-pro&backgroundColor=17A9FD',
  neutral: 'https://api.dicebear.com/7.x/bottts/svg?seed=ai-pro&backgroundColor=0165E1'
};

export default function Sidebar({ isOpen, profileData }) {
  const { newChat, conversations, activeId, setActiveId, deleteChat } = useContext(AppCtx);
  
  // Extract profile data with defaults
  const {
    name = 'John Doe',
    role = 'Data Scientist',
    yearsExperience = '5+',
    companies = ['Google', 'Microsoft'],
    education = 'MS in Computer Science',
    profileImage = null,
    gender = 'neutral'
  } = profileData || {};

  // Determine profile image
  const getProfileImage = () => {
    if (profileImage) return profileImage;
    return DEFAULT_AVATARS[gender] || DEFAULT_AVATARS.neutral;
  };

  // Format companies list
  const displayCompanies = companies.slice(0, 3); // Show max 3

  const [chatMenuOpen, setChatMenuOpen] = useState(null);

const toggleChatMenu = (chatId) => {
  setChatMenuOpen(chatMenuOpen === chatId ? null : chatId);
};

const handleChatAction = async (chatId, action) => {
  setChatMenuOpen(null);
  
  switch(action) {
    case 'download':
      await exportChatToPDF(chatId);
      break;
    case 'archive':
      // Archive chat logic
      console.log('Archive chat:', chatId);
      alert('Chat archived!');
      break;
    case 'bin':
      // Move to bin logic
      console.log('Move to bin:', chatId);
      alert('Chat moved to bin!');
      break;
    case 'delete':
      if(confirm('Are you sure you want to delete this chat?')) {
        // Delete chat from conversations
        // You'll need to pass a delete function from App.jsx
        console.log('Delete chat:', chatId);
        deleteChat(chatId);
      }
      
      break;
  }
};

// Export chat to PDF
const exportChatToPDF = async (chatId) => {
  const chat = conversations.find(c => c.id === chatId);
  if (!chat) return;
  
  // Import jsPDF library (you'll need to install it)
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();
  
  // Title
  doc.setFontSize(20);
  doc.setTextColor(1, 101, 225);
  doc.text('Portfolio AI - Chat Export', 20, 20);
  
  // Date
  doc.setFontSize(10);
  doc.setTextColor(100, 100, 100);
  doc.text(new Date().toLocaleDateString(), 20, 28);
  
  // Messages
  let yPosition = 40;
  doc.setFontSize(12);
  
  chat.messages.forEach((msg, index) => {
    // Role
    if (msg.role === 'user') {
      doc.setTextColor(1, 101, 225);
    } else {
      doc.setTextColor(16, 185, 129);
    }
    doc.setFont(undefined, 'bold');
    doc.text(msg.role === 'user' ? 'You:' : 'AI:', 20, yPosition);
    
    // Message text
    doc.setTextColor(0, 0, 0);
    doc.setFont(undefined, 'normal');
    const lines = doc.splitTextToSize(msg.text, 170);
    doc.text(lines, 20, yPosition + 5);
    
    yPosition += (lines.length * 5) + 10;
    
    // New page if needed
    if (yPosition > 270) {
      doc.addPage();
      yPosition = 20;
    }
  });
  
  // Save PDF
  doc.save(`chat-${chatId.substring(0, 8)}.pdf`);
  alert('Chat exported as PDF!');
};


  return (
    <aside className={`sidebar ${isOpen ? 'show' : ''}`}>
    

      {/* Profile Card */}
      <div className="profile-card">
        <div className="profile-header">
          <div className="profile-avatar-container">
            <img 
              src={getProfileImage()} 
              alt={name}
              className="profile-avatar"
            />
            <div className="profile-status"></div>
          </div>
          <div className="profile-info">
            <div className="profile-name">{name}</div>
            <div className="profile-role">{role}</div>
          </div>
        </div>

        <div className="profile-details">
          <div className="profile-detail-row">
            <span className="profile-detail-icon">💼</span>
            <span className="profile-detail-text">
              <span className="profile-detail-highlight">{yearsExperience}</span> years experience
            </span>
          </div>

          {companies.length > 0 && (
            <div className="profile-detail-row">
              <span className="profile-detail-icon">🏢</span>
              <div className="profile-detail-text">
                <div className="profile-companies">
                  {displayCompanies.map((company, idx) => (
                    <span key={idx} className="profile-company-badge">
                      {company}
                    </span>
                  ))}
                  {companies.length > 3 && (
                    <span className="profile-company-badge">+{companies.length - 3}</span>
                  )}
                </div>
              </div>
            </div>
          )}

          <div className="profile-detail-row">
            <span className="profile-detail-icon">🎓</span>
            <span className="profile-detail-text">{education}</span>
          </div>
        </div>
      </div>

      <button className="new-chat-btn" onClick={newChat}>New Chat</button>
      <input className="search-input" placeholder="Search chats…" readOnly />

      <div className="library-section">
        <div className="library-header">📚 LIBRARY</div>
        <div className="library-item">FAQ / Sample Prompts</div>
      </div>

      <a className="github-link" href="https://github.com/yourhandle" target="_blank" rel="noreferrer">
        GitHub (@yourhandle)
      </a>

     <div className="chat-list">
  <div className="chat-header">CHATS</div>
  {conversations.map(c => (
    <div 
      key={c.id} 
      className={`chat-item ${c.id === activeId ? 'active' : ''}`}
    >
      <div 
        className="chat-item-content"
        onClick={() => setActiveId(c.id)}
      >
        • {c.messages[0]?.text.slice(0, 28) || 'New chat'}
      </div>
      
      {/* 3-dot menu */}
      <div className="chat-item-actions">
        <button 
          className="chat-actions-btn"
          onClick={(e) => {
            e.stopPropagation();
            toggleChatMenu(c.id);
          }}
        >
          ⋯
        </button>
        
        {chatMenuOpen === c.id && (
          <div className="chat-actions-menu">
            <div 
              className="chat-action-item"
              onClick={(e) => {
                e.stopPropagation();
                handleChatAction(c.id, 'download');
              }}
            >
              📤 Downlaod as PDF
            </div>
            <div 
              className="chat-action-item"
              onClick={(e) => {
                e.stopPropagation();
                handleChatAction(c.id, 'archive');
              }}
            >
              📦 Archive
            </div>
            
            <div 
              className="chat-action-item delete"
              onClick={(e) => {
                e.stopPropagation();
                handleChatAction(c.id, 'delete');
              }}
            >
              ❌ Delete
            </div>
          </div>
        )}
      </div>
    </div>
  ))}
</div>

    </aside>
  );
}