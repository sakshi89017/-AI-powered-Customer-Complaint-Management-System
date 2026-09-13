import React from 'react';
import './FormSectionCard.css';

/**
 * Numbered card wrapper for each part of the complaint form. Numbering is
 * meaningful here (the QMS process genuinely runs 1 -> 4), unlike decorative
 * step numbers, so it doubles as a progress cue for the person filling the
 * form.
 */
export default function FormSectionCard({ index, title, description, children }) {
  return (
    <section className="form-section">
      <header className="form-section__header">
        {index && <span className="form-section__index">{index}</span>}
        <div>
          <h3 className="form-section__title">{title}</h3>
          {description && <p className="form-section__description">{description}</p>}
        </div>
      </header>
      <div className="form-section__grid">{children}</div>
    </section>
  );
}
