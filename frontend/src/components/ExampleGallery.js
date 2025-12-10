import React, { useState, useEffect } from 'react';
import { Image, ExternalLink, Zap, Clock, TrendingUp, Filter } from 'lucide-react';

const ExampleGallery = () => {
  const [examples, setExamples] = useState([]);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load example manifest
    fetch('/examples/manifest.json')
      .then(res => res.json())
      .then(data => {
        setExamples(data.images || []);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load examples:', err);
        setLoading(false);
      });
  }, []);

  const categories = ['all', 'ecommerce', 'social', 'games'];
  
  const filteredExamples = filter === 'all' 
    ? examples 
    : examples.filter(ex => ex.category === filter);

  const stats = {
    total: examples.length,
    avgQuality: examples.length > 0 
      ? (examples.reduce((sum, ex) => sum + (ex.quality_score || 0), 0) / examples.length).toFixed(2)
      : 0,
    avgTime: examples.length > 0
      ? (examples.reduce((sum, ex) => sum + (ex.generation_time || 0), 0) / examples.length).toFixed(1)
      : 0,
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-accent mb-4"></div>
          <p className="text-secondary">Loading examples...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-slide-in">
      {/* Stats Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-card p-6 text-center">
          <div className="flex items-center justify-center mb-2">
            <Image className="w-5 h-5 text-accent mr-2" />
            <span className="text-tertiary text-sm font-semibold">Total Images</span>
          </div>
          <div className="text-4xl font-bold text-primary">{stats.total}</div>
          <div className="text-xs text-secondary mt-1">Generated with BRIA API</div>
        </div>
        
        <div className="glass-card p-6 text-center">
          <div className="flex items-center justify-center mb-2">
            <TrendingUp className="w-5 h-5 text-green-400 mr-2" />
            <span className="text-tertiary text-sm font-semibold">Avg Quality Score</span>
          </div>
          <div className="text-4xl font-bold text-primary">{stats.avgQuality}</div>
          <div className="text-xs text-secondary mt-1">Out of 1.0 maximum</div>
        </div>
        
        <div className="glass-card p-6 text-center">
          <div className="flex items-center justify-center mb-2">
            <Clock className="w-5 h-5 text-blue-400 mr-2" />
            <span className="text-tertiary text-sm font-semibold">Avg Generation Time</span>
          </div>
          <div className="text-4xl font-bold text-primary">{stats.avgTime}s</div>
          <div className="text-xs text-secondary mt-1">Per image</div>
        </div>
      </div>

      {/* Category Filter */}
      <div className="flex items-center gap-4 flex-wrap">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-accent" />
          <span className="text-sm font-medium text-secondary">Filter:</span>
        </div>
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => setFilter(cat)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              filter === cat
                ? 'bg-gradient-to-r from-accent to-emerald-500 text-white'
                : 'glass-card hover:bg-white/10 text-secondary'
            }`}
          >
            {cat.charAt(0).toUpperCase() + cat.slice(1)}
          </button>
        ))}
      </div>

      {/* Gallery Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredExamples.map((example, index) => (
          <div
            key={index}
            className="glass-card overflow-hidden hover-glow group"
            style={{ animationDelay: `${(index % 9) * 50}ms` }}
          >
            {/* Image */}
            <div className="relative aspect-square bg-dark-lighter overflow-hidden">
              <img
                src={example.image_url}
                alt={example.name}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                loading="lazy"
              />
              <div className="absolute top-2 right-2">
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                  example.category === 'ecommerce' ? 'bg-blue-500/80' :
                  example.category === 'social' ? 'bg-pink-500/80' :
                  'bg-purple-500/80'
                } text-white`}>
                  {example.category}
                </span>
              </div>
              <div className="absolute inset-0 bg-gradient-to-t from-dark/90 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            </div>
            
            {/* Info */}
            <div className="p-4 space-y-3">
              <div>
                <h3 className="text-lg font-semibold text-primary mb-1 capitalize">
                  {example.name.replace(/_/g, ' ')}
                </h3>
                <p className="text-xs text-tertiary line-clamp-2">
                  {example.prompt}
                </p>
              </div>
              
              {/* Metrics */}
              <div className="flex items-center gap-4 text-xs">
                <div className="flex items-center gap-1">
                  <TrendingUp className="w-3 h-3 text-green-400" />
                  <span className="text-secondary">
                    Quality: <span className="text-primary font-semibold">{example.quality_score}</span>
                  </span>
                </div>
                <div className="flex items-center gap-1">
                  <Clock className="w-3 h-3 text-blue-400" />
                  <span className="text-secondary">
                    {example.generation_time.toFixed(1)}s
                  </span>
                </div>
              </div>
              
              {/* View Button */}
              <a
                href={example.image_url}
                target="_blank"
                rel="noopener noreferrer"
                className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-sm font-medium text-accent transition-colors"
              >
                <ExternalLink className="w-4 h-4" />
                View Full Size
              </a>
            </div>
          </div>
        ))}
      </div>

      {filteredExamples.length === 0 && (
        <div className="text-center py-12">
          <p className="text-secondary">No examples found in this category.</p>
        </div>
      )}
    </div>
  );
};

export default ExampleGallery;
