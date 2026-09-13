import React, { useEffect, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  setDraftMessage,
  appendUserMessage,
  sendCopilotMessage,
} from '../../slices/copilotSlice.js';
import ChatMessage from './ChatMessage.jsx';
import ChatInput from './ChatInput.jsx';
import DocumentUpload from './DocumentUpload.jsx';
import RiskAssessmentCard from './RiskAssessmentCard.jsx';
import RecommendedActionCard from './RecommendedActionCard.jsx';
import './CopilotPanel.css';

/**
 * AI Complaint Co-Pilot panel.
 *
 * Phase 1: the chat/upload UI is fully wired to Redux and the
 * services/copilotApi.js service, but that service currently returns
 * placeholder/demo data (see the comment at the top of that file). The
 * shape of state (`messages`, `riskAssessment`, `recommendedAction`) is
 * already what a real LangGraph-backed endpoint would need to populate, so
 * no component changes should be needed when that's connected.
 */
export default function CopilotPanel() {
  const dispatch = useDispatch();
  const { messages, draftMessage, chatStatus, riskAssessment, recommendedAction } = useSelector(
    (state) => state.copilot
  );
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, chatStatus]);

  const handleSend = () => {
    const text = draftMessage.trim();
    if (!text) return;
    dispatch(appendUserMessage(text));
    dispatch(sendCopilotMessage(text));
  };

  return (
    <aside className="copilot-panel">
      <header className="copilot-panel__header">
        <div className="copilot-panel__badge">AI</div>
        <div>
          <h3 className="copilot-panel__title">Complaint Co-Pilot</h3>
          <p className="copilot-panel__subtitle">Demo mode &middot; AI engine not yet connected</p>
        </div>
      </header>

      <div className="copilot-panel__chat" ref={scrollRef}>
        {messages.map((m) => (
          <ChatMessage key={m.id} role={m.role} text={m.text} toolData={m.toolData} />
        ))}
        {chatStatus === 'loading' && (
          <ChatMessage role="assistant" text="Thinking..." />
        )}
      </div>

      <ChatInput
        value={draftMessage}
        onChange={(val) => dispatch(setDraftMessage(val))}
        onSend={handleSend}
        disabled={chatStatus === 'loading'}
      />

      <DocumentUpload />

      <div className="copilot-panel__insights">
        <RiskAssessmentCard assessment={riskAssessment} />
        <RecommendedActionCard action={recommendedAction} />
      </div>
    </aside>
  );
}
