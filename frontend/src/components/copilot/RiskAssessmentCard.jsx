import React from 'react';

const LEVEL_CLASS = {
  Critical: 'risk-card--critical',
  High: 'risk-card--high',
  Medium: 'risk-card--medium',
  Low: 'risk-card--low',
};

export default function RiskAssessmentCard({ assessment }) {
  if (!assessment) {
    return (
      <div className="insight-card insight-card--empty">
        <h4 className="insight-card__title">Risk Assessment</h4>
        <p className="insight-card__empty-text">
          Send a message or upload a document to generate a risk assessment.
        </p>
      </div>
    );
  }

  const levelClass = LEVEL_CLASS[assessment.level] || 'risk-card--medium';

  return (
    <div className={`insight-card ${levelClass}`}>
      <div className="insight-card__row">
        <h4 className="insight-card__title">Risk Assessment</h4>
        <span className="insight-card__badge">{assessment.level}</span>
      </div>
      <div className="risk-card__score">
        <div className="risk-card__score-bar">
          <div
            className="risk-card__score-fill"
            style={{ width: `${assessment.score}%` }}
          />
        </div>
        <span className="risk-card__score-value">{assessment.score}/100</span>
      </div>
      <p className="insight-card__body">{assessment.rationale}</p>
    </div>
  );
}
