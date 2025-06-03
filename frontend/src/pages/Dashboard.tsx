import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  People as PeopleIcon,
  Campaign as CampaignIcon,
  TrendingUp as TrendingUpIcon,
  AttachMoney as MoneyIcon,
  Share as ShareIcon,
  Email as EmailIcon,
  Mouse as ClickIcon,
} from '@mui/icons-material';
import { Line, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { RootState } from '../store';
import {
  fetchDashboardMetrics,
  fetchLeadTrends,
  fetchCampaignPerformance,
  fetchSocialMediaStats,
} from '../store/slices/dashboardSlice.ts';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const MetricCard: React.FC<{
  title: string;
  value: string | number;
  icon: React.ReactNode;
  color: string;
}> = ({ title, value, icon, color }) => (
  <Card>
    <CardContent>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Box
          sx={{
            backgroundColor: `${color}20`,
            borderRadius: '50%',
            p: 1,
            mr: 2,
          }}
        >
          {icon}
        </Box>
        <Typography variant="h6" component="div">
          {title}
        </Typography>
      </Box>
      <Typography variant="h4" component="div">
        {value}
      </Typography>
    </CardContent>
  </Card>
);

const Dashboard: React.FC = () => {
  const dispatch = useDispatch();
  const { metrics, leadTrends, campaignPerformance, socialMediaStats, loading, error } = useSelector(
    (state: RootState) => state.dashboard
  );

  useEffect(() => {
    const fetchData = async () => {
      await Promise.all([
        dispatch(fetchDashboardMetrics({ start: '', end: '' })),
        dispatch(fetchLeadTrends({ start: '', end: '' })),
        dispatch(fetchCampaignPerformance({ start: '', end: '' })),
        dispatch(fetchSocialMediaStats({ start: '', end: '' })),
      ]);
    };
    fetchData();
  }, [dispatch]);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ mt: 2 }}>
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>

      {/* Metrics Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Total Leads"
            value={metrics?.total_leads || 0}
            icon={<PeopleIcon sx={{ color: '#2196f3' }} />}
            color="#2196f3"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Active Campaigns"
            value={metrics?.active_campaigns || 0}
            icon={<CampaignIcon sx={{ color: '#4caf50' }} />}
            color="#4caf50"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Conversion Rate"
            value={`${metrics?.conversion_rate || 0}%`}
            icon={<TrendingUpIcon sx={{ color: '#ff9800' }} />}
            color="#ff9800"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Revenue"
            value={`$${metrics?.revenue?.toLocaleString() || 0}`}
            icon={<MoneyIcon sx={{ color: '#9c27b0' }} />}
            color="#9c27b0"
          />
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3}>
        {/* Lead Trends */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Lead Trends
            </Typography>
            {leadTrends && (
              <Line
                data={leadTrends}
                options={{
                  responsive: true,
                  plugins: {
                    legend: {
                      position: 'top' as const,
                    },
                  },
                }}
              />
            )}
          </Paper>
        </Grid>

        {/* Campaign Performance */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Campaign Performance
            </Typography>
            {campaignPerformance && (
              <Bar
                data={campaignPerformance}
                options={{
                  responsive: true,
                  plugins: {
                    legend: {
                      position: 'top' as const,
                    },
                  },
                }}
              />
            )}
          </Paper>
        </Grid>

        {/* Social Media Stats */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Social Media Engagement
            </Typography>
            {socialMediaStats && (
              <Line
                data={socialMediaStats}
                options={{
                  responsive: true,
                  plugins: {
                    legend: {
                      position: 'top' as const,
                    },
                  },
                }}
              />
            )}
          </Paper>
        </Grid>
      </Grid>

      {/* Additional Metrics */}
      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Social Engagement"
            value={metrics?.social_media_engagement || 0}
            icon={<ShareIcon sx={{ color: '#e91e63' }} />}
            color="#e91e63"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Email Open Rate"
            value={`${metrics?.email_open_rate || 0}%`}
            icon={<EmailIcon sx={{ color: '#00bcd4' }} />}
            color="#00bcd4"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Click Rate"
            value={`${metrics?.email_click_rate || 0}%`}
            icon={<ClickIcon sx={{ color: '#ff5722' }} />}
            color="#ff5722"
          />
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 