import React from 'react';

export default function ChatMessage({ role, text, toolData }) {
  const isAssistant = role === 'assistant';
  return (
    <div className={`chat-message ${isAssistant ? 'chat-message--assistant' : 'chat-message--user'}`}>
      {isAssistant && <div className="chat-message__avatar">AI</div>}
      <div className="chat-message__bubble">
        {text && <div className="chat-message__text">{text}</div>}
        
        {toolData && (
          <div className="chat-message__tool-card">
            <div className="chat-message__tool-header">
              <span className="chat-message__tool-title">AI Action Completed</span>
            </div>
            
            <div className="chat-message__tool-body">
              <div className="chat-message__tool-section">
                <span className="font-medium text-muted">Tool:</span> 
                <span className="chat-message__tool-badge">{toolData.name.toUpperCase()}</span>
              </div>
              
              {toolData.isDocument && (
                <div className="chat-message__tool-section italic text-muted">
                  Source: Uploaded Document
                </div>
              )}
              
              {toolData.extractedFields && Object.keys(toolData.extractedFields).length > 0 && (
                <div className="chat-message__tool-section">
                  <div className="font-medium">Extracted / Updated:</div>
                  <ul className="chat-message__tool-list">
                    {Object.entries(toolData.extractedFields).map(([k, v]) => (
                      v !== null && (
                        <li key={k}>
                          <strong className="capitalize">{k.replace(/_/g, ' ')}:</strong> {v}
                        </li>
                      )
                    ))}
                  </ul>
                </div>
              )}
              
              {toolData.riskAssessment && (
                <div className="chat-message__tool-section chat-message__risk-section">
                  <div className="font-medium">Risk Assessment:</div>
                  <div className="chat-message__risk-values">
                    <span><strong>Severity:</strong> {toolData.riskAssessment.severity}</span>
                    <span><strong>Priority:</strong> {toolData.riskAssessment.priority}</span>
                  </div>
                  <div className="chat-message__disclaimer">
                    ⚠️ AI-generated assessment requires review by authorized Quality personnel.
                  </div>
                </div>
              )}
              
              {toolData.recommendedActions && toolData.recommendedActions.length > 0 && (
                <div className="chat-message__tool-section">
                  <div className="font-medium">Recommended Action:</div>
                  <div>{toolData.recommendedActions.join(', ')}</div>
                </div>
              )}
            </div>
            
            <div className="chat-message__tool-footer">
              ✓ These values have been applied to the complaint form. Please review before saving.
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
