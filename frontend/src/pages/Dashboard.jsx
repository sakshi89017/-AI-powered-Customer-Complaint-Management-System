import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchDashboardStats, fetchComplaints } from '../slices/complaintSlice';
import { Link, useNavigate } from 'react-router-dom';
import './Dashboard.css';

export default function Dashboard() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { dashboardStats, complaints, status, error } = useSelector((state) => state.complaint);

  useEffect(() => {
    dispatch(fetchDashboardStats());
    dispatch(fetchComplaints());
  }, [dispatch]);

  const stats = dashboardStats || {
    total_complaints: 0,
    pending_triage: 0,
    under_investigation: 0,
    qa_review: 0,
    action_required: 0,
    closed: 0,
    critical_complaints: 0,
    high_priority: 0,
  };

  const recentComplaints = [...complaints].slice(0, 5); // top 5 recent

  return (
    <div className="dashboard">
      <div className="dashboard__header">
        <h1 className="dashboard__title">Quality Assurance Dashboard</h1>
        <p className="dashboard__subtitle">Real-time overview of customer complaints</p>
      </div>

      {status === 'failed' && (
        <div className="dashboard__error-banner">
          <p>Unable to connect to the server. Please try again. ({error})</p>
        </div>
      )}

      {status === 'loading' && (
        <div className="dashboard__loading">
          <p>Loading dashboard...</p>
        </div>
      )}

      <div className="dashboard__grid">
        <div className="dashboard__card dashboard__card--primary">
          <div className="dashboard__card-title">Total Complaints</div>
          <div className="dashboard__card-value">{stats.total_complaints}</div>
        </div>

        <div className="dashboard__card dashboard__card--critical">
          <div className="dashboard__card-title">Critical Severity</div>
          <div className="dashboard__card-value">{stats.critical_complaints}</div>
        </div>

        <div className="dashboard__card dashboard__card--high">
          <div className="dashboard__card-title">High Priority</div>
          <div className="dashboard__card-value">{stats.high_priority}</div>
        </div>
      </div>

      <div className="dashboard__split">
        <div className="dashboard__split-left">
          <h2 className="dashboard__section-title">Workflow Status</h2>
          <div className="dashboard__grid dashboard__grid--small">
            <div className="dashboard__card">
              <div className="dashboard__card-title">Pending Triage</div>
              <div className="dashboard__card-value">{stats.pending_triage}</div>
            </div>
            <div className="dashboard__card">
              <div className="dashboard__card-title">Under Investigation</div>
              <div className="dashboard__card-value">{stats.under_investigation}</div>
            </div>
            <div className="dashboard__card">
              <div className="dashboard__card-title">QA Review</div>
              <div className="dashboard__card-value">{stats.qa_review}</div>
            </div>
            <div className="dashboard__card">
              <div className="dashboard__card-title">Action Required</div>
              <div className="dashboard__card-value">{stats.action_required}</div>
            </div>
            <div className="dashboard__card">
              <div className="dashboard__card-title">Closed</div>
              <div className="dashboard__card-value">{stats.closed}</div>
            </div>
          </div>
        </div>
        
        <div className="dashboard__split-right">
          <h2 className="dashboard__section-title">Quick Actions</h2>
          <div className="dashboard__actions-vertical">
            <Link to="/complaints/new" className="btn btn--primary">Log New Complaint</Link>
            <Link to="/complaints" className="btn btn--ghost">View All Complaints</Link>
          </div>
        </div>
      </div>

      <h2 className="dashboard__section-title" style={{ marginTop: '2rem' }}>Recent Complaints</h2>
      <div className="dashboard__recent-table-container">
        {recentComplaints.length > 0 ? (
          <table className="complaints-table dashboard__recent-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Date</th>
                <th>Customer</th>
                <th>Product</th>
                <th>Batch</th>
                <th>Severity</th>
                <th>Priority</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {recentComplaints.map(c => (
                <tr key={c.id} onClick={() => navigate(`/complaints/${c.id}`)}>
                  <td className="font-medium">{c.id}</td>
                  <td>{c.createdAt ? new Date(c.createdAt).toLocaleDateString() : '—'}</td>
                  <td>{c.customerName || '—'}</td>
                  <td>{c.productName || '—'}</td>
                  <td>{c.batchNumber || '—'}</td>
                  <td>{c.initialSeverity || '—'}</td>
                  <td>{c.priority || '—'}</td>
                  <td>
                    <span className={`status-badge status-badge--${(c.status || '').replace(/\s+/g, '-').toLowerCase()}`}>
                      {c.status || '—'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div className="empty-state">
            <p>No customer complaints yet.</p>
          </div>
        )}
      </div>
    </div>
  );
}
