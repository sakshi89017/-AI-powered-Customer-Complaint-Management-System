import React from 'react';
import FormSectionCard from '../common/FormSectionCard.jsx';
import FormField from '../common/FormField.jsx';

const COMPLAINT_SOURCES = [
  'Phone Call',
  'Email',
  'Company Website',
  'Sales Representative',
  'Distributor / Wholesaler',
  'Regulatory Authority',
  'Healthcare Professional',
  'Other',
];

export default function OriginCustomerSection({ values, onFieldChange, highlightedFields = [] }) {
  return (
    <FormSectionCard
      index={1}
      title="Origin & Customer Details"
      description="Record where the complaint came from and who reported it."
    >
      <FormField
        label="Complaint Source"
        name="complaintSource"
        type="select"
        value={values.complaintSource}
        onChange={onFieldChange}
        options={['Customer', 'Email', 'Phone', 'Web Portal', 'Distributor', 'Other']}
        isHighlighted={highlightedFields.includes('complaintSource')}
      />
      <FormField
        label="Customer Name / Reporter"
        name="customerName"
        placeholder="e.g. John Doe, ABC Healthcare"
        value={values.customerName}
        onChange={onFieldChange}
        fullWidth
        isHighlighted={highlightedFields.includes('customerName')}
      />
    </FormSectionCard>
  );
}
