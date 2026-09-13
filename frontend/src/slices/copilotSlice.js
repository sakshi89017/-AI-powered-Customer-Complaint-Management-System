import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import copilotApi from '../services/copilotApi.js';
import { applyComplaintAIUpdate } from './complaintSlice.js';

const initialState = {
  messages: [
    {
      id: 'welcome',
      role: 'assistant',
      text: "Hi, I'm your Complaint Co-Pilot. I can help summarize the complaint, suggest a risk level, and recommend next actions.",
      timestamp: null,
    },
  ],
  draftMessage: '',
  chatStatus: 'idle', // idle | loading | failed
  uploadedFiles: [],
  uploadStatus: 'idle',
  riskAssessment: null,
  recommendedAction: null,
};

export const sendCopilotMessage = createAsyncThunk(
  'copilot/sendMessage',
  async (message, { dispatch, getState }) => {
    const { complaint } = getState();
    const currentComplaint = complaint.activeComplaint;
    const complaintId = currentComplaint.id || null;

    const response = await copilotApi.sendMessage(message, currentComplaint, complaintId);
    
    if (response.success && response.tool === 'log_complaint') {
      const result = response.result;
      
      const newUpdates = { ...result.updates };
      if (result.root_cause_recommendation) newUpdates.rootCause = result.root_cause_recommendation;
      if (result.capa_recommendation) newUpdates.capa = result.capa_recommendation;
      dispatch(applyComplaintAIUpdate(newUpdates));
      
      let replyText = "I identified this as a new customer complaint and populated the complaint form.";
      if (result.missing_critical_fields && result.missing_critical_fields.length > 0) {
        replyText += `\n\n⚠️ Please provide the following missing information: ${result.missing_critical_fields.join(', ')}.`;
      }
      if (result.duplicate_warnings && result.duplicate_warnings.length > 0) {
        replyText += `\n\n🛑 ${result.duplicate_warnings.join('\n')}`;
      }
      
      return {
        reply: replyText,
        toolResult: result,
        toolType: 'log_complaint'
      };
    } else if (response.success && response.tool === 'edit_complaint') {
      const result = response.result;
      
      const newUpdates = { ...result.updates };
      if (result.root_cause_recommendation) newUpdates.rootCause = result.root_cause_recommendation;
      if (result.capa_recommendation) newUpdates.capa = result.capa_recommendation;
      
      if (Object.keys(newUpdates).length > 0) {
        dispatch(applyComplaintAIUpdate(newUpdates));
        dispatch({ type: 'complaint/highlightFields', payload: result.changed_fields });
        
        setTimeout(() => {
          dispatch({ type: 'complaint/clearHighlights' });
        }, 5000);
      }

      let replyText = result.message || "Complaint updated. Please review the changes before saving.";
      if (result.duplicate_warnings && result.duplicate_warnings.length > 0) {
        replyText += `\n\n🛑 ${result.duplicate_warnings.join('\n')}`;
      }

      return {
        reply: replyText,
        toolResult: result,
        toolType: 'edit_complaint'
      };
    } else if (response.success && response.tool === 'chat') {
      return {
        reply: response.result.reply,
        toolResult: null,
        toolType: 'chat'
      };
    } else {
      throw new Error(response.result?.error || "Unknown error from AI.");
    }
  }
);

export const uploadCopilotDocument = createAsyncThunk(
  'copilot/uploadDocument',
  async (file, { dispatch, getState }) => {
    const { complaint } = getState();
    const currentComplaint = complaint.activeComplaint;
    const complaintId = currentComplaint.id || null;

    const response = await copilotApi.uploadDocument(file, currentComplaint, complaintId);
    
    if (response.success && response.tool === 'extract_complaint_document') {
      const result = response.result;
      
      const newUpdates = { ...result.updates };
      if (result.root_cause_recommendation) newUpdates.rootCause = result.root_cause_recommendation;
      if (result.capa_recommendation) newUpdates.capa = result.capa_recommendation;
      
      if (Object.keys(newUpdates).length > 0) {
        dispatch(applyComplaintAIUpdate(newUpdates));
        dispatch({ type: 'complaint/highlightFields', payload: result.changed_fields });
        
        setTimeout(() => {
          dispatch({ type: 'complaint/clearHighlights' });
        }, 5000);
      }
      
      return {
        filename: response.filename,
        toolResult: result,
      };
    } else {
      throw new Error(response.result?.error || "Unknown error from Document Extraction.");
    }
  }
);

