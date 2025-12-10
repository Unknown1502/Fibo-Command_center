import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navigation = () => {
  const location = useLocation();
  
  const navigation = [
    { name: 'Dashboard', href: '/', current: location.pathname === '/' },
    { name: 'Generate', href: '/generate', current: location.pathname === '/generate' },
    { name: 'AI Translator', href: '/ai-translator', current: location.pathname === '/ai-translator' },
    { name: 'Visual Editor', href: '/visual-editor', current: location.pathname === '/visual-editor' },
    { name: 'Analytics', href: '/analytics', current: location.pathname === '/analytics' },
    { name: 'Brand Guidelines', href: '/brand-guidelines', current: location.pathname === '/brand-guidelines' },
    { name: 'ControlNet', href: '/controlnet', current: location.pathname === '/controlnet' },
    { name: 'Workflows', href: '/workflows', current: location.pathname === '/workflows' },
    { name: 'Projects', href: '/projects', current: location.pathname === '/projects' },
  ];
  
  return (
    <nav className="bg-gray-900/95 backdrop-blur-lg border-b border-white/10 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center space-x-8">
            <div className="flex-shrink-0">
              <h1 className="text-xl font-bold bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
                FIBO Command Center
              </h1>
            </div>
            <div className="hidden lg:flex lg:space-x-1">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`${
                    item.current
                      ? 'bg-white/10 text-white'
                      : 'text-gray-300 hover:bg-white/5 hover:text-white'
                  } px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200`}
                >
                  {item.name}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
