import React from 'react';
import { useSelector } from 'react-redux';
import './AuditTrail.css';

export default function AuditTrail() {
  const auditEvents = useSelector((state) => state.complaint.activeComplaintAudit);

  if (!auditEvents || auditEvents.length === 0) {
    return (
      <div className="audit-trail empty-state">
        <h2 className="audit-trail__title">Audit Trail</h2>
        <p className="empty-state__text">No activity recorded yet.</p>
      </div>
    );
  }

  return (
    <div className="audit-trail">
      <h2 className="audit-trail__title">Audit Trail</h2>
      <div className="audit-trail__list">
        {auditEvents.map((event) => (
          <div key={event.id} className="audit-event">
            <div className="audit-event__header">
              <span className="audit-event__time">
                {new Date(event.timestamp).toLocaleString()}
              </span>
              <span className={`audit-event__type audit-event__type--${event.event_type.toLowerCase()}`}>
                {event.event_type}
              </span>
              <span className="audit-event__user">
                {event.user_id ? event.user_id : 'System / AI'}
              </span>
            </div>
            
            {event.changed_fields && event.changed_fields.length > 0 && (
              <div className="audit-event__changes">
                <strong>Changed Fields:</strong> {event.changed_fields.join(', ')}
                
                <div className="audit-event__details">
                  {event.changed_fields.map((field) => {
                    const oldVal = event.previous_values?.[field] || 'None';
                    const newVal = event.new_values?.[field] || 'None';
                    return (
                      <div key={field} className="audit-event__change-item">
                        <span className="audit-event__field">{field}:</span>
                        <span className="audit-event__old-val">{oldVal}</span>
                        <span className="audit-event__arrow">→</span>
                        <span className="audit-event__new-val">{newVal}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
