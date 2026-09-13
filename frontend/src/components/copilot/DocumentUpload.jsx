import React, { useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { uploadCopilotDocument } from '../../slices/copilotSlice.js';

export default function DocumentUpload() {
  const dispatch = useDispatch();
  const inputRef = useRef(null);
  const uploadedFiles = useSelector((state) => state.copilot.uploadedFiles);

  const handlePick = () => inputRef.current?.click();

  const handleFileSelected = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      dispatch(uploadCopilotDocument(file));
    }
    e.target.value = '';
  };

  return (
    <div className="doc-upload">
      <input
        ref={inputRef}
        type="file"
        className="doc-upload__hidden-input"
        onChange={handleFileSelected}
        accept=".pdf,.doc,.docx,.png,.jpg,.jpeg"
      />
      <button type="button" className="doc-upload__dropzone" onClick={handlePick}>
        <span className="doc-upload__icon" aria-hidden="true">
          &#8613;
        </span>
        <span>
          <strong>Upload supporting document</strong>
          <br />
          Complaint letter, lab report, or photo (PDF, DOC, PNG, JPG)
        </span>
      </button>

      {uploadedFiles.length > 0 && (
        <ul className="doc-upload__list">
          {uploadedFiles.map((file) => (
            <li key={file.id} className="doc-upload__item">
              <span className="doc-upload__filename">{file.name}</span>
              <span className={`doc-upload__status doc-upload__status--${file.status}`}>
                {file.status === 'uploading' && 'Reading document...'}
                {file.status === 'done' && 'Extraction complete'}
                {file.status === 'error' && 'Unable to process'}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
