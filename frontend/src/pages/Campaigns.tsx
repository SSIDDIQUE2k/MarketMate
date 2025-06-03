import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Typography,
  Paper,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  LinearProgress,
  Alert,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  PlayArrow as StartIcon,
  Stop as StopIcon,
  Schedule as ScheduleIcon,
} from '@mui/icons-material';
import { useFormik } from 'formik';
import * as yup from 'yup';
import { RootState } from '../store';
import {
  fetchCampaigns,
  createCampaign,
  updateCampaign,
  deleteCampaign,
  startCampaign,
  stopCampaign,
} from '../store/slices/campaignsSlice.ts';

const validationSchema = yup.object({
  name: yup
    .string()
    .required('Campaign name is required'),
  description: yup
    .string()
    .required('Description is required'),
  type: yup
    .string()
    .required('Campaign type is required'),
  target_audience: yup
    .string()
    .required('Target audience is required'),
  start_date: yup
    .date()
    .required('Start date is required'),
  end_date: yup
    .date()
    .min(yup.ref('start_date'), 'End date must be after start date'),
  budget: yup
    .number()
    .min(0, 'Budget must be positive')
    .required('Budget is required'),
  status: yup
    .string()
    .required('Status is required'),
});

const initialValues = {
  name: '',
  description: '',
  type: '',
  target_audience: '',
  start_date: '',
  end_date: '',
  budget: 0,
  status: 'draft',
};

const CampaignForm: React.FC<{
  open: boolean;
  onClose: () => void;
  onSubmit: (values: any) => void;
  initialValues?: any;
}> = ({ open, onClose, onSubmit, initialValues: initialFormValues }) => {
  const formik = useFormik({
    initialValues: initialFormValues || initialValues,
    validationSchema: validationSchema,
    onSubmit: (values) => {
      onSubmit(values);
      onClose();
    },
  });

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        {initialFormValues ? 'Edit Campaign' : 'Create New Campaign'}
      </DialogTitle>
      <form onSubmit={formik.handleSubmit}>
        <DialogContent>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                id="name"
                name="name"
                label="Campaign Name"
                value={formik.values.name}
                onChange={formik.handleChange}
                error={formik.touched.name && Boolean(formik.errors.name)}
                helperText={formik.touched.name && formik.errors.name}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                id="description"
                name="description"
                label="Description"
                multiline
                rows={4}
                value={formik.values.description}
                onChange={formik.handleChange}
                error={formik.touched.description && Boolean(formik.errors.description)}
                helperText={formik.touched.description && formik.errors.description}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Campaign Type</InputLabel>
                <Select
                  id="type"
                  name="type"
                  value={formik.values.type}
                  onChange={formik.handleChange}
                  error={formik.touched.type && Boolean(formik.errors.type)}
                >
                  <MenuItem value="email">Email Campaign</MenuItem>
                  <MenuItem value="social_media">Social Media Campaign</MenuItem>
                  <MenuItem value="content">Content Marketing</MenuItem>
                  <MenuItem value="paid_ads">Paid Advertising</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                id="target_audience"
                name="target_audience"
                label="Target Audience"
                value={formik.values.target_audience}
                onChange={formik.handleChange}
                error={formik.touched.target_audience && Boolean(formik.errors.target_audience)}
                helperText={formik.touched.target_audience && formik.errors.target_audience}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                id="start_date"
                name="start_date"
                label="Start Date"
                type="datetime-local"
                value={formik.values.start_date}
                onChange={formik.handleChange}
                error={formik.touched.start_date && Boolean(formik.errors.start_date)}
                helperText={formik.touched.start_date && formik.errors.start_date}
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                id="end_date"
                name="end_date"
                label="End Date"
                type="datetime-local"
                value={formik.values.end_date}
                onChange={formik.handleChange}
                error={formik.touched.end_date && Boolean(formik.errors.end_date)}
                helperText={formik.touched.end_date && formik.errors.end_date}
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                id="budget"
                name="budget"
                label="Budget"
                type="number"
                value={formik.values.budget}
                onChange={formik.handleChange}
                error={formik.touched.budget && Boolean(formik.errors.budget)}
                helperText={formik.touched.budget && formik.errors.budget}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Status</InputLabel>
                <Select
                  id="status"
                  name="status"
                  value={formik.values.status}
                  onChange={formik.handleChange}
                  error={formik.touched.status && Boolean(formik.errors.status)}
                >
                  <MenuItem value="draft">Draft</MenuItem>
                  <MenuItem value="scheduled">Scheduled</MenuItem>
                  <MenuItem value="active">Active</MenuItem>
                  <MenuItem value="paused">Paused</MenuItem>
                  <MenuItem value="completed">Completed</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
          <Button type="submit" variant="contained" color="primary">
            {initialFormValues ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};

const CampaignCard: React.FC<{
  campaign: any;
  onEdit: (campaign: any) => void;
  onDelete: (id: number) => void;
  onStart: (id: number) => void;
  onStop: (id: number) => void;
}> = ({ campaign, onEdit, onDelete, onStart, onStop }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'paused':
        return 'warning';
      case 'completed':
        return 'info';
      case 'scheduled':
        return 'primary';
      default:
        return 'default';
    }
  };

  const getProgress = () => {
    if (campaign.status === 'completed') return 100;
    if (!campaign.start_date || !campaign.end_date) return 0;
    
    const start = new Date(campaign.start_date).getTime();
    const end = new Date(campaign.end_date).getTime();
    const now = new Date().getTime();
    
    if (now < start) return 0;
    if (now > end) return 100;
    
    return ((now - start) / (end - start)) * 100;
  };

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
          <Typography variant="h6" component="div">
            {campaign.name}
          </Typography>
          <Chip
            label={campaign.status}
            color={getStatusColor(campaign.status)}
            size="small"
          />
        </Box>
        <Typography color="text.secondary" gutterBottom>
          {campaign.description}
        </Typography>
        <Grid container spacing={2} sx={{ mt: 1 }}>
          <Grid item xs={6}>
            <Typography variant="body2" color="text.secondary">
              Type: {campaign.type}
            </Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="body2" color="text.secondary">
              Budget: ${campaign.budget}
            </Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="body2" color="text.secondary">
              Start: {new Date(campaign.start_date).toLocaleDateString()}
            </Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="body2" color="text.secondary">
              End: {new Date(campaign.end_date).toLocaleDateString()}
            </Typography>
          </Grid>
        </Grid>
        <Box sx={{ mt: 2 }}>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Progress
          </Typography>
          <LinearProgress
            variant="determinate"
            value={getProgress()}
            color={getStatusColor(campaign.status)}
          />
        </Box>
      </CardContent>
      <CardActions>
        {campaign.status === 'draft' && (
          <Button
            size="small"
            startIcon={<StartIcon />}
            onClick={() => onStart(campaign.id)}
          >
            Start
          </Button>
        )}
        {campaign.status === 'active' && (
          <Button
            size="small"
            startIcon={<StopIcon />}
            onClick={() => onStop(campaign.id)}
          >
            Stop
          </Button>
        )}
        <Button
          size="small"
          startIcon={<EditIcon />}
          onClick={() => onEdit(campaign)}
        >
          Edit
        </Button>
        <Button
          size="small"
          startIcon={<DeleteIcon />}
          onClick={() => onDelete(campaign.id)}
          color="error"
        >
          Delete
        </Button>
      </CardActions>
    </Card>
  );
};

