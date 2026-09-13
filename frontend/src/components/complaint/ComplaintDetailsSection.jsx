import React from 'react';
import FormSectionCard from '../common/FormSectionCard.jsx';
import FormField from '../common/FormField.jsx';

const COMPLAINT_TYPES = [
  'Product Quality Defect',
  'Adverse Event / Reaction',
  'Packaging Defect',
  'Labeling Issue',
  'Suspected Contamination',
  'Efficacy Concern',
  'Counterfeit Suspicion',
  'Other',
];

export default function ComplaintDetailsSection({ values, onFieldChange, highlightedFields = [] }) {
  return (
    <FormSectionCard
      index={3}
      title="Complaint Details"
      description="Categorize the issue and provide a comprehensive description."
    >
      <FormField
        label="Complaint Date"
        name="complaintDate"
        type="date"
        value={values.complaintDate}
        onChange={onFieldChange}
        isHighlighted={highlightedFields.includes('complaintDate')}
        required
      />
      <FormField
        label="Complaint Type"
        name="complaintType"
        type="select"
        options={COMPLAINT_TYPES}
        value={values.complaintType}
        onChange={onFieldChange}
        isHighlighted={highlightedFields.includes('complaintType')}
        required
      />
      <FormField
        label="Description"
        name="description"
        type="textarea"
        placeholder="Provide full details of the reported issue..."
        value={values.description}
        onChange={onFieldChange}
        fullWidth
        isHighlighted={highlightedFields.includes('description')}
        required
      />
    </FormSectionCard>
  );
}
