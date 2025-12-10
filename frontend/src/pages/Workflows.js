import React, { useState } from 'react';
import { useMutation } from 'react-query';
import { workflowsAPI } from '../services/api';
import { Play, Package, Share2, Gamepad2, CheckCircle, XCircle } from 'lucide-react';

const Workflows = () => {
  const [selectedWorkflow, setSelectedWorkflow] = useState('ecommerce');
  const [formData, setFormData] = useState({});
  const [result, setResult] = useState(null);
  
  const workflowTypes = {
    ecommerce: {
      name: 'E-commerce Product Pipeline',
      description: 'Generate complete product photography sets with multiple angles',
      icon: <Package className="w-6 h-6" />,
      color: 'from-blue-500 to-cyan-500',
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
      icon: <Share2 className="w-6 h-6" />,
      color: 'from-pink-500 to-rose-500',
      fields: [
        { name: 'campaign_theme', label: 'Campaign Theme', type: 'text', required: true },
        { name: 'brand_name', label: 'Brand Name', type: 'text', required: true },
        { name: 'tone', label: 'Tone', type: 'select', options: ['professional', 'casual', 'energetic', 'elegant'] },
      ],
    },
    game_asset: {
      name: 'Game Asset Generation',
      description: 'Produce game-ready visual assets with variations',
      icon: <Gamepad2 className="w-6 h-6" />,
      color: 'from-purple-500 to-indigo-500',
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
    <div className="max-w-7xl mx-auto p-6">
      {/* Header */}
      <div className="mb-8 text-center animate-fade-in">
        <div className="inline-flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 rounded-full mb-4">
          <Play className="w-4 h-4 text-indigo-400" />
          <span className="text-sm font-medium text-white">Automated Production</span>
        </div>
        <h1 className="text-5xl font-bold text-white mb-3">
          <span className="text-gradient">Automated Workflows</span>
        </h1>
        <p className="text-xl text-gray-300">Streamline your production with intelligent automation</p>
      </div>
      
      {/* Workflow Type Selection */}
      <div className="mb-8">
        <label className="block text-sm font-medium text-gray-300 mb-4">
          Select Workflow Type
        </label>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {Object.entries(workflowTypes).map(([key, workflow]) => (
            <div
              key={key}
              onClick={() => {
                setSelectedWorkflow(key);
                setFormData({});
                setResult(null);
              }}
              className={`glass-card p-6 cursor-pointer transition-all duration-300 hover-glow group ${
                selectedWorkflow === key ? 'ring-2 ring-indigo-500' : ''
              }`}
            >
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${workflow.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
                {workflow.icon}
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">{workflow.name}</h3>
              <p className="text-sm text-gray-400">{workflow.description}</p>
              {selectedWorkflow === key && (
                <div className="mt-3 text-xs text-indigo-400 font-medium">
                  ✓ Selected
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
      
      {/* Workflow Form */}
      <div className="glass-card p-8 animate-slide-in">
        <h2 className="text-2xl font-bold text-white mb-6">{currentWorkflow.name}</h2>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-5">
            {currentWorkflow.fields.map((field) => (
              <div key={field.name}>
                <label htmlFor={field.name} className="block text-sm font-medium text-gray-300 mb-2">
                  {field.label} {field.required && <span className="text-red-400">*</span>}
                </label>
                <div>
                  {field.type === 'textarea' ? (
                    <textarea
                      id={field.name}
                      name={field.name}
                      rows={3}
                      required={field.required}
                      className="textarea-modern w-full"
                      value={formData[field.name] || ''}
                      onChange={(e) => handleInputChange(field.name, e.target.value)}
                      placeholder={`Enter ${field.label.toLowerCase()}...`}
                    />
                  ) : field.type === 'select' ? (
                    <select
                      id={field.name}
                      name={field.name}
                      required={field.required}
                      className="input-modern w-full"
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
                      className="input-modern w-full"
                      value={formData[field.name] || ''}
                      onChange={(e) => handleInputChange(field.name, e.target.value)}
                      placeholder={`Enter ${field.label.toLowerCase()}...`}
                    />
                  ) : (
                    <input
                      type="text"
                      id={field.name}
                      name={field.name}
                      required={field.required}
                      className="input-modern w-full"
                      value={formData[field.name] || ''}
                      onChange={(e) => handleInputChange(field.name, e.target.value)}
                      placeholder={`Enter ${field.label.toLowerCase()}...`}
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
              className="btn-modern w-full bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 flex items-center justify-center space-x-2"
            >
              <Play className="w-5 h-5" />
              <span>{executeMutation.isLoading ? 'Executing Workflow...' : 'Execute Workflow'}</span>
            </button>
          </div>
        </form>
      </div>
      
      {/* Workflow Results */}
      {result && (
        <div className="mt-8 glass-card p-8 animate-fade-in">
          <h3 className="text-2xl font-bold text-white mb-6">Workflow Results</h3>
          
          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="bg-white/5 rounded-xl p-4 border border-white/10">
              <div className="text-3xl font-bold text-white mb-1">{result.total_generations}</div>
              <div className="text-sm text-gray-400">Total Generated</div>
            </div>
            <div className="bg-green-500/10 rounded-xl p-4 border border-green-500/20">
              <div className="flex items-center space-x-2">
                <CheckCircle className="w-5 h-5 text-green-400" />
                <div className="text-3xl font-bold text-green-400">{result.completed_generations}</div>
              </div>
              <div className="text-sm text-gray-400">Completed</div>
            </div>
            <div className="bg-red-500/10 rounded-xl p-4 border border-red-500/20">
              <div className="flex items-center space-x-2">
                <XCircle className="w-5 h-5 text-red-400" />
                <div className="text-3xl font-bold text-red-400">{result.failed_generations}</div>
              </div>
              <div className="text-sm text-gray-400">Failed</div>
            </div>
          </div>
          
          {/* Results Grid */}
          {result.results && result.results.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {result.results.map((item, index) => (
                <div key={index} className="bg-white/5 rounded-xl overflow-hidden border border-white/10 hover:border-indigo-500/50 transition-all duration-300">
                  <div className="p-4">
                    <h4 className="font-semibold text-white mb-3">
                      {item.angle || item.platform || item.variation || `Result ${index + 1}`}
                    </h4>
                    {item.status === 'success' && item.result?.image_url && (
                      <div className="relative group">
                        <img
                          src={item.result.image_url}
                          alt={item.angle || `Result ${index + 1}`}
                          className="w-full h-48 object-cover rounded-lg"
                        />
                        <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-lg flex items-center justify-center">
                          <span className="text-white text-sm">View Full Size</span>
                        </div>
                      </div>
                    )}
                    {item.status === 'failed' && (
                      <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-3">
                        <div className="flex items-start space-x-2">
                          <XCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                          <div className="text-sm text-red-400">
                            {item.error}
                          </div>
                        </div>
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
  );
};

export default Workflows;