const copilotSlice = createSlice({
  name: 'copilot',
  initialState,
  reducers: {
    setDraftMessage: (state, action) => {
      state.draftMessage = action.payload;
    },
    appendUserMessage: (state, action) => {
      state.messages.push({
        id: `user-${Date.now()}`,
        role: 'user',
        text: action.payload,
        timestamp: new Date().toISOString(),
      });
      state.draftMessage = '';
    },
    clearChat: (state) => {
      state.messages = initialState.messages;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendCopilotMessage.pending, (state) => {
        state.chatStatus = 'loading';
      })
      .addCase(sendCopilotMessage.fulfilled, (state, action) => {
        state.chatStatus = 'idle';
        
        const newMsg = {
          id: `assistant-${Date.now()}`,
          role: 'assistant',
          text: action.payload.reply,
          timestamp: new Date().toISOString(),
        };
        
        if (action.payload.toolResult) {
          const res = action.payload.toolResult;
          const isEdit = action.payload.toolType === 'edit_complaint';
          
          newMsg.toolData = {
            name: isEdit ? "EDIT COMPLAINT" : "LOG COMPLAINT",
            status: "Completed",
            extractedFields: res.updates || {},
            riskAssessment: res.risk_assessment || (isEdit ? null : undefined),
            recommendedActions: res.recommended_actions || (isEdit ? null : undefined),
            isEdit: isEdit,
            riskChanged: res.risk_changed
          };
          
          if (!isEdit || res.risk_changed) {
            if (res.risk_assessment) {
              state.riskAssessment = {
                level: res.risk_assessment.priority,
                score: res.risk_assessment.severity === 'Critical' ? 90 : res.risk_assessment.severity === 'Major' ? 60 : 30,
                rationale: res.explanation || "Reassessed based on recent edits."
              };
            }
            if (res.recommended_actions && res.recommended_actions.length > 0) {
              state.recommendedAction = {
                title: res.recommended_actions[0],
                description: res.recommended_actions.join(', ')
              };
            }
          }
        }
        
        state.messages.push(newMsg);
      })
      .addCase(sendCopilotMessage.rejected, (state, action) => {
        state.chatStatus = 'failed';
        state.messages.push({
          id: `assistant-error-${Date.now()}`,
          role: 'assistant',
          text: `I couldn't reliably extract the complaint details. Please provide more information.`,
          timestamp: new Date().toISOString(),
        });
      })
      .addCase(uploadCopilotDocument.pending, (state, action) => {
        state.uploadStatus = 'uploading';
      })
      .addCase(uploadCopilotDocument.fulfilled, (state, action) => {
        state.uploadStatus = 'done';
        const res = action.payload.toolResult;
        
        state.uploadedFiles.push({
          id: `file-${Date.now()}`,
          name: action.payload.filename,
          status: 'done'
        });

        let replyText = `Document processed successfully.\n\nThese values have been extracted and applied to the complaint form. Please review before saving.`;
        if (res.missing_critical_fields && res.missing_critical_fields.length > 0) {
          replyText += `\n\n⚠️ Please provide the following missing information: ${res.missing_critical_fields.join(', ')}.`;
        }
        if (res.duplicate_warnings && res.duplicate_warnings.length > 0) {
          replyText += `\n\n🛑 ${res.duplicate_warnings.join('\n')}`;
        }

        const newMsg = {
          id: `assistant-doc-${Date.now()}`,
          role: 'assistant',
          text: replyText,
          timestamp: new Date().toISOString(),
          toolData: {
            name: "EXTRACT DOCUMENT",
            status: "Completed",
            extractedFields: res.updates || {},
            riskAssessment: res.risk_assessment,
            recommendedActions: res.recommended_actions,
            isDocument: true
          }
        };

        if (res.risk_assessment) {
          state.riskAssessment = {
            level: res.risk_assessment.priority,
            score: res.risk_assessment.severity === 'Critical' ? 90 : res.risk_assessment.severity === 'Major' ? 60 : 30,
            rationale: res.explanation || "Extracted from document."
          };
        }
        if (res.recommended_actions && res.recommended_actions.length > 0) {
          state.recommendedAction = {
            title: res.recommended_actions[0],
            description: res.recommended_actions.join(', ')
          };
        }

        state.messages.push(newMsg);
      })
      .addCase(uploadCopilotDocument.rejected, (state, action) => {
        state.uploadStatus = 'error';
        state.messages.push({
          id: `assistant-error-${Date.now()}`,
          role: 'assistant',
          text: `Failed to process document: ${action.error.message}`,
          timestamp: new Date().toISOString(),
        });
      });
  },
});

export const { setDraftMessage, appendUserMessage, clearChat } = copilotSlice.actions;
export default copilotSlice.reducer;
