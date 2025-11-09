import React, { useEffect, useMemo, createContext } from 'react';
import { AppShell } from './components/AppShell';
import ChatWindow from './components/ChatWindow';
import Composer from './components/Composer';
import { useConversations } from './state/useConversations';
import { apiChat } from './lib/apiClient';  // ← Import API client

export const AppCtx = createContext(null);

export default function App() {
  const store = useConversations();
  const activeConvo = useMemo(
    () => store.conversations.find(c => c.id === store.activeId),
    [store.conversations, store.activeId]
  );

  // Ensure there is always a conversation
  useEffect(() => {
    if (store.conversations.length === 0) {
      store.newChat();
    }
  }, [store.conversations.length]);

  // Quick ask handler that calls the API
  const quickAsk = async (question) => {
    if (!activeConvo) return;
    
    // Add user message
    store.append(activeConvo.id, { role: 'user', text: question });
    
    // Call API
    try {
      const response = await apiChat({
        question,
        section: activeConvo.activeSection,
        conversationId: activeConvo.id
      });
      
      // Add assistant response
      store.append(activeConvo.id, {
        role: 'assistant',
        text: response.answer,
        chips: response.chips || [],
        links: response.links || []
      });
    } catch (error) {
      console.error('Quick ask error:', error);
      store.append(activeConvo.id, {
        role: 'assistant',
        text: `⚠️ Error: ${error.message}`,
        chips: ['Error'],
        links: []
      });
    }
  };

  return (
    <AppCtx.Provider value={{ ...store, activeConvo, quickAsk }}>
      <AppShell>
        {activeConvo ? (
          <ChatWindow
            messages={activeConvo.messages}
            onQuickAsk={quickAsk}  // ← Pass the real handler
          />
        ) : (
          <div className="chat-window" />
        )}
        <Composer />
      </AppShell>
    </AppCtx.Provider>
  );
}