import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const generationAPI = {
  generate: async (data) => {
    const response = await api.post('/api/generate/', data);
    return response.data;
  },
  
  getGeneration: async (id) => {
    const response = await api.get(`/api/generate/${id}`);
    return response.data;
  },
  
  refineGeneration: async (id, refinementPrompt) => {
    const response = await api.post(`/api/generate/${id}/refine`, {
      refinement_prompt: refinementPrompt,
    });
    return response.data;
  },
  
  getParameters: async () => {
    const response = await api.get('/api/generate/parameters');
    return response.data;
  },
};

export const workflowsAPI = {
  execute: async (data) => {
    // Workflows can take 3-5 minutes for batch generation, use longer timeout
    const response = await api.post('/api/workflows/execute', data, {
      timeout: 300000, // 5 minutes
    });
    return response.data;
  },
  
  getWorkflow: async (id) => {
    const response = await api.get(`/api/workflows/${id}`);
    return response.data;
  },
  
  listWorkflows: async (params) => {
    const response = await api.get('/api/workflows/', { params });
    return response.data;
  },
  
  getWorkflowTypes: async () => {
    const response = await api.get('/api/workflows/types');
    return response.data;
  },
};

export const projectsAPI = {
  create: async (data) => {
    const response = await api.post('/api/projects/', data);
    return response.data;
  },
  
  list: async (params) => {
    const response = await api.get('/api/projects/', { params });
    return response.data;
  },
  
  get: async (id) => {
    const response = await api.get(`/api/projects/${id}`);
    return response.data;
  },
  
  update: async (id, data) => {
    const response = await api.put(`/api/projects/${id}`, data);
    return response.data;
  },
  
  delete: async (id) => {
    const response = await api.delete(`/api/projects/${id}`);
    return response.data;
  },
};

export const healthAPI = {
  check: async () => {
    const response = await api.get('/api/health');
    return response.data;
  },
};

export default api;
