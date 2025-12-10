import React, { useState } from 'react';
import { Upload, FileText, CheckCircle, AlertTriangle, Shield, Download, Eye } from 'lucide-react';

const BrandGuidelines = () => {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [guidelines, setGuidelines] = useState([]);
  const [selectedGuideline, setSelectedGuideline] = useState(null);
  const [validationResult, setValidationResult] = useState(null);
  const [dragging, setDragging] = useState(false);

  // Mock guidelines data
  const mockGuidelines = [
    {
      id: 'brand_001',
      name: 'Nike Brand Guidelines',
      uploaded: '2025-12-07',
      rules_count: 24,
      last_used: '2 hours ago',
      compliance_avg: 94
    },
    {
      id: 'brand_002',
      name: 'Apple Product Photography',
      uploaded: '2025-12-05',
      rules_count: 18,
      last_used: '1 day ago',
      compliance_avg: 98
    }
  ];

  const mockValidation = {
    compliance_score: 87,
    violations: [
      { severity: 'high', rule: 'Color Palette', message: 'Using non-brand colors (detected: #FF5733, should use brand palette)', suggestion: 'Use brand-approved color_palette: "corporate_blue"' },
      { severity: 'medium', rule: 'Composition', message: 'Product not centered as per brand guidelines', suggestion: 'Set composition to "centered" or "symmetrical"' },
      { severity: 'low', rule: 'Lighting', message: 'Lighting style preference: soft diffused', suggestion: 'Consider using lighting: "soft" for consistency' }
    ],
    warnings: [
      'Camera angle preference: eye_level for products',
      'Background should be minimalist and clean'
    ],
    approved_parameters: {
      camera_angle: 'eye_level',
      lighting: 'soft',
      color_palette: 'neutral',
      composition: 'centered',
      style: 'clean_minimalist'
    }
  };

  const handleFileUpload = (file) => {
    if (file) {
      setUploadedFile(file);
      setTimeout(() => {
        alert(`Brand guidelines "${file.name}" uploaded successfully!\n\nIn production, this would:\n1. Parse PDF/DOC for brand rules\n2. Extract color codes, fonts, styles\n3. Create validation criteria\n4. Store in backend: POST /api/brand/guidelines`);
        setGuidelines([...mockGuidelines, {
          id: `brand_${Date.now()}`,
          name: file.name,
          uploaded: 'Just now',
          rules_count: 15,
          last_used: 'Never',
          compliance_avg: 0
        }]);
        setUploadedFile(null);
      }, 1000);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file && (file.type === 'application/pdf' || file.type.includes('document'))) {
      handleFileUpload(file);
    } else {
      alert('Please upload PDF or DOC files');
    }
  };

  const validateGeneration = (guidelineId) => {
    setValidationResult(mockValidation);
  };

  return (
    <div className="min-h-screen px-4 py-8 md:px-8 lg:px-12 xl:px-16">
      <div className="max-w-7xl mx-auto animate-slide-in">
        {/* Hero Section */}
        <div className="mb-8">
          <div className="inline-flex items-center gap-2 glass-card px-6 py-3 mb-4">
            <Shield className="w-5 h-5 text-accent animate-pulse" />
            <span className="text-secondary font-medium">Brand Consistency</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-gradient mb-3">
            Brand Guidelines Manager
          </h1>
          <p className="text-xl text-secondary max-w-3xl">
            Upload brand documents, enforce identity rules, and ensure 100% compliance across all generated content.
          </p>
        </div>

        {/* Upload Section */}
        <div className="glass-card p-8 mb-8">
          <h3 className="text-2xl font-bold text-primary mb-6 flex items-center gap-3">
            <Upload className="w-6 h-6 text-accent" />
            Upload Brand Guidelines
          </h3>
          
          <div
            onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
            onDragLeave={() => setDragging(false)}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-xl p-12 text-center transition-all ${
              dragging 
                ? 'border-accent bg-accent/10' 
                : 'border-glass-border hover:border-accent/50'
            }`}
          >
            <div className="max-w-md mx-auto">
              <Upload className="w-16 h-16 mx-auto mb-4 text-accent" />
              <h4 className="text-xl font-bold text-primary mb-2">
                Drag & Drop Brand Documents
              </h4>
              <p className="text-secondary mb-4">
                or click to browse
              </p>
              <input
                type="file"
                accept=".pdf,.doc,.docx"
                onChange={(e) => handleFileUpload(e.target.files[0])}
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="btn-modern cursor-pointer inline-flex items-center gap-2">
                <FileText className="w-5 h-5" />
                Select File
              </label>
              <p className="text-tertiary text-sm mt-4">
                Supports PDF, DOC, DOCX • Max 10MB
              </p>
            </div>
          </div>
        </div>

        {/* Existing Guidelines */}
        <div className="mb-8">
          <h3 className="text-2xl font-bold text-primary mb-6 flex items-center gap-3">
            <FileText className="w-6 h-6 text-primary-light" />
            Active Brand Guidelines
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {mockGuidelines.map((guideline) => (
              <div key={guideline.id} className="glass-card p-6 hover-glow">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h4 className="text-xl font-bold text-primary mb-2">{guideline.name}</h4>
                    <div className="text-sm text-tertiary">ID: {guideline.id}</div>
                  </div>
                  <button
                    onClick={() => validateGeneration(guideline.id)}
                    className="glass-card px-4 py-2 hover:bg-hover flex items-center gap-2 text-sm font-semibold"
                  >
                    <Eye className="w-4 h-4" />
                    Validate
                  </button>
                </div>

                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <div className="text-tertiary text-xs mb-1">Rules Count</div>
                    <div className="text-lg font-bold text-primary">{guideline.rules_count}</div>
                  </div>
                  <div>
                    <div className="text-tertiary text-xs mb-1">Avg Compliance</div>
                    <div className="text-lg font-bold text-accent">{guideline.compliance_avg}%</div>
                  </div>
                  <div>
                    <div className="text-tertiary text-xs mb-1">Last Used</div>
                    <div className="text-sm font-semibold text-secondary">{guideline.last_used}</div>
                  </div>
                  <div>
                    <div className="text-tertiary text-xs mb-1">Uploaded</div>
                    <div className="text-sm font-semibold text-secondary">{guideline.uploaded}</div>
                  </div>
                </div>

                <div className="h-2 bg-bg-card rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-success to-accent transition-all"
                    style={{ width: `${guideline.compliance_avg}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Validation Results */}
        {validationResult && (
          <div className="glass-card p-8 animate-fade-in">
            <h3 className="text-2xl font-bold text-primary mb-6 flex items-center gap-3">
              <CheckCircle className="w-6 h-6 text-success" />
              Validation Results
            </h3>

            {/* Compliance Score */}
            <div className="glass-card p-6 bg-gradient-to-r from-success/10 to-accent/10 mb-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <div className="text-tertiary text-sm mb-1">Overall Compliance Score</div>
                  <div className="text-5xl font-bold text-success">{validationResult.compliance_score}%</div>
                </div>
                <div className="text-6xl">
                  {validationResult.compliance_score >= 90 ? '✅' : 
                   validationResult.compliance_score >= 70 ? '⚠️' : '❌'}
                </div>
              </div>
              <div className="h-3 bg-bg-card rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-success to-accent transition-all duration-1000"
                  style={{ width: `${validationResult.compliance_score}%` }}
                />
              </div>
            </div>

            {/* Violations */}
            {validationResult.violations.length > 0 && (
              <div className="mb-6">
                <h4 className="text-xl font-bold text-primary mb-4 flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-warning" />
                  Violations Found
                </h4>
                <div className="space-y-4">
                  {validationResult.violations.map((violation, idx) => (
                    <div
                      key={idx}
                      className={`glass-card p-5 border-l-4 ${
                        violation.severity === 'high' ? 'border-error' :
                        violation.severity === 'medium' ? 'border-warning' :
                        'border-primary-light'
                      }`}
                    >
                      <div className="flex items-start gap-4">
                        <span className="text-3xl">
                          {violation.severity === 'high' ? '🚨' :
                           violation.severity === 'medium' ? '⚠️' : 'ℹ️'}
                        </span>
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <span className={`badge-modern ${
                              violation.severity === 'high' ? 'bg-error/20 text-error border-error/30' :
                              violation.severity === 'medium' ? 'bg-warning/20 text-warning border-warning/30' :
                              'bg-primary/20 text-primary-light border-primary/30'
                            }`}>
                              {violation.severity.toUpperCase()}
                            </span>
                            <span className="font-bold text-primary">{violation.rule}</span>
                          </div>
                          <p className="text-secondary mb-3">{violation.message}</p>
                          <div className="glass-card p-3 bg-accent/10">
                            <div className="text-accent font-semibold text-sm mb-1">💡 Suggestion:</div>
                            <div className="text-secondary text-sm">{violation.suggestion}</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Warnings */}
            {validationResult.warnings && validationResult.warnings.length > 0 && (
              <div className="mb-6">
                <h4 className="text-xl font-bold text-primary mb-4">Warnings & Recommendations</h4>
                <div className="glass-card p-5 bg-warning/5">
                  <ul className="space-y-2">
                    {validationResult.warnings.map((warning, idx) => (
                      <li key={idx} className="flex items-start gap-3 text-secondary">
                        <span className="text-warning">⚡</span>
                        <span>{warning}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {/* Approved Parameters */}
            <div>
              <h4 className="text-xl font-bold text-primary mb-4 flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-success" />
                Brand-Approved Parameters
              </h4>
              <div className="glass-card p-6 bg-success/5">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {Object.entries(validationResult.approved_parameters).map(([key, value]) => (
                    <div key={key} className="flex justify-between items-center p-3 rounded-lg bg-bg-hover">
                      <span className="text-secondary capitalize">{key.replace(/_/g, ' ')}</span>
                      <span className="badge-modern bg-success/20 text-success border-success/30">{value}</span>
                    </div>
                  ))}
                </div>
                <button className="btn-modern w-full mt-6 bg-gradient-to-r from-success to-accent">
                  <Download className="w-5 h-5 mr-2 inline" />
                  Apply These Parameters to Generation
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BrandGuidelines;
