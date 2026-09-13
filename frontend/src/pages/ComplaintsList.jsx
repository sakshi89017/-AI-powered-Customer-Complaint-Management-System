import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { fetchComplaints, fetchComplaintById, deleteComplaint } from '../slices/complaintSlice.js';
import './ComplaintsList.css';

export default function ComplaintsList() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { complaints, status, error } = useSelector((state) => state.complaint);

  const [searchTerm, setSearchTerm] = useState('');
  const [filterSeverity, setFilterSeverity] = useState('All');
  const [filterPriority, setFilterPriority] = useState('All');
  const [filterStatus, setFilterStatus] = useState('All');

  useEffect(() => {
    dispatch(fetchComplaints());
  }, [dispatch]);

  const openComplaint = async (id) => {
    await dispatch(fetchComplaintById(id));
    navigate(`/complaints/${id}`);
  };

  const handleDelete = async (e, id) => {
    e.stopPropagation();
    if (window.confirm(`Are you sure you want to delete complaint ${id}?`)) {
      await dispatch(deleteComplaint(id));
    }
  };

  // Local filtering (since our backend list endpoint doesn't strictly take these params in the slice yet,
  // we do a quick local filter for the UI prototype).
  const filteredComplaints = complaints.filter((c) => {
    const matchesSearch = 
      searchTerm === '' ||
      (c.id && c.id.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (c.customerName && c.customerName.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (c.productName && c.productName.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (c.batchNumber && c.batchNumber.toLowerCase().includes(searchTerm.toLowerCase()));

    const matchesSeverity = filterSeverity === 'All' || c.initialSeverity === filterSeverity;
    const matchesPriority = filterPriority === 'All' || c.priority === filterPriority;
    const matchesStatus = filterStatus === 'All' || c.status === filterStatus;

    return matchesSearch && matchesSeverity && matchesPriority && matchesStatus;
  });

  return (
    <div className="complaints-list">
      <div className="complaints-list__header">
        <div>
          <h1 className="complaints-list__title">All Complaints</h1>
          <p className="complaints-list__subtitle">Records managed in PostgreSQL.</p>
        </div>
        <button className="btn btn--primary" onClick={() => navigate('/complaints/new')}>
          Log New Complaint
        </button>
      </div>

      <div className="complaints-list__filters">
        <input
          type="text"
          placeholder="Search ID, Customer, Product, Batch..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="form-input"
        />
        <select value={filterSeverity} onChange={(e) => setFilterSeverity(e.target.value)} className="form-input">
          <option value="All">All Severities</option>
          <option value="Minor">Minor</option>
          <option value="Major">Major</option>
          <option value="Critical">Critical</option>
        </select>
        <select value={filterPriority} onChange={(e) => setFilterPriority(e.target.value)} className="form-input">
          <option value="All">All Priorities</option>
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
          <option value="Urgent">Urgent</option>
        </select>
        <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)} className="form-input">
          <option value="All">All Statuses</option>
          <option value="Pending Triage">Pending Triage</option>
          <option value="Under Investigation">Under Investigation</option>
          <option value="QA Review">QA Review</option>
          <option value="Action Required">Action Required</option>
          <option value="Closed">Closed</option>
        </select>
      </div>

      {status === 'loading' && <p className="complaints-list__state">Loading complaints...</p>}
      {status === 'failed' && (
        <p className="complaints-list__state complaints-list__state--error">
          Could not reach the backend ({error}). Make sure the FastAPI server is running.
        </p>
      )}
      {status === 'succeeded' && complaints.length === 0 && (
        <p className="complaints-list__state">
          No complaints found. Create one from the Dashboard or New Complaint page.
        </p>
      )}

      {complaints.length > 0 && (
        <table className="complaints-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer</th>
              <th>Product</th>
              <th>Batch</th>
              <th>Type</th>
              <th>Severity</th>
              <th>Priority</th>
              <th>Status</th>
              <th>Date</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredComplaints.map((c) => (
              <tr key={c.id} onClick={() => openComplaint(c.id)}>
                <td className="font-medium">{c.id}</td>
                <td>{c.customerName || '—'}</td>
                <td>{c.productName || '—'}</td>
                <td>{c.batchNumber || '—'}</td>
                <td>{c.complaintType || '—'}</td>
                <td>
                  <span className={`severity-badge severity-badge--${(c.initialSeverity || '').toLowerCase()}`}>
                    {c.initialSeverity || '—'}
                  </span>
                </td>
                <td>{c.priority || '—'}</td>
                <td>
                  <span className={`status-badge status-badge--${(c.status || '').replace(/\s+/g, '-').toLowerCase()}`}>
                    {c.status || '—'}
                  </span>
                </td>
                <td>{c.createdAt ? new Date(c.createdAt).toLocaleDateString() : '—'}</td>
                <td>
                  <button className="btn-icon text-red-500" onClick={(e) => handleDelete(e, c.id)} title="Delete Complaint">
                    &times;
                  </button>
                </td>
              </tr>
            ))}
            {filteredComplaints.length === 0 && (
              <tr>
                <td colSpan="10" className="text-center py-4">No complaints match your filters.</td>
              </tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}