const Campaigns: React.FC = () => {
  const dispatch = useDispatch();
  const { campaigns, loading, error } = useSelector((state: RootState) => state.campaigns);
  const [openForm, setOpenForm] = useState(false);
  const [selectedCampaign, setSelectedCampaign] = useState<any>(null);

  useEffect(() => {
    dispatch(fetchCampaigns());
  }, [dispatch]);

  const handleCreateCampaign = async (values: any) => {
    await dispatch(createCampaign(values));
  };

  const handleUpdateCampaign = async (values: any) => {
    await dispatch(updateCampaign({ id: selectedCampaign.id, ...values }));
    setSelectedCampaign(null);
  };

  const handleDeleteCampaign = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this campaign?')) {
      await dispatch(deleteCampaign(id));
    }
  };

  const handleStartCampaign = async (id: number) => {
    await dispatch(startCampaign(id));
  };

  const handleStopCampaign = async (id: number) => {
    await dispatch(stopCampaign(id));
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Campaigns</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenForm(true)}
        >
          Create Campaign
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {campaigns.map((campaign) => (
          <Grid item xs={12} md={6} lg={4} key={campaign.id}>
            <CampaignCard
              campaign={campaign}
              onEdit={(campaign) => {
                setSelectedCampaign(campaign);
                setOpenForm(true);
              }}
              onDelete={handleDeleteCampaign}
              onStart={handleStartCampaign}
              onStop={handleStopCampaign}
            />
          </Grid>
        ))}
      </Grid>

      <CampaignForm
        open={openForm}
        onClose={() => {
          setOpenForm(false);
          setSelectedCampaign(null);
        }}
        onSubmit={selectedCampaign ? handleUpdateCampaign : handleCreateCampaign}
        initialValues={selectedCampaign}
      />
    </Box>
  );
};

export default Campaigns; 