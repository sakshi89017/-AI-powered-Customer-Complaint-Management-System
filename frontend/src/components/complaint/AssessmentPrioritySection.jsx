import React from 'react';
import FormSectionCard from '../common/FormSectionCard.jsx';
import FormField from '../common/FormField.jsx';

const SEVERITY_LEVELS = ['Critical', 'Major', 'Minor'];
const PRIORITY_LEVELS = ['Urgent', 'High', 'Medium', 'Low'];

export default function AssessmentPrioritySection({ values, onFieldChange, highlightedFields = [] }) {
  return (
    <FormSectionCard
      index={4}
      title="Initial Assessment & Priority"
      description="Determine the severity and required response time."
    >
      <FormField
        label="Severity"
        name="severity"
        type="select"
        options={SEVERITY_LEVELS}
        value={values.severity}
        onChange={onFieldChange}
        isHighlighted={highlightedFields.includes('severity')}
        required
      />
      <FormField
        label="Priority"
        name="priority"
        type="select"
        options={PRIORITY_LEVELS}
        value={values.priority}
        onChange={onFieldChange}
        isHighlighted={highlightedFields.includes('priority')}
        required
      />
    </FormSectionCard>
  );
}
