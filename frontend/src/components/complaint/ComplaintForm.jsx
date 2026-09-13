import React, { useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setField, resetComplaint, saveComplaint, clearHighlights } from '../../slices/complaintSlice.js';
import OriginCustomerSection from './OriginCustomerSection.jsx';
import ProductBatchSection from './ProductBatchSection.jsx';
import ComplaintDetailsSection from './ComplaintDetailsSection.jsx';
import AssessmentPrioritySection from './AssessmentPrioritySection.jsx';
import ResolutionSection from './ResolutionSection.jsx';
import './ComplaintForm.css';

/**
 * The full Customer Complaint Form. This component holds NO field state
 * itself — every value comes from `state.complaint.activeComplaint` in
 * Redux, and every edit dispatches `setField`. This satisfies the
 * requirement that the active complaint lives in one place (the store),
 * not scattered across component state.
 */
export default function ComplaintForm() {
  const dispatch = useDispatch();
  const activeComplaint = useSelector((state) => state.complaint.activeComplaint);
  const saveStatus = useSelector((state) => state.complaint.saveStatus);
  const highlightedFields = useSelector((state) => state.complaint.highlightedFields);

  const handleFieldChange = useCallback(
    (field, value) => {
      dispatch(setField({ field, value }));
      if (highlightedFields.length > 0) {
        dispatch(clearHighlights());
      }
    },
    [dispatch, highlightedFields]
  );

  const handleSave = () => {
    dispatch(saveComplaint(activeComplaint));
  };

  const handleReset = () => {
    dispatch(resetComplaint());
  };

  return (
    <div className="complaint-form">
      <OriginCustomerSection values={activeComplaint} onFieldChange={handleFieldChange} highlightedFields={highlightedFields} />
      <ProductBatchSection values={activeComplaint} onFieldChange={handleFieldChange} highlightedFields={highlightedFields} />
      <ComplaintDetailsSection values={activeComplaint} onFieldChange={handleFieldChange} highlightedFields={highlightedFields} />
      <AssessmentPrioritySection values={activeComplaint} onFieldChange={handleFieldChange} highlightedFields={highlightedFields} />
      <ResolutionSection
        values={activeComplaint}
        onFieldChange={handleFieldChange}
        onSave={handleSave}
        onReset={handleReset}
        saveStatus={saveStatus}
        isDirty={useSelector((state) => state.complaint.isDirty)}
      />
    </div>
  );
}
