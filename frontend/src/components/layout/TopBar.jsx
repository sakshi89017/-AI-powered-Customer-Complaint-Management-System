import React from 'react';
import { NavLink } from 'react-router-dom';
import './TopBar.css';

export default function TopBar() {
  return (
    <header className="top-bar">
      <div className="top-bar__brand">
        <div className="top-bar__mark">AI</div>
        <div>
          <div className="top-bar__name">AI Customer Complaint Management System</div>
          <div className="top-bar__tagline">PharmaQMS Powered by LangGraph</div>
        </div>
      </div>

      <nav className="top-bar__nav">
        <NavLink
          to="/dashboard"
          className={({ isActive }) => `top-bar__link ${isActive ? 'top-bar__link--active' : ''}`}
        >
          Dashboard
        </NavLink>
        <NavLink
          to="/complaints"
          end
          className={({ isActive }) => `top-bar__link ${isActive ? 'top-bar__link--active' : ''}`}
        >
          Complaints
        </NavLink>
        <NavLink
          to="/complaints/new"
          className={({ isActive }) => `top-bar__link ${isActive ? 'top-bar__link--active' : ''}`}
        >
          New Complaint
        </NavLink>
      </nav>

      <div className="top-bar__meta">
        <span className="top-bar__env-badge" style={{ backgroundColor: '#e2e8f0', color: '#334155' }}>
          QA User
        </span>
      </div>
    </header>
  );
}
