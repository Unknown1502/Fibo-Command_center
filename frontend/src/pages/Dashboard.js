import React from 'react';
import { Sparkles, Zap, Layers, Image, TrendingUp, Shield, Cpu, Rocket } from 'lucide-react';
import ExampleGallery from '../components/ExampleGallery';
import QualityShowcase from '../components/QualityShowcase';

const Dashboard = () => {
  const features = [
    {
      icon: <Sparkles className="w-6 h-6" />,
      title: "AI Agent Intelligence",
      description: "Natural language to optimal parameters",
      color: "from-indigo-500 to-purple-500",
      link: "/ai-translator"
    },
    {
      icon: <Image className="w-6 h-6" />,
      title: "HDR & 16-bit Export",
      description: "Professional color depth control",
      color: "from-green-500 to-emerald-500",
      link: "/generate"
    },
    {
      icon: <Layers className="w-6 h-6" />,
      title: "Visual Parameter Editor",
      description: "Interactive studio controls",
      color: "from-blue-500 to-cyan-500",
      link: "/visual-editor"
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      title: "Analytics Dashboard",
      description: "A/B testing & optimization",
      color: "from-orange-500 to-red-500",
      link: "/analytics"
    },
    {
      icon: <Shield className="w-6 h-6" />,
      title: "Brand Guidelines",
      description: "Automated compliance validation",
      color: "from-pink-500 to-rose-500",
      link: "/brand-guidelines"
    },
    {
      icon: <Cpu className="w-6 h-6" />,
      title: "ControlNet Studio",
      description: "Advanced image control",
      color: "from-violet-500 to-purple-500",
      link: "/controlnet"
    }
  ];

  return (
    <div className="max-w-7xl mx-auto p-6">
      {/* Hero Section */}
      <div className="text-center mb-12 animate-fade-in">
        <div className="inline-flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 rounded-full mb-4">
          <Rocket className="w-4 h-4 text-indigo-400" />
          <span className="text-sm font-medium text-white">FIBO Hackathon 2025</span>
        </div>
        <h1 className="text-6xl font-bold mb-4">
          <span className="text-gradient">FIBO Command Center</span>
        </h1>
        <p className="text-xl text-gray-300 mb-6">
          Professional AI Visual Production Suite with Agentic Intelligence
        </p>
        <div className="flex items-center justify-center space-x-4">
          <a 
            href="/generate" 
            className="btn-modern bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 px-8 py-4 text-lg"
          >
            <Zap className="w-5 h-5 mr-2 inline" />
            Start Generating
          </a>
          <a 
            href="/ai-translator" 
            className="btn-modern bg-white/10 hover:bg-white/20 px-8 py-4 text-lg border border-white/20"
          >
            <Sparkles className="w-5 h-5 mr-2 inline" />
            Try AI Translator
          </a>
        </div>
      </div>

      {/* Feature Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        {features.map((feature, index) => (
          <a
            key={index}
            href={feature.link}
            className="glass-card p-6 hover-glow animate-slide-in group"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${feature.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
              {feature.icon}
            </div>
            <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
            <p className="text-gray-400 text-sm">{feature.description}</p>
            <div className="mt-4 text-indigo-400 text-sm font-medium group-hover:translate-x-2 transition-transform duration-300">
              Explore →
            </div>
          </a>
        ))}
      </div>

      {/* Stats Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <div className="glass-card p-6 text-center animate-slide-in">
          <div className="text-5xl font-bold text-gradient mb-2">6</div>
          <div className="text-gray-400">Powerful Features</div>
        </div>
        <div className="glass-card p-6 text-center animate-slide-in" style={{ animationDelay: '100ms' }}>
          <div className="text-5xl font-bold text-gradient mb-2">16-bit</div>
          <div className="text-gray-400">Color Depth</div>
        </div>
        <div className="glass-card p-6 text-center animate-slide-in" style={{ animationDelay: '200ms' }}>
          <div className="text-5xl font-bold text-gradient mb-2">AI</div>
          <div className="text-gray-400">Powered Intelligence</div>
        </div>
      </div>

      {/* Example Gallery Section */}
      <div className="mb-12">
        <div className="text-center mb-8">
          <h2 className="text-4xl font-bold text-gradient mb-3">
            Real BRIA API Output Examples
          </h2>
          <p className="text-xl text-secondary max-w-3xl mx-auto">
            30 professionally generated images across e-commerce, social media, and gaming categories.
            All images generated using actual BRIA FIBO API with verified quality metrics.
          </p>
        </div>
        <ExampleGallery />
      </div>

      {/* Quality Showcase Section */}
      <div className="mb-12">
        <QualityShowcase />
      </div>

      {/* Key Highlights */}
      <div className="glass-card p-8 animate-fade-in">
        <h2 className="text-3xl font-bold text-white mb-6">Why FIBO Command Center?</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-green-500/20 flex items-center justify-center text-green-400">
              ✓
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white mb-1">AI Agent Intelligence</h3>
              <p className="text-gray-400 text-sm">Natural language to optimal parameters with GPT-4, Groq, and Gemini support</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-green-500/20 flex items-center justify-center text-green-400">
              ✓
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white mb-1">Professional Controls</h3>
              <p className="text-gray-400 text-sm">HDR, 16-bit color depth, 4 tone mapping algorithms, full parameter access</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-green-500/20 flex items-center justify-center text-green-400">
              ✓
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white mb-1">Automated Workflows</h3>
              <p className="text-gray-400 text-sm">E-commerce, social media, game assets with batch processing</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-green-500/20 flex items-center justify-center text-green-400">
              ✓
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white mb-1">Enterprise Features</h3>
              <p className="text-gray-400 text-sm">Brand management, A/B testing, analytics, ControlNet integration</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
