import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import complaintApi from '../services/complaintApi.js';

/**
 * The single source of truth for the complaint currently being edited in the
 * Complaint Workspace. Every form field in <ComplaintForm /> reads from and
 * writes to this slice via useSelector / useDispatch — no field value is
 * ever held only in local component state.
 */
export const initialComplaintState = {
  id: null,
  complaintSource: '',
  customerName: '',
  productName: '',
  productStrength: '',
  batchNumber: '',
  manufacturingDate: '',
  expiryDate: '',
  quantityAffected: '',
  complaintType: '',
  complaintDate: '',
  complaintDescription: '',
  initialSeverity: 'Minor',
  priority: 'Medium',
  recommendedActions: '',
  rootCause: '',
  capa: '',
  status: 'Pending Triage',
};

const initialState = {
  activeComplaint: { ...initialComplaintState },
  activeComplaintAudit: [],
  complaints: [],
  dashboardStats: null,
  saveStatus: 'idle', // idle | loading | succeeded | failed
  error: null,
  highlightedFields: [],
  isDirty: false,
};

// Async Thunks
export const fetchComplaints = createAsyncThunk(
  'complaint/fetchComplaints',
  async () => complaintApi.listComplaints()
);

export const fetchComplaintById = createAsyncThunk(
  'complaint/fetchComplaintById',
  async (id) => complaintApi.getComplaint(id)
);

export const fetchComplaintAudit = createAsyncThunk(
  'complaint/fetchComplaintAudit',
  async (id) => complaintApi.getComplaintAudit(id)
);

export const saveComplaint = createAsyncThunk(
  'complaint/saveComplaint',
  async (complaint) => {
    if (complaint.id) {
      return complaintApi.updateComplaint(complaint.id, complaint);
    }
    return complaintApi.createComplaint(complaint);
  }
);

export const deleteComplaint = createAsyncThunk(
  'complaint/deleteComplaint',
  async (id) => complaintApi.deleteComplaint(id)
);

export const fetchDashboardStats = createAsyncThunk(
  'complaint/fetchDashboardStats',
  async () => complaintApi.getDashboardStats()
);

const complaintSlice = createSlice({
  name: 'complaint',
  initialState,
  reducers: {
    setField: (state, action) => {
      const { field, value } = action.payload;
      state.activeComplaint[field] = value;
      state.isDirty = true;
    },
    setComplaint: (state, action) => {
      state.activeComplaint = { ...initialComplaintState, ...action.payload };
      state.isDirty = false;
    },
    resetComplaint: (state) => {
      state.activeComplaint = { ...initialComplaintState };
      state.activeComplaintAudit = [];
      state.saveStatus = 'idle';
      state.error = null;
      state.isDirty = false;
    },
    applyComplaintAIUpdate: (state, action) => {
      const updates = action.payload;
      let changed = false;
      for (const [key, value] of Object.entries(updates)) {
        if (value !== null && value !== undefined) {
          state.activeComplaint[key] = value;
          changed = true;
        }
      }
      if (changed) state.isDirty = true;
    },
    highlightFields: (state, action) => {
      // payload is an array of field names
      state.highlightedFields = action.payload || [];
    },
    clearHighlights: (state) => {
      state.highlightedFields = [];
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchComplaints.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchComplaints.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.complaints = action.payload;
      })
      .addCase(fetchComplaints.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      })
      .addCase(fetchComplaintById.fulfilled, (state, action) => {
        state.activeComplaint = { ...initialComplaintState, ...action.payload };
        state.isDirty = false;
      })
      .addCase(fetchComplaintAudit.fulfilled, (state, action) => {
        state.activeComplaintAudit = action.payload;
      })
      .addCase(saveComplaint.pending, (state) => {
        state.saveStatus = 'loading';
      })
      .addCase(saveComplaint.fulfilled, (state, action) => {
        state.saveStatus = 'succeeded';
        state.activeComplaint = { ...initialComplaintState, ...action.payload };
        state.isDirty = false;
      })
      .addCase(saveComplaint.rejected, (state, action) => {
        state.saveStatus = 'failed';
        state.error = action.error.message;
      })
      .addCase(deleteComplaint.fulfilled, (state, action) => {
        state.complaints = state.complaints.filter(c => c.id !== action.payload);
      })
      .addCase(fetchDashboardStats.fulfilled, (state, action) => {
        state.dashboardStats = action.payload;
      });
  },
});

export const { setField, setComplaint, resetComplaint, applyComplaintAIUpdate, highlightFields, clearHighlights } = complaintSlice.actions;

export default complaintSlice.reducer;
