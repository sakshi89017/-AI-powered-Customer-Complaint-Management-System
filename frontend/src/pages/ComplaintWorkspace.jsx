import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { fetchComplaintById, fetchComplaintAudit, resetComplaint } from '../slices/complaintSlice.js';
import ComplaintForm from '../components/complaint/ComplaintForm.jsx';
import CopilotPanel from '../components/copilot/CopilotPanel.jsx';
import AuditTrail from '../components/complaint/AuditTrail.jsx';
import './ComplaintWorkspace.css';

export default function ComplaintWorkspace() {
  const { id } = useParams();
  const dispatch = useDispatch();

  useEffect(() => {
    if (id) {
      dispatch(fetchComplaintById(id));
      dispatch(fetchComplaintAudit(id));
    } else {
      dispatch(resetComplaint());
    }
  }, [id, dispatch]);

  return (
    <div className="workspace">
      <div className="workspace__intro">
        <h1 className="workspace__title">{id ? `Complaint ${id}` : 'Complaint Workspace'}</h1>
        <p className="workspace__subtitle">
          {id ? 'Review and update the existing complaint.' : 'Log a new customer complaint on the left.'} The AI Co-Pilot on the right can help
          summarize, assess risk, and recommend next steps.
        </p>
      </div>

      <div className="workspace__columns">
        <div className="workspace__column workspace__column--form">
          <ComplaintForm />
        </div>
        <div className="workspace__column workspace__column--copilot">
          <CopilotPanel />
        </div>
      </div>
      
      {id && (
        <div className="workspace__audit-section">
          <AuditTrail />
        </div>
      )}
    </div>
  );
}
