import apiClient from './apiClient.js';

const DEMO_LATENCY_MS = 700;

const copilotApi = {
  async sendMessage(message, current_complaint = null, complaint_id = null) {
    const payload = {
      message,
      current_complaint,
      complaint_id
    };
    const { data } = await apiClient.post('/ai/chat', payload);
    return data;
  },

  async uploadDocument(file, currentComplaint, complaintId) {
    const formData = new FormData();
    formData.append('file', file);
    if (complaintId) {
      formData.append('complaint_id', complaintId);
    }
    if (currentComplaint) {
      formData.append('current_complaint', JSON.stringify(currentComplaint));
    }
    
    const { data } = await apiClient.post('/ai/extract-document', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return data;
  },
};

export default copilotApi;
