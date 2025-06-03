import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice.ts';
import leadsReducer from './slices/leadsSlice.ts';
import campaignsReducer from './slices/campaignsSlice.ts';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    leads: leadsReducer,
    campaigns: campaignsReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch; 