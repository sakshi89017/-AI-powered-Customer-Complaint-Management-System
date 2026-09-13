import React from 'react';
import './FormField.css';

/**
 * A single labeled form control. Purely presentational — the parent
 * (ComplaintForm section components) supplies `value` from Redux state and
 * an `onChange` that dispatches setField. This component holds no state of
 * its own, per the requirement that the complaint record lives only in Redux.
 */
export default function FormField({
  label,
  name,
  type = 'text',
  value,
  onChange,
  placeholder,
  options,
  required = false,
  rows,
  fullWidth = false,
  isHighlighted = false,
}) {
  const handleChange = (e) => onChange(name, e.target.value);

  return (
    <div className={`form-field ${fullWidth ? 'form-field--full' : ''} ${isHighlighted ? 'form-field--highlighted' : ''}`}>
      <label className="form-field__label" htmlFor={name}>
        {label}
        {required && <span className="form-field__required">*</span>}
        {isHighlighted && <span className="form-field__ai-badge">AI Updated</span>}
      </label>

      {type === 'select' && (
        <select
          id={name}
          name={name}
          className="form-field__control"
          value={value}
          onChange={handleChange}
        >
          <option value="" disabled>
            Select {label.toLowerCase()}
          </option>
          {options.map((opt) => (
            <option key={opt} value={opt}>
              {opt}
            </option>
          ))}
        </select>
      )}

      {type === 'textarea' && (
        <textarea
          id={name}
          name={name}
          className="form-field__control form-field__control--textarea"
          value={value}
          onChange={handleChange}
          placeholder={placeholder}
          rows={rows || 4}
        />
      )}

      {type !== 'select' && type !== 'textarea' && (
        <input
          id={name}
          name={name}
          type={type}
          className="form-field__control"
          value={value}
          onChange={handleChange}
          placeholder={placeholder}
        />
      )}
    </div>
  );
}
