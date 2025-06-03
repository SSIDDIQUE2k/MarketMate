import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box, Container } from '@mui/material';
import Dashboard from './pages/Dashboard.tsx';
import Leads from './pages/Leads.tsx';
import Campaigns from './pages/Campaigns.tsx';
import Layout from './components/Layout.tsx';

const App: React.FC = () => {
  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Layout>
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/leads" element={<Leads />} />
            <Route path="/campaigns" element={<Campaigns />} />
          </Routes>
        </Container>
      </Layout>
    </Box>
  );
};

export default App; 