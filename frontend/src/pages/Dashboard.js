import React from 'react';

const Dashboard = () => {
  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="bg-white shadow sm:rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Welcome to FIBO Command Center</h2>
          <p className="text-gray-600 mb-6">
            The Professional AI Visual Production Suite with Agentic Intelligence
          </p>
          
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            <div className="bg-indigo-50 overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <svg className="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Quick Generate</dt>
                      <dd className="text-lg font-medium text-gray-900">AI-Powered</dd>
                    </dl>
                  </div>
                </div>
                <div className="mt-4">
                  <a href="/generate" className="text-sm font-medium text-indigo-600 hover:text-indigo-500">
                    Start generating
                  </a>
                </div>
              </div>
            </div>
            
            <div className="bg-green-50 overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <svg className="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Workflows</dt>
                      <dd className="text-lg font-medium text-gray-900">Automated</dd>
                    </dl>
                  </div>
                </div>
                <div className="mt-4">
                  <a href="/workflows" className="text-sm font-medium text-green-600 hover:text-green-500">
                    Run workflow
                  </a>
                </div>
              </div>
            </div>
            
            <div className="bg-purple-50 overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <svg className="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                    </svg>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Projects</dt>
                      <dd className="text-lg font-medium text-gray-900">Organized</dd>
                    </dl>
                  </div>
                </div>
                <div className="mt-4">
                  <a href="/projects" className="text-sm font-medium text-purple-600 hover:text-purple-500">
                    Manage projects
                  </a>
                </div>
              </div>
            </div>
          </div>
          
          <div className="mt-8">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Key Features</h3>
            <ul className="space-y-3">
              <li className="flex items-start">
                <span className="flex-shrink-0 h-5 w-5 text-green-500">✓</span>
                <span className="ml-3 text-gray-700">AI Agent Intelligence - Natural language to optimal parameters</span>
              </li>
              <li className="flex items-start">
                <span className="flex-shrink-0 h-5 w-5 text-green-500">✓</span>
                <span className="ml-3 text-gray-700">Professional Controls - HDR, 16-bit color depth, full parameter access</span>
              </li>
              <li className="flex items-start">
                <span className="flex-shrink-0 h-5 w-5 text-green-500">✓</span>
                <span className="ml-3 text-gray-700">Automated Workflows - E-commerce, social media, game assets</span>
              </li>
              <li className="flex items-start">
                <span className="flex-shrink-0 h-5 w-5 text-green-500">✓</span>
                <span className="ml-3 text-gray-700">Enterprise Features - Brand management, batch processing, integrations</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
