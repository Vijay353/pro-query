import React, { useEffect, useMemo, createContext, useState } from 'react';
import { AppShell } from './components/AppShell';
import HeaderBar from './components/HeaderBar';
import ChatWindow from './components/ChatWindow';
import Composer from './components/Composer';
import Sidebar from './components/Sidebar';
import { useConversations } from './state/useConversations';
import { apiChat, apiSections } from './lib/apiClient';

export const AppCtx = createContext(null);

export default function App() {
  const store = useConversations();
  const [profileData, setProfileData] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const activeConvo = useMemo(
    () => store.conversations.find(c => c.id === store.activeId),
    [store.conversations, store.activeId]
  );

  /* ---------- load profile ---------- */
  useEffect(() => {
    const loadProfile = async () => {
      try {
        const data = await apiSections();
        setProfileData({
          name: data.about?.name || 'John Doe',
          role: data.about?.role || 'Data Scientist',
          yearsExperience: calculateYears(data.experience),
          companies: extractCompanies(data.experience),
          education: data.education?.[0]?.degree || 'MS in Computer Science',
          profileImage: data.about?.profileImage || null,
          gender: data.about?.gender || 'neutral'
        });
      } catch (e) {
        console.error('Failed to load profile:', e);
        setProfileData({
          name: 'John Doe',
          role: 'Data Scientist',
          yearsExperience: '5+',
          companies: ['Company A', 'Company B'],
          education: 'MS in Computer Science',
          profileImage: null,
          gender: 'neutral'
        });
      }
    };
    loadProfile();
  }, []);

  const calculateYears = (exp) => {
    if (!exp?.length) return '5+';
    const first = new Date(exp[exp.length - 1].startDate).getFullYear();
    return `${new Date().getFullYear() - first}+`;
  };

  const extractCompanies = (exp) => (exp?.length ? exp.map(j => j.company) : []);

  /* ---------- quick ask ---------- */
  const quickAsk = async (question) => {
    if (!activeConvo) return;
    store.append(activeConvo.id, { role: 'user', text: question });
    try {
      const res = await apiChat({ question, section: null, conversationId: activeConvo.id });
      store.append(activeConvo.id, {
        role: 'assistant',
        text: res.answer,
        chips: res.chips || [],
        links: res.links || []
      });
    } catch (err) {
      store.append(activeConvo.id, {
        role: 'assistant',
        text: `⚠️ Error: ${err.message}`,
        chips: ['Error'],
        links: []
      });
    }
  };

  const toggleSidebar = () => setSidebarOpen(p => !p);

  /* ---------- UI ---------- */
  return (
    <AppCtx.Provider value={{ ...store, activeConvo, quickAsk, sidebarOpen, toggleSidebar }}>
      <div className="app-shell">
        <header className="header">
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
           {/* <button className="btn mobile-only" onClick={toggleSidebar}>☰</button> */}
            <div className="header-title">Portfolio AI</div>
          </div>
          <div className="header-actions">
            <button className="btn">Share</button>
            <button className="btn">Profile</button>
          </div>
        </header>

        <Sidebar isOpen={sidebarOpen} profileData={profileData} />

        <main className="main">
          {activeConvo ? (
            <>
              <ChatWindow
                messages={activeConvo.messages}
                onQuickAsk={quickAsk}
                profileImage={profileData?.profileImage}
                gender={profileData?.gender}
              />
              <Composer />
            </>
          ) : (
            <div className="chat-container empty-state">
              <div style={{ margin: 'auto', textAlign: 'center', color: 'var(--text-muted)' }}>
                <h3>Hello!</h3>
                <button className="btn" onClick={store.newChat}>Start a new chat</button>
              </div>
            </div>
          )}
        </main>
      </div>
    </AppCtx.Provider>
  );
}