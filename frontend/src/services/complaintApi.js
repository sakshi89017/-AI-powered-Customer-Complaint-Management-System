import apiClient from './apiClient.js';

/**
 * Thin wrapper around the /api/complaints endpoints. Keeping every request
 * in one place means the Redux slice (and any future component) never
 * constructs a URL itself, and swapping in-memory storage for PostgreSQL on
 * the backend requires zero frontend changes.
 */
const complaintApi = {
  async listComplaints() {
    const { data } = await apiClient.get('/complaints');
    return data;
  },

  async getComplaint(id) {
    const { data } = await apiClient.get(`/complaints/${id}`);
    return data;
  },

  async getComplaintAudit(id) {
    const { data } = await apiClient.get(`/complaints/${id}/audit`);
    return data;
  },

  async createComplaint(payload) {
    const { data } = await apiClient.post('/complaints', payload);
    return data;
  },

  async updateComplaint(id, payload) {
    const { data } = await apiClient.patch(`/complaints/${id}`, payload);
    return data;
  },

  async deleteComplaint(id) {
    await apiClient.delete(`/complaints/${id}`);
    return id;
  },

  async getDashboardStats() {
    const { data } = await apiClient.get('/complaints/stats');
    return data;
  },

  async checkHealth() {
    const { data } = await apiClient.get('/health');
    return data;
  },
};

export default complaintApi;
