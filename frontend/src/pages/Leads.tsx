import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Grid,
  MenuItem,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  Chip,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  FilterList as FilterIcon,
} from '@mui/icons-material';
import { DataGrid, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';
import { useFormik } from 'formik';
import * as yup from 'yup';
import { RootState } from '../store';
import {
  fetchLeads,
  createLead,
  updateLead,
  deleteLead,
} from '../store/slices/leadsSlice.ts';

const validationSchema = yup.object({
  email: yup
    .string()
    .email('Enter a valid email')
    .required('Email is required'),
  full_name: yup
    .string()
    .required('Full name is required'),
  company: yup
    .string()
    .required('Company is required'),
  phone: yup
    .string()
    .matches(/^\+?[1-9]\d{1,14}$/, 'Enter a valid phone number'),
  source: yup
    .string()
    .required('Source is required'),
  status: yup
    .string()
    .required('Status is required'),
  tags: yup
    .array()
    .of(yup.string()),
});

const initialValues = {
  email: '',
  full_name: '',
  company: '',
  phone: '',
  source: '',
  status: 'new',
  tags: [],
};

const LeadForm: React.FC<{
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
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        {initialFormValues ? 'Edit Lead' : 'Add New Lead'}
      </DialogTitle>
      <form onSubmit={formik.handleSubmit}>
        <DialogContent>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                id="email"
                name="email"
                label="Email"
                value={formik.values.email}
                onChange={formik.handleChange}
                error={formik.touched.email && Boolean(formik.errors.email)}
                helperText={formik.touched.email && formik.errors.email}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                id="full_name"
                name="full_name"
                label="Full Name"
                value={formik.values.full_name}
                onChange={formik.handleChange}
                error={formik.touched.full_name && Boolean(formik.errors.full_name)}
                helperText={formik.touched.full_name && formik.errors.full_name}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                id="company"
                name="company"
                label="Company"
                value={formik.values.company}
                onChange={formik.handleChange}
                error={formik.touched.company && Boolean(formik.errors.company)}
                helperText={formik.touched.company && formik.errors.company}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                id="phone"
                name="phone"
                label="Phone"
                value={formik.values.phone}
                onChange={formik.handleChange}
                error={formik.touched.phone && Boolean(formik.errors.phone)}
                helperText={formik.touched.phone && formik.errors.phone}
              />
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Source</InputLabel>
                <Select
                  id="source"
                  name="source"
                  value={formik.values.source}
                  onChange={formik.handleChange}
                  error={formik.touched.source && Boolean(formik.errors.source)}
                >
                  <MenuItem value="website">Website</MenuItem>
                  <MenuItem value="social_media">Social Media</MenuItem>
                  <MenuItem value="referral">Referral</MenuItem>
                  <MenuItem value="email">Email</MenuItem>
                  <MenuItem value="other">Other</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Status</InputLabel>
                <Select
                  id="status"
                  name="status"
                  value={formik.values.status}
                  onChange={formik.handleChange}
                  error={formik.touched.status && Boolean(formik.errors.status)}
                >
                  <MenuItem value="new">New</MenuItem>
                  <MenuItem value="contacted">Contacted</MenuItem>
                  <MenuItem value="qualified">Qualified</MenuItem>
                  <MenuItem value="proposal">Proposal</MenuItem>
                  <MenuItem value="negotiation">Negotiation</MenuItem>
                  <MenuItem value="closed">Closed</MenuItem>
                  <MenuItem value="lost">Lost</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                id="tags"
                name="tags"
                label="Tags"
                value={formik.values.tags.join(', ')}
                onChange={(e) => {
                  const tags = e.target.value.split(',').map(tag => tag.trim());
                  formik.setFieldValue('tags', tags);
                }}
                helperText="Enter tags separated by commas"
              />
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

const Leads: React.FC = () => {
  const dispatch = useDispatch();
  const { leads, loading, error } = useSelector((state: RootState) => state.leads);
  const [openForm, setOpenForm] = useState(false);
  const [selectedLead, setSelectedLead] = useState<any>(null);
  const [filters, setFilters] = useState({
    search: '',
    status: '',
    source: '',
  });

  useEffect(() => {
    dispatch(fetchLeads());
  }, [dispatch]);

  const handleCreateLead = async (values: any) => {
    await dispatch(createLead(values));
  };

  const handleUpdateLead = async (values: any) => {
    await dispatch(updateLead({ id: selectedLead.id, ...values }));
    setSelectedLead(null);
  };

  const handleDeleteLead = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this lead?')) {
      await dispatch(deleteLead(id));
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 90 },
    { field: 'full_name', headerName: 'Full Name', width: 200 },
    { field: 'email', headerName: 'Email', width: 250 },
    { field: 'company', headerName: 'Company', width: 200 },
    { field: 'phone', headerName: 'Phone', width: 150 },
    {
      field: 'status',
      headerName: 'Status',
      width: 130,
      renderCell: (params: GridValueGetterParams) => (
        <Chip
          label={params.value}
          color={
            params.value === 'qualified' ? 'success' :
            params.value === 'closed' ? 'primary' :
            params.value === 'lost' ? 'error' :
            'default'
          }
          size="small"
        />
      ),
    },
    {
      field: 'source',
      headerName: 'Source',
      width: 130,
    },
    {
      field: 'tags',
      headerName: 'Tags',
      width: 200,
      renderCell: (params: GridValueGetterParams) => (
        <Box>
          {params.value.map((tag: string) => (
            <Chip
              key={tag}
              label={tag}
              size="small"
              sx={{ mr: 0.5 }}
            />
          ))}
        </Box>
      ),
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 120,
      renderCell: (params: GridValueGetterParams) => (
        <Box>
          <IconButton
            size="small"
            onClick={() => {
              setSelectedLead(params.row);
              setOpenForm(true);
            }}
          >
            <EditIcon />
          </IconButton>
          <IconButton
            size="small"
            onClick={() => handleDeleteLead(params.row.id)}
          >
            <DeleteIcon />
          </IconButton>
        </Box>
      ),
    },
  ];

  const filteredLeads = leads.filter((lead) => {
    const matchesSearch = lead.full_name.toLowerCase().includes(filters.search.toLowerCase()) ||
      lead.email.toLowerCase().includes(filters.search.toLowerCase()) ||
      lead.company.toLowerCase().includes(filters.search.toLowerCase());
    const matchesStatus = !filters.status || lead.status === filters.status;
    const matchesSource = !filters.source || lead.source === filters.source;
    return matchesSearch && matchesStatus && matchesSource;
  });

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Leads</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenForm(true)}
        >
          Add Lead
        </Button>
      </Box>

      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Search"
              value={filters.search}
              onChange={(e) => setFilters({ ...filters, search: e.target.value })}
              InputProps={{
                startAdornment: <FilterIcon sx={{ mr: 1, color: 'text.secondary' }} />,
              }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>Status</InputLabel>
              <Select
                value={filters.status}
                onChange={(e) => setFilters({ ...filters, status: e.target.value })}
                label="Status"
              >
                <MenuItem value="">All</MenuItem>
                <MenuItem value="new">New</MenuItem>
                <MenuItem value="contacted">Contacted</MenuItem>
                <MenuItem value="qualified">Qualified</MenuItem>
                <MenuItem value="proposal">Proposal</MenuItem>
                <MenuItem value="negotiation">Negotiation</MenuItem>
                <MenuItem value="closed">Closed</MenuItem>
                <MenuItem value="lost">Lost</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>Source</InputLabel>
              <Select
                value={filters.source}
                onChange={(e) => setFilters({ ...filters, source: e.target.value })}
                label="Source"
              >
                <MenuItem value="">All</MenuItem>
                <MenuItem value="website">Website</MenuItem>
                <MenuItem value="social_media">Social Media</MenuItem>
                <MenuItem value="referral">Referral</MenuItem>
                <MenuItem value="email">Email</MenuItem>
                <MenuItem value="other">Other</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Paper>

      <Paper sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={filteredLeads}
          columns={columns}
          pageSize={10}
          rowsPerPageOptions={[10, 25, 50]}
          checkboxSelection
          disableSelectionOnClick
          loading={loading}
        />
      </Paper>

      <LeadForm
        open={openForm}
        onClose={() => {
          setOpenForm(false);
          setSelectedLead(null);
        }}
        onSubmit={selectedLead ? handleUpdateLead : handleCreateLead}
        initialValues={selectedLead}
      />
    </Box>
  );
};

export default Leads; 