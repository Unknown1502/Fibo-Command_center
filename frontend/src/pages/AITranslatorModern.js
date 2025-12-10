import React, { useState } from 'react';
import { useMutation } from 'react-query';
import { aiAPI } from '../services/api';
import { Sparkles, Wand2, Copy, Download, ArrowRight, Lightbulb, Zap } from 'lucide-react';

const AITranslator = () => {
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState(null);

  const translateMutation = useMutation(aiAPI.translate, {
    onSuccess: (data) => {
      setResult(data);
    },
    onError: (error) => {
      alert('Translation failed: ' + (error.response?.data?.detail || error.message));
    },
  });

  const handleTranslate = (e) => {
    e.preventDefault();
    translateMutation.mutate({
      prompt,
      context: { use_case: 'general' },
    });
  };

  const handleUseParameters = () => {
    if (result && result.parameters) {
      localStorage.setItem('fibo_translated_params', JSON.stringify(result.parameters));
      const notification = document.createElement('div');
      notification.className = 'fixed top-4 right-4 glass-card px-6 py-4 animate-slide-in z-50';
      notification.innerHTML = `
        <div class="flex items-center gap-3">
          <div class="text-2xl">✅</div>
          <div>
            <div class="text-primary font-semibold">Parameters Saved!</div>
            <div class="text-secondary text-sm">Ready to use in Generate page</div>
          </div>
        </div>
      `;
      document.body.appendChild(notification);
      setTimeout(() => notification.remove(), 3000);
    }
  };

  const examples = [
    { text: "Dramatic luxury watch commercial with cinematic lighting", icon: "⌚", gradient: "from-yellow-500 to-orange-500" },
    { text: "Bright cheerful summer beach collection for Instagram", icon: "🏖️", gradient: "from-cyan-500 to-blue-500" },
    { text: "Professional clean product photography for e-commerce", icon: "📦", gradient: "from-purple-500 to-pink-500" },
    { text: "Epic fantasy game character art with heroic pose", icon: "⚔️", gradient: "from-red-500 to-purple-500" },
    { text: "Minimalist modern architecture for magazine editorial", icon: "🏛️", gradient: "from-gray-500 to-slate-500" }
  ];

  return (
    <div className="min-h-screen px-4 py-8 md:px-8 lg:px-12 xl:px-16">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto mb-12 animate-slide-in">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 glass-card px-6 py-3 mb-6">
            <Sparkles className="w-5 h-5 text-primary-light animate-pulse" />
            <span className="text-secondary font-medium">AI-Powered Translation</span>
          </div>
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-4 text-gradient">
            Natural Language to FIBO
          </h1>
          <p className="text-xl text-secondary max-w-3xl mx-auto">
            Describe your vision in plain English. Our AI translates it into optimized parameters with intelligent reasoning.
          </p>
        </div>

        {/* Main Input Section */}
        <div className="glass-card p-6 md:p-8 lg:p-10 mb-8">
          <form onSubmit={handleTranslate} className="space-y-6">
            <div>
              <label className="flex items-center gap-2 text-primary font-semibold mb-3 text-lg">
                <Wand2 className="w-5 h-5" />
                Describe Your Vision
              </label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="textarea-modern"
                placeholder="e.g., 'Dramatic luxury watch on marble surface with moody lighting and cinematic composition...'"
                rows="5"
                required
              />
            </div>

            <button
              type="submit"
              disabled={translateMutation.isLoading}
              className="btn-modern w-full md:w-auto px-12 flex items-center justify-center gap-3 mx-auto"
            >
              {translateMutation.isLoading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Translating...
                </>
              ) : (
                <>
                  <Zap className="w-5 h-5" />
                  Translate to Parameters
                  <ArrowRight className="w-5 h-5" />
                </>
              )}
            </button>
          </form>
        </div>

        {/* Example Prompts */}
        <div className="mb-12">
          <div className="flex items-center gap-2 mb-6">
            <Lightbulb className="w-5 h-5 text-warning" />
            <h3 className="text-xl font-semibold text-primary">Try These Examples</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {examples.map((example, idx) => (
              <button
                key={idx}
                onClick={() => setPrompt(example.text)}
                className="glass-card p-5 text-left hover:scale-105 transition-all duration-300 group"
                style={{ animationDelay: `${idx * 100}ms` }}
              >
                <div className={`text-4xl mb-3 group-hover:scale-110 transition-transform`}>
                  {example.icon}
                </div>
                <p className="text-secondary text-sm leading-relaxed group-hover:text-primary transition-colors">
                  {example.text}
                </p>
              </button>
            ))}
          </div>
        </div>

        {/* Results Section */}
        {result && (
          <div className="glass-card p-6 md:p-8 lg:p-10 animate-fade-in">
            <div className="flex items-center justify-between mb-6 flex-wrap gap-4">
              <h3 className="text-2xl font-bold text-primary flex items-center gap-3">
                <Sparkles className="w-6 h-6 text-accent" />
                Translation Results
              </h3>
              <div className="flex gap-3">
                <button
                  onClick={handleUseParameters}
                  className="btn-modern px-6 py-3 flex items-center gap-2 bg-gradient-to-r from-accent to-emerald-500"
                >
                  <Download className="w-4 h-4" />
                  Use Parameters
                </button>
                <button
                  onClick={() => navigator.clipboard.writeText(JSON.stringify(result.parameters, null, 2))}
                  className="glass-card px-6 py-3 hover:bg-hover flex items-center gap-2 font-semibold"
                >
                  <Copy className="w-4 h-4" />
                  Copy JSON
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
              {/* Intent & Mood */}
              <div className="space-y-4">
                <div className="glass-card p-5 bg-gradient-to-br from-primary/10 to-secondary/10">
                  <div className="text-sm font-semibold text-tertiary mb-2">Detected Intent</div>
                  <div className="text-xl font-bold text-primary">{result.intent}</div>
                </div>
                <div className="glass-card p-5 bg-gradient-to-br from-secondary/10 to-accent/10">
                  <div className="text-sm font-semibold text-tertiary mb-2">Overall Mood</div>
                  <div className="text-xl font-bold text-primary">{result.mood}</div>
                </div>
              </div>

              {/* Parameters */}
              <div className="glass-card p-5">
                <div className="text-sm font-semibold text-tertiary mb-4">Generated Parameters</div>
                <div className="space-y-3">
                  {Object.entries(result.parameters || {}).map(([key, value]) => (
                    <div key={key} className="flex justify-between items-center p-3 rounded-lg bg-bg-hover">
                      <span className="text-secondary capitalize">{key.replace(/_/g, ' ')}</span>
                      <span className="badge-modern">{value}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* AI Reasoning */}
            {result.reasoning && (
              <div className="glass-card p-6 mb-6 border-l-4 border-accent">
                <h4 className="font-bold text-primary mb-3 flex items-center gap-2">
                  <span className="text-2xl">🧠</span>
                  AI Reasoning
                </h4>
                <div className="space-y-3">
                  {Object.entries(result.reasoning).map(([key, value]) => (
                    <div key={key} className="p-4 rounded-lg bg-bg-hover">
                      <div className="font-semibold text-primary-light capitalize mb-1">
                        {key.replace(/_/g, ' ')}
                      </div>
                      <div className="text-secondary text-sm">{value}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Suggestions */}
            {result.suggestions && result.suggestions.length > 0 && (
              <div className="glass-card p-6 border-l-4 border-warning">
                <h4 className="font-bold text-primary mb-4 flex items-center gap-2">
                  <Lightbulb className="w-5 h-5 text-warning" />
                  AI Suggestions
                </h4>
                <ul className="space-y-2">
                  {result.suggestions.map((suggestion, idx) => (
                    <li key={idx} className="flex items-start gap-3 text-secondary p-3 rounded-lg bg-bg-hover">
                      <span className="text-accent font-bold">→</span>
                      <span>{suggestion}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Confidence Score */}
            {result.confidence && (
              <div className="mt-6 p-5 glass-card bg-gradient-to-r from-success/10 to-accent/10">
                <div className="flex items-center justify-between">
                  <span className="text-secondary font-medium">Confidence Score</span>
                  <span className="text-2xl font-bold text-success">{(result.confidence * 100).toFixed(0)}%</span>
                </div>
                <div className="mt-3 h-2 bg-bg-card rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-gradient-to-r from-success to-accent transition-all duration-1000"
                    style={{ width: `${result.confidence * 100}%` }}
                  />
                </div>
              </div>
            )}

            {/* Fallback Warning */}
            {result.is_fallback && (
              <div className="mt-6 p-5 glass-card bg-gradient-to-r from-warning/10 to-orange-500/10 border-l-4 border-warning">
                <div className="flex items-start gap-3">
                  <div className="text-2xl">⚡</div>
                  <div>
                    <div className="font-semibold text-primary mb-1">Smart parameter optimization applied. Ready to generate!</div>
                    <div className="text-secondary text-sm">Using intelligent defaults based on your prompt keywords.</div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default AITranslator;
