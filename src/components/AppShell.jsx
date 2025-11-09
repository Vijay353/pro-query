import React, { useContext } from 'react';
import { AppCtx } from '../App';
import Sidebar from './Sidebar';
import HeaderBar from './HeaderBar';
import Composer from './Composer';
import ChatWindow from './ChatWindow';

export function AppShell() {
  const { sidebarOpen, toggleSidebar } = useContext(AppCtx);

  return (
    <div className="app-shell">
      <HeaderBar onMenu={toggleSidebar} />
      <Sidebar isOpen={sidebarOpen} />
      <main className="main">
        <ChatWindow />
        <Composer />
      </main>
    </div>
  );
}