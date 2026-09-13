import { configureStore } from '@reduxjs/toolkit';
import complaintReducer from '../slices/complaintSlice.js';
import copilotReducer from '../slices/copilotSlice.js';

export const store = configureStore({
  reducer: {
    complaint: complaintReducer,
    copilot: copilotReducer,
  },
  // Keep default middleware (includes redux-thunk, used by our async thunks).
  devTools: import.meta.env.MODE !== 'production',
});

export default store;
