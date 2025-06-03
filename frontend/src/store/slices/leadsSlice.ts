import { createSlice, PayloadAction, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

interface Lead {
  id: string;
  name: string;
  email: string;
  phone?: string;
  status: 'new' | 'contacted' | 'qualified' | 'lost';
  source: string;
  createdAt: string;
}

interface LeadsState {
  leads: Lead[];
  loading: boolean;
  error: string | null;
  totalCount?: number;
  selectedLead?: Lead | null;
}

const initialState: LeadsState = {
  leads: [],
  loading: false,
  error: null,
  totalCount: 0,
  selectedLead: null,
};

export const fetchLeads = createAsyncThunk(
  'leads/fetchLeads',
  async (params?: { page?: number; limit?: number; filters?: any }) => {
    const { page = 1, limit = 50, filters = {} } = params || {};
    const response = await axios.get('/api/leads/', {
      params: {
        page,
        limit,
        ...filters,
      },
    });
    return response.data;
  }
);

export const fetchLeadById = createAsyncThunk('leads/fetchLeadById', async (id: number) => {
  const response = await axios.get(`/api/leads/${id}/`);
  return response.data;
});

export const createLead = createAsyncThunk('leads/createLead', async (lead: Partial<Lead>) => {
  const response = await axios.post('/api/leads/', lead);
  return response.data;
});

export const updateLead = createAsyncThunk(
  'leads/updateLead',
  async ({ id, data }: { id: number; data: Partial<Lead> }) => {
    const response = await axios.patch(`/api/leads/${id}/`, data);
    return response.data;
  }
);

export const deleteLead = createAsyncThunk('leads/deleteLead', async (id: number) => {
  await axios.delete(`/api/leads/${id}/`);
  return id;
});

const leadsSlice = createSlice({
  name: 'leads',
  initialState,
  reducers: {
    setLeads: (state, action: PayloadAction<Lead[]>) => {
      state.leads = action.payload;
    },
    addLead: (state, action: PayloadAction<Lead>) => {
      state.leads.push(action.payload);
    },
    updateLeadAction: (state, action: PayloadAction<Lead>) => {
      const index = state.leads.findIndex(lead => lead.id === action.payload.id);
      if (index !== -1) {
        state.leads[index] = action.payload;
      }
    },
    deleteLeadAction: (state, action: PayloadAction<string>) => {
      state.leads = state.leads.filter(lead => lead.id !== action.payload);
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Leads
      .addCase(fetchLeads.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchLeads.fulfilled, (state, action) => {
        state.loading = false;
        state.leads = action.payload.items;
        state.totalCount = action.payload.total;
      })
      .addCase(fetchLeads.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch leads';
      })
      // Fetch Lead by ID
      .addCase(fetchLeadById.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchLeadById.fulfilled, (state, action) => {
        state.loading = false;
        state.selectedLead = action.payload;
      })
      .addCase(fetchLeadById.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch lead';
      })
      // Create Lead
      .addCase(createLead.fulfilled, (state, action) => {
        state.leads.unshift(action.payload);
        state.totalCount += 1;
      })
      // Update Lead
      .addCase(updateLead.fulfilled, (state, action) => {
        const index = state.leads.findIndex((lead) => lead.id === action.payload.id);
        if (index !== -1) {
          state.leads[index] = action.payload;
        }
        if (state.selectedLead?.id === action.payload.id) {
          state.selectedLead = action.payload;
        }
      })
      // Delete Lead
      .addCase(deleteLead.fulfilled, (state, action) => {
        state.leads = state.leads.filter((lead) => lead.id !== action.payload);
        state.totalCount -= 1;
        if (state.selectedLead?.id === action.payload) {
          state.selectedLead = null;
        }
      });
  },
});

export const {
  setLeads,
  addLead,
  updateLeadAction,
  deleteLeadAction,
  setLoading,
  setError,
} = leadsSlice.actions;

export default leadsSlice.reducer; 