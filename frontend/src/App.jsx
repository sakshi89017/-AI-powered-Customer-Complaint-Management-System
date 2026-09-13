import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import TopBar from './components/layout/TopBar.jsx';
import Dashboard from './pages/Dashboard.jsx';
import ComplaintWorkspace from './pages/ComplaintWorkspace.jsx';
import ComplaintsList from './pages/ComplaintsList.jsx';
import NotFound from './pages/NotFound.jsx';

export default function App() {
  return (
    <div className="app-shell">
      <TopBar />
      <main>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/complaints" element={<ComplaintsList />} />
          <Route path="/complaints/new" element={<ComplaintWorkspace />} />
          <Route path="/complaints/:id" element={<ComplaintWorkspace />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
    </div>
  );
}
