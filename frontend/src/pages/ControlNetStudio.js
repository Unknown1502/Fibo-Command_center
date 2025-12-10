import React, { useState } from 'react';
import { Upload, Image, Sliders, Download, Eye, Zap, Info } from 'lucide-react';

const ControlNetStudio = () => {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [controlType, setControlType] = useState('canny_edge');
  const [strength, setStrength] = useState(0.7);
  const [sensitivity, setSensitivity] = useState('medium');
  const [processedImage, setProcessedImage] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [dragging, setDragging] = useState(false);

  const controlTypes = [
    {
      id: 'canny_edge',
      name: 'Canny Edge Detection',
      icon: '🔲',
      description: 'Extract sharp edges for precise structural control',
      useCase: 'Architecture, product outlines, technical drawings'
    },
    {
      id: 'depth_map',
      name: 'Depth Map',
      icon: '🌊',
      description: 'Generate depth information for 3D-like composition',
      useCase: 'Landscapes, portraits, spatial relationships'
    },
    {
      id: 'normal_map',
      name: 'Normal Map',
      icon: '🎨',
      description: 'Surface normal estimation for lighting and texture',
      useCase: 'Product design, material rendering, lighting studies'
    },
    {
      id: 'hed_edge',
      name: 'HED Boundary',
      icon: '✏️',
      description: 'Holistically-nested edge detection for soft boundaries',
      useCase: 'Artistic sketches, soft compositions, natural scenes'
    },
    {
      id: 'scribble',
      name: 'Scribble Control',
      icon: '✍️',
      description: 'Convert rough sketches into structured guidance',
      useCase: 'Concept art, quick ideation, artistic freedom'
    },
    {
      id: 'pose',
      name: 'Pose Estimation',
      icon: '🧍',
      description: 'Extract human pose keypoints for character control',
      useCase: 'Character art, fashion, human figures'
    }
  ];

  const handleFileUpload = (file) => {
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setUploadedImage(e.target.result);
        setProcessedImage(null);
      };
      reader.readAsDataURL(file);
    } else {
      alert('Please upload an image file (JPG, PNG, WebP)');
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    handleFileUpload(file);
  };

  const processImage = async () => {
    if (!uploadedImage) {
      alert('Please upload an image first');
      return;
    }

    setProcessing(true);
    
    // Simulate processing
    setTimeout(() => {
      setProcessedImage(uploadedImage); // In production, this would be the processed control image
      setProcessing(false);
      alert(`ControlNet processing complete!\n\nType: ${controlType}\nStrength: ${strength}\nSensitivity: ${sensitivity}\n\nIn production, this would call:\nPOST /api/controlnet/process`);
    }, 2000);
  };

  return (
    <div className="min-h-screen px-4 py-8 md:px-8 lg:px-12 xl:px-16">
      <div className="max-w-7xl mx-auto animate-slide-in">
        {/* Hero Section */}
        <div className="mb-8">
          <div className="inline-flex items-center gap-2 glass-card px-6 py-3 mb-4">
            <Image className="w-5 h-5 text-secondary animate-pulse" />
            <span className="text-secondary font-medium">Advanced Composition Control</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-gradient mb-3">
            ControlNet Studio
          </h1>
          <p className="text-xl text-secondary max-w-3xl">
            Transform reference images into precise control signals. Guide FIBO with edges, depth, pose, and more.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upload & Controls Section */}
          <div className="space-y-6">
            {/* Upload Zone */}
            <div className="glass-card p-6">
              <h3 className="text-xl font-bold text-primary mb-4 flex items-center gap-2">
                <Upload className="w-5 h-5" />
                Upload Reference Image
              </h3>
              
              <div
                onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
                onDragLeave={() => setDragging(false)}
                onDrop={handleDrop}
                className={`border-2 border-dashed rounded-xl p-8 text-center transition-all ${
                  dragging 
                    ? 'border-secondary bg-secondary/10' 
                    : 'border-glass-border hover:border-secondary/50'
                }`}
              >
                {uploadedImage ? (
                  <div>
                    <img 
                      src={uploadedImage} 
                      alt="Uploaded" 
                      className="max-w-full h-48 mx-auto rounded-lg object-contain mb-4"
                    />
                    <button
                      onClick={() => setUploadedImage(null)}
                      className="text-error text-sm hover:underline"
                    >
                      Remove Image
                    </button>
                  </div>
                ) : (
                  <div>
                    <Upload className="w-12 h-12 mx-auto mb-3 text-secondary" />
                    <p className="text-primary font-semibold mb-2">Drop image here</p>
                    <p className="text-tertiary text-sm mb-4">or</p>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={(e) => handleFileUpload(e.target.files[0])}
                      className="hidden"
                      id="image-upload"
                    />
                    <label htmlFor="image-upload" className="btn-modern cursor-pointer inline-flex items-center gap-2 bg-gradient-to-r from-secondary to-pink-500">
                      <Image className="w-5 h-5" />
                      Browse Files
                    </label>
                  </div>
                )}
              </div>
            </div>

            {/* Control Type Selection */}
            <div className="glass-card p-6">
              <h3 className="text-xl font-bold text-primary mb-4 flex items-center gap-2">
                <Sliders className="w-5 h-5" />
                Control Type
              </h3>
              <div className="grid grid-cols-2 gap-3">
                {controlTypes.map((type) => (
                  <button
                    key={type.id}
                    onClick={() => setControlType(type.id)}
                    className={`glass-card p-4 text-left transition-all hover:scale-105 ${
                      controlType === type.id 
                        ? 'bg-gradient-to-br from-secondary/20 to-accent/20 border-2 border-secondary' 
                        : 'hover:bg-bg-hover'
                    }`}
                    title={type.description}
                  >
                    <div className="text-3xl mb-2">{type.icon}</div>
                    <div className="font-semibold text-primary text-sm">{type.name}</div>
                  </button>
                ))}
              </div>
            </div>

            {/* Control Parameters */}
            <div className="glass-card p-6">
              <h3 className="text-xl font-bold text-primary mb-4">Parameters</h3>
              
              {/* Strength Slider */}
              <div className="mb-6">
                <label className="flex items-center justify-between mb-3">
                  <span className="text-secondary font-semibold">Control Strength</span>
                  <span className="badge-modern">{(strength * 100).toFixed(0)}%</span>
                </label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  value={strength}
                  onChange={(e) => setStrength(parseFloat(e.target.value))}
                  className="w-full h-2 bg-bg-card rounded-lg appearance-none cursor-pointer"
                  style={{
                    background: `linear-gradient(to right, var(--secondary) 0%, var(--secondary) ${strength * 100}%, var(--bg-card) ${strength * 100}%, var(--bg-card) 100%)`
                  }}
                />
                <div className="flex justify-between text-xs text-tertiary mt-2">
                  <span>Subtle</span>
                  <span>Balanced</span>
                  <span>Strong</span>
                </div>
              </div>

              {/* Sensitivity Selection */}
              <div>
                <label className="block text-secondary font-semibold mb-3">Detection Sensitivity</label>
                <div className="grid grid-cols-3 gap-3">
                  {['low', 'medium', 'high'].map((level) => (
                    <button
                      key={level}
                      onClick={() => setSensitivity(level)}
                      className={`glass-card px-4 py-3 font-semibold capitalize transition-all ${
                        sensitivity === level 
                          ? 'bg-gradient-to-r from-accent to-emerald-500 text-white' 
                          : 'text-secondary hover:bg-bg-hover'
                      }`}
                    >
                      {level}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Process Button */}
            <button
              onClick={processImage}
              disabled={!uploadedImage || processing}
              className="btn-modern w-full py-4 text-lg flex items-center justify-center gap-3 bg-gradient-to-r from-secondary to-pink-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {processing ? (
                <>
                  <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  <Zap className="w-6 h-6" />
                  Process Control Image
                </>
              )}
            </button>
          </div>

          {/* Preview & Info Section */}
          <div className="space-y-6">
            {/* Control Type Info */}
            <div className="glass-card p-6 border-l-4 border-accent">
              <div className="flex items-start gap-4">
                <div className="text-5xl">
                  {controlTypes.find(t => t.id === controlType)?.icon}
                </div>
                <div>
                  <h3 className="text-xl font-bold text-primary mb-2">
                    {controlTypes.find(t => t.id === controlType)?.name}
                  </h3>
                  <p className="text-secondary mb-3">
                    {controlTypes.find(t => t.id === controlType)?.description}
                  </p>
                  <div className="glass-card p-3 bg-accent/10">
                    <div className="text-accent font-semibold text-sm mb-1">Best For:</div>
                    <div className="text-secondary text-sm">
                      {controlTypes.find(t => t.id === controlType)?.useCase}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Preview */}
            <div className="glass-card p-6">
              <h3 className="text-xl font-bold text-primary mb-4 flex items-center gap-2">
                <Eye className="w-5 h-5" />
                Processed Control Image
              </h3>
              <div className="bg-bg-card rounded-xl overflow-hidden min-h-[300px] flex items-center justify-center">
                {processedImage ? (
                  <img 
                    src={processedImage} 
                    alt="Processed" 
                    className="max-w-full h-auto"
                  />
                ) : (
                  <div className="text-center py-12">
                    <Image className="w-16 h-16 mx-auto mb-4 text-tertiary opacity-50" />
                    <p className="text-secondary">Upload and process an image to see results</p>
                  </div>
                )}
              </div>
              
              {processedImage && (
                <button className="btn-modern w-full mt-4 flex items-center justify-center gap-2">
                  <Download className="w-5 h-5" />
                  Download Control Image
                </button>
              )}
            </div>

            {/* Quick Tips */}
            <div className="glass-card p-6 bg-primary/5">
              <h4 className="font-bold text-primary mb-3 flex items-center gap-2">
                <Info className="w-5 h-5 text-primary-light" />
                Pro Tips
              </h4>
              <ul className="space-y-2 text-sm text-secondary">
                <li className="flex gap-2">
                  <span className="text-accent">→</span>
                  <span>Use <strong>Canny Edge</strong> for precise structural control</span>
                </li>
                <li className="flex gap-2">
                  <span className="text-accent">→</span>
                  <span>Try <strong>Depth Map</strong> for atmospheric perspective</span>
                </li>
                <li className="flex gap-2">
                  <span className="text-accent">→</span>
                  <span><strong>Pose Estimation</strong> works best with clear body visibility</span>
                </li>
                <li className="flex gap-2">
                  <span className="text-accent">→</span>
                  <span>Lower strength (30-50%) for subtle guidance</span>
                </li>
                <li className="flex gap-2">
                  <span className="text-accent">→</span>
                  <span>Higher strength (70-90%) for strict adherence</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ControlNetStudio;
