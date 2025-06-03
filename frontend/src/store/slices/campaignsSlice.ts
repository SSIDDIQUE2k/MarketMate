import { createSlice, PayloadAction, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

interface Campaign {
  id: string;
  name: string;
  description: string;
  status: 'draft' | 'active' | 'paused' | 'completed';
  type: 'email' | 'social' | 'sms' | 'chatbot';
  startDate: string;
  endDate?: string;
  metrics: {
    reach: number;
    engagement: number;
    conversions: number;
  };
}

interface CampaignsState {
  campaigns: Campaign[];
  loading: boolean;
  error: string | null;
}

const initialState: CampaignsState = {
  campaigns: [],
  loading: false,
  error: null,
};

// Async thunks
export const fetchCampaigns = createAsyncThunk(
  'campaigns/fetchCampaigns',
  async () => {
    const response = await axios.get('/api/campaigns/');
    return response.data;
  }
);

export const createCampaign = createAsyncThunk(
  'campaigns/createCampaign',
  async (campaignData: Partial<Campaign>) => {
    const response = await axios.post('/api/campaigns/', campaignData);
    return response.data;
  }
);

export const startCampaign = createAsyncThunk(
  'campaigns/startCampaign',
  async (id: number) => {
    const response = await axios.post(`/api/campaigns/${id}/start/`);
    return response.data;
  }
);

export const stopCampaign = createAsyncThunk(
  'campaigns/stopCampaign',
  async (id: number) => {
    const response = await axios.post(`/api/campaigns/${id}/stop/`);
    return response.data;
  }
);

const campaignsSlice = createSlice({
  name: 'campaigns',
  initialState,
  reducers: {
    setCampaigns: (state, action: PayloadAction<Campaign[]>) => {
      state.campaigns = action.payload;
    },
    addCampaign: (state, action: PayloadAction<Campaign>) => {
      state.campaigns.push(action.payload);
    },
    updateCampaign: (state, action: PayloadAction<Campaign>) => {
      const index = state.campaigns.findIndex(campaign => campaign.id === action.payload.id);
      if (index !== -1) {
        state.campaigns[index] = action.payload;
      }
    },
    deleteCampaign: (state, action: PayloadAction<string>) => {
      state.campaigns = state.campaigns.filter(campaign => campaign.id !== action.payload);
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
      // Fetch Campaigns
      .addCase(fetchCampaigns.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCampaigns.fulfilled, (state, action) => {
        state.loading = false;
        state.campaigns = action.payload;
      })
      .addCase(fetchCampaigns.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch campaigns';
      })
      // Create Campaign
      .addCase(createCampaign.fulfilled, (state, action) => {
        state.campaigns.push(action.payload);
      })
      // Start Campaign
      .addCase(startCampaign.fulfilled, (state, action) => {
        const index = state.campaigns.findIndex(c => c.id === action.payload.id);
        if (index !== -1) {
          state.campaigns[index] = action.payload;
        }
      })
      // Stop Campaign
      .addCase(stopCampaign.fulfilled, (state, action) => {
        const index = state.campaigns.findIndex(c => c.id === action.payload.id);
        if (index !== -1) {
          state.campaigns[index] = action.payload;
        }
      });
  },
});

export const {
  setCampaigns,
  addCampaign,
  updateCampaign,
  deleteCampaign,
  setLoading,
  setError,
} = campaignsSlice.actions;

export default campaignsSlice.reducer; 