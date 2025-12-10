import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import ErrorBoundary from './components/ErrorBoundary';
import Navigation from './components/Navigation';
import Dashboard from './pages/Dashboard';
import Generator from './pages/Generator';
import Workflows from './pages/Workflows';
import Projects from './pages/Projects';
import AITranslator from './pages/AITranslatorModern';
import VisualEditor from './pages/VisualEditor';
import AnalyticsDashboard from './pages/AnalyticsDashboard';
import BrandGuidelines from './pages/BrandGuidelines';
import ControlNetStudio from './pages/ControlNetStudio';
import './App.css';
import './styles/modern.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000,
    },
  },
});

function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <Router>
          <div className="min-h-screen">
            <Navigation />
            <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/generator" element={<Generator />} />
                <Route path="/generate" element={<Navigate to="/generator" replace />} />
                <Route path="/workflows" element={<Workflows />} />
                <Route path="/projects" element={<Projects />} />
                <Route path="/ai-translator" element={<AITranslator />} />
                <Route path="/visual-editor" element={<VisualEditor />} />
                <Route path="/analytics" element={<AnalyticsDashboard />} />
                <Route path="/brand-guidelines" element={<BrandGuidelines />} />
                <Route path="/controlnet" element={<ControlNetStudio />} />
              </Routes>
            </div>
          </div>
        </Router>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

export default App;
