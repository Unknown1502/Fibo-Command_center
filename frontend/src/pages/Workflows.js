import React, { useState } from 'react';
import { useMutation } from 'react-query';
import { workflowsAPI } from '../services/api';

const Workflows = () => {
  const [selectedWorkflow, setSelectedWorkflow] = useState('ecommerce');
  const [formData, setFormData] = useState({});
  const [result, setResult] = useState(null);
  
  const workflowTypes = {
    ecommerce: {
      name: 'E-commerce Product Pipeline',
      description: 'Generate complete product photography sets with multiple angles',
      fields: [
        { name: 'product_name', label: 'Product Name', type: 'text', required: true },
        { name: 'product_type', label: 'Product Type', type: 'text', required: true },
        { name: 'brand_colors', label: 'Brand Colors (comma-separated)', type: 'text' },
        { name: 'style_preference', label: 'Style Preference', type: 'select', options: ['commercial', 'lifestyle', 'editorial'] },
      ],
    },
    social_media: {
      name: 'Social Media Campaign',
      description: 'Create platform-optimized content for social channels',
      fields: [
        { name: 'campaign_theme', label: 'Campaign Theme', type: 'text', required: true },
        { name: 'brand_name', label: 'Brand Name', type: 'text', required: true },
        { name: 'tone', label: 'Tone', type: 'select', options: ['professional', 'casual', 'energetic', 'elegant'] },
      ],
    },
    game_asset: {
      name: 'Game Asset Generation',
      description: 'Produce game-ready visual assets with variations',
      fields: [
        { name: 'asset_type', label: 'Asset Type', type: 'text', required: true },
        { name: 'description', label: 'Description', type: 'textarea', required: true },
        { name: 'game_style', label: 'Game Style', type: 'select', options: ['realistic', 'stylized', 'pixel-art', 'low-poly'] },
        { name: 'variations', label: 'Number of Variations', type: 'number', min: 1, max: 4 },
      ],
    },
  };
  
  const executeMutation = useMutation(workflowsAPI.execute, {
    onSuccess: (data) => {
      setResult(data);
    },
    onError: (error) => {
      alert('Workflow failed: ' + (error.response?.data?.detail || error.message));
    },
  });
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    executeMutation.mutate({
      workflow_type: selectedWorkflow,
      input_data: formData,
      user_id: 1,
    });
  };
  
  const handleInputChange = (fieldName, value) => {
    setFormData({
      ...formData,
      [fieldName]: value,
    });
  };
  
  const currentWorkflow = workflowTypes[selectedWorkflow];
  
  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="bg-white shadow sm:rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Automated Workflows</h2>
          
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Workflow Type
            </label>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              {Object.entries(workflowTypes).map(([key, workflow]) => (
                <div
                  key={key}
                  onClick={() => {
                    setSelectedWorkflow(key);
                    setFormData({});
                    setResult(null);
                  }}
                  className={`cursor-pointer rounded-lg border-2 p-4 ${
                    selectedWorkflow === key
                      ? 'border-indigo-600 bg-indigo-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <h3 className="font-medium text-gray-900">{workflow.name}</h3>
                  <p className="mt-1 text-sm text-gray-500">{workflow.description}</p>
                </div>
              ))}
            </div>
          </div>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-4">
              {currentWorkflow.fields.map((field) => (
                <div key={field.name}>
                  <label htmlFor={field.name} className="block text-sm font-medium text-gray-700">
                    {field.label} {field.required && <span className="text-red-500">*</span>}
                  </label>
                  <div className="mt-1">
                    {field.type === 'textarea' ? (
                      <textarea
                        id={field.name}
                        name={field.name}
                        rows={3}
                        required={field.required}
                        className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                        value={formData[field.name] || ''}
                        onChange={(e) => handleInputChange(field.name, e.target.value)}
                      />
                    ) : field.type === 'select' ? (
                      <select
                        id={field.name}
                        name={field.name}
                        required={field.required}
                        className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                        value={formData[field.name] || ''}
                        onChange={(e) => handleInputChange(field.name, e.target.value)}
                      >
                        <option value="">Select...</option>
                        {field.options.map((option) => (
                          <option key={option} value={option}>
                            {option.charAt(0).toUpperCase() + option.slice(1)}
                          </option>
                        ))}
                      </select>
                    ) : field.type === 'number' ? (
                      <input
                        type="number"
                        id={field.name}
                        name={field.name}
                        required={field.required}
                        min={field.min}
                        max={field.max}
                        className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                        value={formData[field.name] || ''}
                        onChange={(e) => handleInputChange(field.name, e.target.value)}
                      />
                    ) : (
                      <input
                        type="text"
                        id={field.name}
                        name={field.name}
                        required={field.required}
                        className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                        value={formData[field.name] || ''}
                        onChange={(e) => handleInputChange(field.name, e.target.value)}
                      />
                    )}
                  </div>
                </div>
              ))}
            </div>
            
            <div>
              <button
                type="submit"
                disabled={executeMutation.isLoading}
                className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {executeMutation.isLoading ? 'Executing Workflow...' : 'Execute Workflow'}
              </button>
            </div>
          </form>
          
          {result && (
            <div className="mt-8 border-t border-gray-200 pt-8">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Workflow Results</h3>
              <div className="bg-gray-50 rounded-lg p-4 mb-4">
                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="font-medium">Total Generated:</span> {result.total_generations}
                  </div>
                  <div>
                    <span className="font-medium">Completed:</span> {result.completed_generations}
                  </div>
                  <div>
                    <span className="font-medium">Failed:</span> {result.failed_generations}
                  </div>
                </div>
              </div>
              
              {result.results && result.results.length > 0 && (
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  {result.results.map((item, index) => (
                    <div key={index} className="bg-white border border-gray-200 rounded-lg overflow-hidden">
                      <div className="p-4">
                        <h4 className="font-medium text-gray-900 mb-2">
                          {item.angle || item.platform || item.variation || `Result ${index + 1}`}
                        </h4>
                        {item.status === 'success' && item.result?.image_url && (
                          <img
                            src={item.result.image_url}
                            alt={item.angle || `Result ${index + 1}`}
                            className="w-full h-48 object-cover rounded"
                          />
                        )}
                        {item.status === 'failed' && (
                          <div className="text-sm text-red-600">
                            Failed: {item.error}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Workflows;
