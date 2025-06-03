import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

interface DashboardMetrics {
  total_leads: number;
  active_campaigns: number;
  conversion_rate: number;
  revenue: number;
  social_media_engagement: number;
  email_open_rate: number;
  email_click_rate: number;
}

interface ChartData {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    backgroundColor: string;
    borderColor: string;
  }[];
}

interface DashboardState {
  metrics: DashboardMetrics | null;
  leadTrends: ChartData | null;
  campaignPerformance: ChartData | null;
  socialMediaStats: ChartData | null;
  loading: boolean;
  error: string | null;
  dateRange: {
    start: string;
    end: string;
  };
}

const initialState: DashboardState = {
  metrics: null,
  leadTrends: null,
  campaignPerformance: null,
  socialMediaStats: null,
  loading: false,
  error: null,
  dateRange: {
    start: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    end: new Date().toISOString().split('T')[0],
  },
};

export const fetchDashboardMetrics = createAsyncThunk(
  'dashboard/fetchMetrics',
  async (dateRange: DashboardState['dateRange']) => {
    const response = await axios.get('/api/dashboard/metrics/', { params: dateRange });
    return response.data;
  }
);

export const fetchLeadTrends = createAsyncThunk(
  'dashboard/fetchLeadTrends',
  async (dateRange: DashboardState['dateRange']) => {
    const response = await axios.get('/api/dashboard/lead-trends/', { params: dateRange });
    return response.data;
  }
);

export const fetchCampaignPerformance = createAsyncThunk(
  'dashboard/fetchCampaignPerformance',
  async (dateRange: DashboardState['dateRange']) => {
    const response = await axios.get('/api/dashboard/campaign-performance/', { params: dateRange });
    return response.data;
  }
);

export const fetchSocialMediaStats = createAsyncThunk(
  'dashboard/fetchSocialMediaStats',
  async (dateRange: DashboardState['dateRange']) => {
    const response = await axios.get('/api/dashboard/social-media-stats/', { params: dateRange });
    return response.data;
  }
);

const dashboardSlice = createSlice({
  name: 'dashboard',
  initialState,
  reducers: {
    setDateRange: (state, action) => {
      state.dateRange = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Dashboard Metrics
      .addCase(fetchDashboardMetrics.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchDashboardMetrics.fulfilled, (state, action) => {
        state.loading = false;
        state.metrics = action.payload;
      })
      .addCase(fetchDashboardMetrics.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch dashboard metrics';
      })
      // Fetch Lead Trends
      .addCase(fetchLeadTrends.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchLeadTrends.fulfilled, (state, action) => {
        state.loading = false;
        state.leadTrends = action.payload;
      })
      .addCase(fetchLeadTrends.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch lead trends';
      })
      // Fetch Campaign Performance
      .addCase(fetchCampaignPerformance.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCampaignPerformance.fulfilled, (state, action) => {
        state.loading = false;
        state.campaignPerformance = action.payload;
      })
      .addCase(fetchCampaignPerformance.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch campaign performance';
      })
      // Fetch Social Media Stats
      .addCase(fetchSocialMediaStats.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchSocialMediaStats.fulfilled, (state, action) => {
        state.loading = false;
        state.socialMediaStats = action.payload;
      })
      .addCase(fetchSocialMediaStats.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch social media stats';
      });
  },
});

export const { setDateRange, clearError } = dashboardSlice.actions;
export default dashboardSlice.reducer; 