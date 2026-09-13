import React from 'react';
import FormSectionCard from '../common/FormSectionCard.jsx';
import FormField from '../common/FormField.jsx';
import './ResolutionSection.css';

const STATUS_OPTIONS = [
  'Pending Triage',
  'Under Investigation',
  'QA Review',
  'Action Required',
  'Closed',
];

export default function ResolutionSection({
  values,
  onFieldChange,
  onSave,
  onReset,
  saveStatus,
  isDirty,
}) {
  const isSaving = saveStatus === 'loading';

  return (
    <FormSectionCard
      title="Resolution & Status"
      description="Track what happens next and the current state of this complaint."
    >
      <FormField
        label="Recommended Actions"
        name="recommendedActions"
        type="textarea"
        placeholder="e.g. Initiate CAPA, retain retention samples, notify QA head..."
        value={values.recommendedActions}
        onChange={onFieldChange}
        fullWidth
        rows={3}
      />
      <FormField
        label="Root Cause"
        name="rootCause"
        type="textarea"
        placeholder="e.g. Seal failure during primary packaging..."
        value={values.rootCause}
        onChange={onFieldChange}
        fullWidth
        rows={3}
      />
      <FormField
        label="CAPA"
        name="capa"
        type="textarea"
        placeholder="e.g. Recalibrate sealing machine temperature..."
        value={values.capa}
        onChange={onFieldChange}
        fullWidth
        rows={3}
      />
      <FormField
        label="Complaint Status"
        name="status"
        type="select"
        options={STATUS_OPTIONS}
        value={values.status}
        onChange={onFieldChange}
      />

      <div className="resolution-actions form-field--full">
        {isDirty && (
          <span className="text-orange-500 font-medium mr-4 text-sm" style={{ alignSelf: 'center' }}>
            Unsaved Changes
          </span>
        )}
        <button
          type="button"
          className="btn btn--ghost"
          onClick={onReset}
          disabled={isSaving}
        >
          Reset
        </button>
        <button
          type="button"
          className="btn btn--primary"
          onClick={onSave}
          disabled={isSaving}
        >
          {isSaving ? 'Saving...' : 'Save Complaint'}
        </button>
      </div>

      {saveStatus === 'succeeded' && (
        <p className="resolution-feedback resolution-feedback--success form-field--full">
          {values.id ? `Complaint ${values.id} saved successfully.` : 'Complaint saved successfully.'}
        </p>
      )}
      {saveStatus === 'failed' && (
        <p className="resolution-feedback resolution-feedback--error form-field--full">
          Could not save the complaint. Check that the backend is running and that Product Name and Complaint Description are provided.
        </p>
      )}
    </FormSectionCard>
  );
}
