import React, { useState, useEffect } from 'react';
import { Save, Download, Upload, Lock, Unlock, Copy, RefreshCw } from 'lucide-react';

const VisualEditor = () => {
  const [parameters, setParameters] = useState({
    camera_angle: 'eye_level',
    field_of_view: 'normal',
    lighting: 'soft',
    color_palette: 'neutral',
    composition: 'centered',
    style: 'realistic',
    num_results: 1,
    seed: Math.floor(Math.random() * 1000000)
  });

  const [locked, setLocked] = useState({});
  const [presets, setPresets] = useState([]);
  const [presetName, setPresetName] = useState('');
  const [jsonView, setJsonView] = useState('');

  // Parameter definitions with icons and tooltips
  const parameterConfig = {
    camera_angle: {
      label: 'Camera Angle',
      icon: '📷',
      options: [
        { value: 'eye_level', label: 'Eye Level', tooltip: 'Natural, direct view - ideal for portraits and products' },
        { value: 'low_angle', label: 'Low Angle', tooltip: 'Looking up - makes subject appear powerful, dramatic' },
        { value: 'high_angle', label: 'High Angle', tooltip: 'Looking down - provides overview, makes subject vulnerable' },
        { value: 'birds_eye', label: "Bird's Eye", tooltip: 'Directly overhead - perfect for flat lays, food, patterns' },
        { value: 'dutch_angle', label: 'Dutch Angle', tooltip: 'Tilted horizon - creates tension, unease, dynamic energy' }
      ]
    },
    field_of_view: {
      label: 'Field of View',
      icon: '🔭',
      options: [
        { value: 'extreme_wide', label: 'Extreme Wide', tooltip: 'Ultra-wide perspective - landscape, architecture, context' },
        { value: 'wide', label: 'Wide', tooltip: 'Broad view - environmental shots, establishing scenes' },
        { value: 'normal', label: 'Normal', tooltip: 'Natural perspective - portraits, products, general use' },
        { value: 'telephoto', label: 'Telephoto', tooltip: 'Narrow focus - compression, subject isolation, details' },
        { value: 'macro', label: 'Macro', tooltip: 'Extreme close-up - textures, tiny details, product features' }
      ]
    },
    lighting: {
      label: 'Lighting',
      icon: '💡',
      options: [
        { value: 'soft', label: 'Soft', tooltip: 'Diffused, gentle - beauty, portraits, even tones' },
        { value: 'hard', label: 'Hard', tooltip: 'Strong shadows - dramatic, editorial, high contrast' },
        { value: 'backlit', label: 'Backlit', tooltip: 'Light from behind - silhouettes, glows, ethereal mood' },
        { value: 'golden_hour', label: 'Golden Hour', tooltip: 'Warm sunset/sunrise - romantic, cinematic, natural beauty' },
        { value: 'studio', label: 'Studio', tooltip: 'Controlled professional - products, portraits, clean look' }
      ]
    },
    color_palette: {
      label: 'Color Palette',
      icon: '🎨',
      options: [
        { value: 'vibrant', label: 'Vibrant', tooltip: 'Bold, saturated colors - energetic, playful, attention-grabbing' },
        { value: 'muted', label: 'Muted', tooltip: 'Desaturated tones - sophisticated, calm, vintage feel' },
        { value: 'monochrome', label: 'Monochrome', tooltip: 'Black & white - timeless, dramatic, artistic' },
        { value: 'pastel', label: 'Pastel', tooltip: 'Soft, light colors - gentle, feminine, dreamy aesthetic' },
        { value: 'neutral', label: 'Neutral', tooltip: 'Natural, balanced - versatile, professional, realistic' }
      ]
    },
    composition: {
      label: 'Composition',
      icon: '🖼️',
      options: [
        { value: 'centered', label: 'Centered', tooltip: 'Subject in middle - balanced, stable, symmetric' },
        { value: 'rule_of_thirds', label: 'Rule of Thirds', tooltip: 'Off-center placement - dynamic, professional, natural' },
        { value: 'leading_lines', label: 'Leading Lines', tooltip: 'Visual guides to subject - depth, movement, focus' },
        { value: 'symmetrical', label: 'Symmetrical', tooltip: 'Mirror balance - formal, harmonious, architectural' },
        { value: 'dynamic', label: 'Dynamic', tooltip: 'Diagonal energy - movement, action, excitement' }
      ]
    },
    style: {
      label: 'Style',
      icon: '🎭',
      options: [
        { value: 'realistic', label: 'Realistic', tooltip: 'True-to-life - products, portraits, documentation' },
        { value: 'artistic', label: 'Artistic', tooltip: 'Creative interpretation - expressive, unique, conceptual' },
        { value: 'minimalist', label: 'Minimalist', tooltip: 'Simple, clean - modern, focused, elegant' },
        { value: 'vintage', label: 'Vintage', tooltip: 'Retro aesthetic - nostalgic, film-like, textured' },
        { value: 'cinematic', label: 'Cinematic', tooltip: 'Film quality - dramatic, moody, storytelling' }
      ]
    },
    num_results: {
      label: 'Number of Results',
      icon: '🔢',
      type: 'slider',
      min: 1,
      max: 4,
      tooltip: 'How many variations to generate (1-4)'
    },
    seed: {
      label: 'Seed',
      icon: '🎲',
      type: 'number',
      tooltip: 'Random seed for reproducibility. Same seed = same result'
    }
  };

  // Update JSON view when parameters change
  useEffect(() => {
    setJsonView(JSON.stringify(parameters, null, 2));
  }, [parameters]);

  // Load presets from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('fibo_presets');
    if (saved) {
      setPresets(JSON.parse(saved));
    }
  }, []);

  const handleParameterChange = (key, value) => {
    if (!locked[key]) {
      setParameters(prev => ({ ...prev, [key]: value }));
    }
  };

  const toggleLock = (key) => {
    setLocked(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const savePreset = () => {
    if (!presetName.trim()) {
      alert('Please enter a preset name');
      return;
    }

    const newPreset = {
      name: presetName,
      parameters: { ...parameters },
      timestamp: new Date().toISOString()
    };

    const updated = [...presets, newPreset];
    setPresets(updated);
    localStorage.setItem('fibo_presets', JSON.stringify(updated));
    setPresetName('');
    alert('Preset saved!');
  };

  const loadPreset = (preset) => {
    // Only update unlocked parameters
    const updated = { ...parameters };
    Object.keys(preset.parameters).forEach(key => {
      if (!locked[key]) {
        updated[key] = preset.parameters[key];
      }
    });
    setParameters(updated);
  };

  const deletePreset = (index) => {
    const updated = presets.filter((_, i) => i !== index);
    setPresets(updated);
    localStorage.setItem('fibo_presets', JSON.stringify(updated));
  };

  const exportPreset = () => {
    const dataStr = JSON.stringify(parameters, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
    const exportFileDefaultName = `fibo_preset_${Date.now()}.json`;

    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const importPreset = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const imported = JSON.parse(e.target.result);
          setParameters(imported);
          alert('Preset imported successfully!');
        } catch (error) {
          alert('Invalid preset file');
        }
      };
      reader.readAsText(file);
    }
  };

  const randomizeSeed = () => {
    setParameters(prev => ({ ...prev, seed: Math.floor(Math.random() * 1000000) }));
  };

  const copyJSON = () => {
    navigator.clipboard.writeText(jsonView);
    alert('JSON copied to clipboard!');
  };

  const renderParameterControl = (key, config) => {
    if (config.type === 'slider') {
      return (
        <div className="space-y-3">
          <input
            type="range"
            min={config.min}
            max={config.max}
            value={parameters[key]}
            onChange={(e) => handleParameterChange(key, parseInt(e.target.value))}
            disabled={locked[key]}
            className="w-full h-3 bg-gradient-to-r from-indigo-500/30 to-purple-500/30 rounded-lg appearance-none cursor-pointer disabled:opacity-50 slider-thumb"
            style={{
              background: `linear-gradient(to right, 
                #6366f1 0%, 
                #6366f1 ${((parameters[key] - config.min) / (config.max - config.min)) * 100}%, 
                rgba(99, 102, 241, 0.2) ${((parameters[key] - config.min) / (config.max - config.min)) * 100}%, 
                rgba(99, 102, 241, 0.2) 100%)`
            }}
          />
          <div className="text-center">
            <span className="text-4xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
              {parameters[key]}
            </span>
          </div>
        </div>
      );
    }

    if (config.type === 'number') {
      return (
        <div className="flex space-x-3">
          <input
            type="number"
            value={parameters[key]}
            onChange={(e) => handleParameterChange(key, parseInt(e.target.value))}
            disabled={locked[key]}
            className="input-modern flex-1 text-center text-lg font-semibold"
          />
          <button
            onClick={randomizeSeed}
            className="px-4 py-3 bg-indigo-500/20 text-indigo-400 rounded-lg hover:bg-indigo-500/30 transition-all duration-300"
            title="Randomize seed"
          >
            <RefreshCw size={20} />
          </button>
        </div>
      );
    }

    return (
      <div className="grid grid-cols-1 gap-3">
        {config.options.map(option => (
          <button
            key={option.value}
            onClick={() => handleParameterChange(key, option.value)}
            disabled={locked[key]}
            className={`px-5 py-4 rounded-xl text-left transition-all duration-300 ${
              parameters[key] === option.value
                ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-xl shadow-indigo-500/50 scale-105 transform'
                : 'bg-white/5 text-gray-300 hover:bg-white/10 hover:scale-102'
            } disabled:opacity-50 disabled:cursor-not-allowed border border-white/10`}
            title={option.tooltip}
          >
            <div className="font-semibold text-base">{option.label}</div>
            <div className="text-xs mt-1 opacity-75">{option.tooltip}</div>
          </button>
        ))}
      </div>
    );
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="mb-8 text-center animate-fade-in">
        <div className="inline-flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 rounded-full mb-4">
          <span className="text-2xl">🎨</span>
          <span className="text-sm font-medium text-white">Interactive Parameter Studio</span>
        </div>
        <h1 className="text-5xl font-bold text-white mb-3">
          <span className="text-gradient">Visual Parameter Editor</span>
        </h1>
        <p className="text-xl text-gray-300">Craft perfect FIBO parameters with intuitive controls</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Parameter Controls */}
        <div className="lg:col-span-2 space-y-6">
          {Object.entries(parameterConfig).map(([key, config]) => (
            <div key={key} className="glass-card animate-slide-in p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <span className="text-3xl animate-pulse">{config.icon}</span>
                  <h3 className="text-xl font-semibold text-white">{config.label}</h3>
                </div>
                <button
                  onClick={() => toggleLock(key)}
                  className={`p-2.5 rounded-lg transition-all duration-300 ${
                    locked[key] 
                      ? 'bg-red-500/20 text-red-400 hover:bg-red-500/30' 
                      : 'bg-gray-500/20 text-gray-400 hover:bg-gray-500/30'
                  }`}
                  title={locked[key] ? 'Unlock parameter' : 'Lock parameter'}
                >
                  {locked[key] ? <Lock size={20} /> : <Unlock size={20} />}
                </button>
              </div>
              <p className="text-sm text-gray-400 mb-4">{config.tooltip}</p>
              {renderParameterControl(key, config)}
            </div>
          ))}
        </div>

        {/* Right: JSON Preview & Presets */}
        <div className="space-y-6">
          {/* JSON Preview */}
          <div className="glass-card p-6 sticky top-6 animate-slide-in">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-semibold text-white">JSON Preview</h3>
              <button
                onClick={copyJSON}
                className="p-2.5 bg-indigo-500/20 text-indigo-400 rounded-lg hover:bg-indigo-500/30 transition-all duration-300"
                title="Copy JSON"
              >
                <Copy size={20} />
              </button>
            </div>
            <pre className="bg-black/30 p-4 rounded-lg text-xs overflow-auto max-h-96 font-mono text-green-400 border border-green-500/20">
              {jsonView}
            </pre>

            <div className="mt-4 space-y-3">
              <button
                onClick={exportPreset}
                className="btn-modern w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 flex items-center justify-center space-x-2"
              >
                <Download size={20} />
                <span>Export JSON</span>
              </button>
              <label className="btn-modern w-full bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 flex items-center justify-center space-x-2 cursor-pointer">
                <Upload size={20} />
                <span>Import JSON</span>
                <input
                  type="file"
                  accept=".json"
                  onChange={importPreset}
                  className="hidden"
                />
              </label>
            </div>
          </div>

          {/* Presets */}
          <div className="glass-card p-6 animate-slide-in">
            <h3 className="text-xl font-semibold text-white mb-4">Saved Presets</h3>
            
            <div className="mb-4">
              <input
                type="text"
                value={presetName}
                onChange={(e) => setPresetName(e.target.value)}
                placeholder="Enter preset name..."
                className="input-modern w-full mb-3"
              />
              <button
                onClick={savePreset}
                className="btn-modern w-full bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 flex items-center justify-center space-x-2"
              >
                <Save size={20} />
                <span>Save Current as Preset</span>
              </button>
            </div>

            <div className="space-y-2 max-h-64 overflow-y-auto">
              {presets.length === 0 ? (
                <p className="text-sm text-gray-400 text-center py-8">No saved presets yet</p>
              ) : (
                presets.map((preset, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-all duration-300">
                    <button
                      onClick={() => loadPreset(preset)}
                      className="flex-1 text-left text-sm font-medium text-white hover:text-indigo-400 transition-colors"
                    >
                      {preset.name}
                    </button>
                    <button
                      onClick={() => deletePreset(index)}
                      className="ml-2 text-red-400 hover:text-red-300 text-xs px-3 py-1 bg-red-500/10 rounded-md hover:bg-red-500/20 transition-all"
                    >
                      Delete
                    </button>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VisualEditor;
