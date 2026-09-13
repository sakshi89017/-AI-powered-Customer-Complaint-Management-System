import React from 'react';
import { Link } from 'react-router-dom';

export default function NotFound() {
  return (
    <div style={{ padding: 60, textAlign: 'center' }}>
      <h1 style={{ fontSize: 22, marginBottom: 8 }}>Page not found</h1>
      <p style={{ color: 'var(--color-ink-muted)', marginBottom: 20 }}>
        The page you&apos;re looking for doesn&apos;t exist.
      </p>
      <Link to="/" style={{ color: 'var(--color-primary)', fontWeight: 600 }}>
        Return to Complaint Workspace
      </Link>
    </div>
  );
}
