import { useState } from 'react';

export function useConversations() {
  const [conversations, setConversations] = useState([]);
  const [activeId, setActiveId] = useState(null);

  const newChat = () => {
    const id = crypto.randomUUID();
    const convo = {
      id,
      messages: [],  // ← Start with empty messages (no mock message)
      activeSection: null
    };
    setConversations(prev => [convo, ...prev]);
    setActiveId(id);
  };

  const append = (id, msg) => {
    setConversations(prev =>
      prev.map(c =>
        c.id === id ? { ...c, messages: [...c.messages, { id: crypto.randomUUID(), ...msg }] } : c
      )
    );
  };

  const setSection = (id, section) => {
    setConversations(prev => prev.map(c => (c.id === id ? { ...c, activeSection: section } : c)));
  };

 const deleteChat = (id) => {
  setConversations(prev => {
    const filtered = prev.filter(c => c.id !== id);
    // ↓ always keep one stub; reuse it if it exists
    if (filtered.length) return filtered;
    return [{ id: crypto.randomUUID(), messages: [] }];
  });

  setActiveId(prevId => {
    const remaining = conversations.filter(c => c.id !== id);
    return remaining.length ? remaining[0].id : conversations[0]?.id;
  });
};

  return { conversations, activeId, setActiveId, newChat, append, setSection, deleteChat};

  



}