import React from 'react';
import FormSectionCard from '../common/FormSectionCard.jsx';
import FormField from '../common/FormField.jsx';

export default function ProductBatchSection({ values, onFieldChange, highlightedFields = [] }) {
  return (
    <FormSectionCard
      index={2}
      title="Product & Batch Identification"
      description="Identify the exact product and batch involved in the complaint."
    >
      <FormField
        label="Product Name"
        name="productName"
        placeholder="e.g. Amoxicillin Capsules"
        value={values.productName}
        onChange={onFieldChange}
        isHighlighted={highlightedFields.includes('productName')}
        required
      />
      <FormField
        label="Product Strength / Grade"
        name="productStrength"
        placeholder="e.g. 500 mg"
        value={values.productStrength}
        onChange={onFieldChange}
        isHighlighted={highlightedFields.includes('productStrength')}
      />
      <FormField
        label="Batch / Lot Number"
        name="batchNumber"
        placeholder="e.g. B24-00981"
        value={values.batchNumber}
        onChange={onFieldChange}
        isHighlighted={highlightedFields.includes('batchNumber')}
        required
      />
      <FormField
        label="Quantity Affected"
        name="quantityAffected"
        placeholder="e.g. 200 units"
        value={values.quantityAffected}
        onChange={onFieldChange}
        isHighlighted={highlightedFields.includes('quantityAffected')}
      />
      <FormField
        label="Manufacturing Date"
        name="manufacturingDate"
        type="date"
        value={values.manufacturingDate}
        onChange={onFieldChange}
        isHighlighted={highlightedFields.includes('manufacturingDate')}
      />
      <FormField
        label="Expiry Date"
        name="expiryDate"
        type="date"
        value={values.expiryDate}
        onChange={onFieldChange}
        isHighlighted={highlightedFields.includes('expiryDate')}
      />
    </FormSectionCard>
  );
}
