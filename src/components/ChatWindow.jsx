import React, { useContext, useEffect, useRef, useState } from 'react';
import { AppCtx } from '../App';
import MessageItem from './MessageItem';
import Welcome from './Welcome';

export default function ChatWindow(){
  const { activeConvo, quickAsk } = useContext(AppCtx);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  
  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [activeConvo?.messages]);

  // Check if assistant is typing (last message is user message)
  useEffect(() => {
    if (!activeConvo) return;
    const lastMsg = activeConvo.messages[activeConvo.messages.length - 1];
    setIsTyping(lastMsg?.role === 'user');
    
    // Hide typing indicator after 5 seconds (safety)
    if (lastMsg?.role === 'user') {
      const timer = setTimeout(() => setIsTyping(false), 5000);
      return () => clearTimeout(timer);
    }
  }, [activeConvo?.messages]);

  if (!activeConvo) return <div className="chat-container"/>;

  const showWelcome = activeConvo.messages.filter(m=>m.role==='user').length === 0;

  return (
    <div className="chat-container">
      <div className="messages" id="messages">
        {showWelcome && <Welcome onAsk={quickAsk} />}
        {!showWelcome && activeConvo.messages.map(m=>
          <MessageItem 
            key={m.id} 
            role={m.role} 
            text={m.text} 
            links={m.links} 
            chips={m.chips} 
          />
        )}
        {isTyping && <TypingIndicator />}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}

/*  Typing indicator  */
const TypingIndicator = () => (
  <div className="typing-indicator show">
    <div className="message">
      <div className="message-avatar assistant-avatar">AI</div>
      <div className="message-content">
        <span>Thinking</span>
        <div className="typing-dots">
          <div className="dot"></div>
          <div className="dot"></div>
          <div className="dot"></div>
        </div>
      </div>
    </div>
  </div>
);