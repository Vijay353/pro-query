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

  return { conversations, activeId, setActiveId, newChat, append, setSection };
}