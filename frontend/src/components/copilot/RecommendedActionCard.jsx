import React from 'react';

export default function RecommendedActionCard({ action }) {
  if (!action) {
    return (
      <div className="insight-card insight-card--empty">
        <h4 className="insight-card__title">Recommended Action</h4>
        <p className="insight-card__empty-text">
          Recommendations will appear here once the co-pilot has enough context.
        </p>
      </div>
    );
  }

  return (
    <div className="insight-card insight-card--accent">
      <h4 className="insight-card__title">Recommended Action</h4>
      <p className="insight-card__action-title">{action.title}</p>
      <p className="insight-card__body">{action.description}</p>
    </div>
  );
}
