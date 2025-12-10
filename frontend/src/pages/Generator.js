import React, { useState } from 'react';
import { useMutation } from 'react-query';
import { generationAPI } from '../services/api';

const Generator = () => {
  const [mode, setMode] = useState('ai');
  const [prompt, setPrompt] = useState('');
  const [parameters, setParameters] = useState({
    camera_angle: '',
    fov: '',
    lighting: '',
    color_palette: '',
    composition: '',
    style: '',
  });
  const [result, setResult] = useState(null);
  
  const generateMutation = useMutation(generationAPI.generate, {
    onSuccess: (data) => {
      setResult(data);
    },
    onError: (error) => {
      alert('Generation failed: ' + (error.response?.data?.detail || error.message));
    },
  });
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    const requestData = {
      prompt,
      mode,
      user_id: 1,
    };
    
    if (mode === 'manual') {
      Object.keys(parameters).forEach(key => {
        if (parameters[key]) {
          requestData[key] = parameters[key];
        }
      });
    }
    
    generateMutation.mutate(requestData);
  };
  
  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="bg-white shadow sm:rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Image Generation</h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="text-base font-medium text-gray-900">Generation Mode</label>
              <div className="mt-4 space-y-4">
                <div className="flex items-center">
                  <input
                    id="mode-ai"
                    name="mode"
                    type="radio"
                    checked={mode === 'ai'}
                    onChange={() => setMode('ai')}
                    className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300"
                  />
                  <label htmlFor="mode-ai" className="ml-3 block text-sm font-medium text-gray-700">
                    AI Mode - Automatic parameter optimization
                  </label>
                </div>
                <div className="flex items-center">
                  <input
                    id="mode-manual"
                    name="mode"
                    type="radio"
                    checked={mode === 'manual'}
                    onChange={() => setMode('manual')}
                    className="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300"
                  />
                  <label htmlFor="mode-manual" className="ml-3 block text-sm font-medium text-gray-700">
                    Manual Mode - Full control over parameters
                  </label>
                </div>
              </div>
            </div>
            
            <div>
              <label htmlFor="prompt" className="block text-sm font-medium text-gray-700">
                Prompt
              </label>
              <div className="mt-1">
                <textarea
                  id="prompt"
                  name="prompt"
                  rows={3}
                  className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md bg-white text-gray-900 placeholder-gray-400"
                  style={{ color: '#111827', fontSize: '15px' }}
                  placeholder="Describe what you want to generate... (e.g., 'Epic fantasy game character art with heroic pose')"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  required
                />
              </div>
            </div>
            
            {mode === 'manual' && (
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <div>
                  <label htmlFor="camera_angle" className="block text-sm font-medium text-gray-700">
                    Camera Angle
                  </label>
                  <select
                    id="camera_angle"
                    name="camera_angle"
                    className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                    value={parameters.camera_angle}
                    onChange={(e) => setParameters({...parameters, camera_angle: e.target.value})}
                  >
                    <option value="">Select...</option>
                    <option value="eye-level">Eye Level</option>
                    <option value="low-angle">Low Angle</option>
                    <option value="high-angle">High Angle</option>
                    <option value="dutch-tilt">Dutch Tilt</option>
                    <option value="bird's-eye">Bird's Eye</option>
                  </select>
                </div>
                
                <div>
                  <label htmlFor="fov" className="block text-sm font-medium text-gray-700">
                    Field of View
                  </label>
                  <select
                    id="fov"
                    name="fov"
                    className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                    value={parameters.fov}
                    onChange={(e) => setParameters({...parameters, fov: e.target.value})}
                  >
                    <option value="">Select...</option>
                    <option value="wide">Wide</option>
                    <option value="standard">Standard</option>
                    <option value="telephoto">Telephoto</option>
                  </select>
                </div>
                
                <div>
                  <label htmlFor="lighting" className="block text-sm font-medium text-gray-700">
                    Lighting
                  </label>
                  <select
                    id="lighting"
                    name="lighting"
                    className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                    value={parameters.lighting}
                    onChange={(e) => setParameters({...parameters, lighting: e.target.value})}
                  >
                    <option value="">Select...</option>
                    <option value="natural">Natural</option>
                    <option value="studio">Studio</option>
                    <option value="dramatic">Dramatic</option>
                    <option value="golden-hour">Golden Hour</option>
                  </select>
                </div>
                
                <div>
                  <label htmlFor="color_palette" className="block text-sm font-medium text-gray-700">
                    Color Palette
                  </label>
                  <select
                    id="color_palette"
                    name="color_palette"
                    className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                    value={parameters.color_palette}
                    onChange={(e) => setParameters({...parameters, color_palette: e.target.value})}
                  >
                    <option value="">Select...</option>
                    <option value="vibrant">Vibrant</option>
                    <option value="pastel">Pastel</option>
                    <option value="monochrome">Monochrome</option>
                    <option value="warm">Warm</option>
                    <option value="cool">Cool</option>
                  </select>
                </div>
                
                <div>
                  <label htmlFor="composition" className="block text-sm font-medium text-gray-700">
                    Composition
                  </label>
                  <select
                    id="composition"
                    name="composition"
                    className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                    value={parameters.composition}
                    onChange={(e) => setParameters({...parameters, composition: e.target.value})}
                  >
                    <option value="">Select...</option>
                    <option value="rule-of-thirds">Rule of Thirds</option>
                    <option value="centered">Centered</option>
                    <option value="dynamic">Dynamic</option>
                    <option value="minimal">Minimal</option>
                  </select>
                </div>
                
                <div>
                  <label htmlFor="style" className="block text-sm font-medium text-gray-700">
                    Style
                  </label>
                  <select
                    id="style"
                    name="style"
                    className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                    value={parameters.style}
                    onChange={(e) => setParameters({...parameters, style: e.target.value})}
                  >
                    <option value="">Select...</option>
                    <option value="photorealistic">Photorealistic</option>
                    <option value="cinematic">Cinematic</option>
                    <option value="editorial">Editorial</option>
                    <option value="commercial">Commercial</option>
                  </select>
                </div>
              </div>
            )}
            
            <div>
              <button
                type="submit"
                disabled={generateMutation.isLoading}
                className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {generateMutation.isLoading ? 'Generating...' : 'Generate Image'}
              </button>
            </div>
          </form>
          
          {result && (
            <div className="mt-8 border-t border-gray-200 pt-8">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Result</h3>
              <div className="bg-gray-50 rounded-lg p-4">
                {result.image_url && (
                  <div className="mb-4">
                    <img
                      src={result.image_url}
                      alt="Generated"
                      className="max-w-full h-auto rounded-lg shadow-lg"
                    />
                  </div>
                )}
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="font-medium">Status:</span> {result.status}
                  </div>
                  <div>
                    <span className="font-medium">Generation Time:</span> {result.generation_time?.toFixed(2)}s
                  </div>
                  <div>
                    <span className="font-medium">Quality Score:</span> {(result.quality_score * 100)?.toFixed(1)}%
                  </div>
                  <div>
                    <span className="font-medium">ID:</span> {result.id}
                  </div>
                </div>
                {result.reasoning && (
                  <div className="mt-4">
                    <h4 className="font-medium text-gray-900 mb-2">AI Reasoning</h4>
                    <div className="text-sm text-gray-600 space-y-1">
                      {Object.entries(result.reasoning).map(([key, value]) => (
                        <div key={key}>
                          <span className="font-medium capitalize">{key.replace('_', ' ')}:</span> {value}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Generator;
