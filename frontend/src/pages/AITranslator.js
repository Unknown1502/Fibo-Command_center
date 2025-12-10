import React, { useState } from 'react';
import { useMutation } from 'react-query';
import { aiAPI } from '../services/api';

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
      // Store parameters in localStorage for use in Generate page
      localStorage.setItem('fibo_translated_params', JSON.stringify(result.parameters));
      alert('Parameters saved! Go to Generate page to use them.');
    }
  };

  const examples = [
    "Dramatic luxury watch commercial with cinematic lighting",
    "Bright cheerful summer beach collection for Instagram",
    "Professional clean product photography for e-commerce",
    "Epic fantasy game character art with heroic pose",
    "Minimalist modern architecture for magazine editorial"
  ];

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="bg-white shadow sm:rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <div className="mb-2">
            <h2 className="text-2xl font-bold text-gray-900">AI Prompt Translator</h2>
          </div>
          <p className="text-sm text-gray-500 mb-6">
            Describe what you want in natural language. Our AI will convert it to optimized FIBO parameters with detailed reasoning.
          </p>

          <form onSubmit={handleTranslate} className="space-y-6">
            <div>
              <label htmlFor="prompt" className="block text-sm font-medium text-gray-700 mb-2">
                Describe Your Image
              </label>
              <textarea
                id="prompt"
                rows={4}
                className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="E.g., 'I need dramatic product photos of a watch that look expensive and cinematic, like a luxury brand commercial'"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                required
              />
              <p className="mt-2 text-sm text-gray-500">
                Be specific about mood, style, and purpose. The more detail, the better the translation.
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Quick Examples (click to use)
              </label>
              <div className="flex flex-wrap gap-2">
                {examples.map((example, idx) => (
                  <button
                    key={idx}
                    type="button"
                    onClick={() => setPrompt(example)}
                    className="inline-flex items-center px-3 py-1.5 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    {example.slice(0, 30)}...
                  </button>
                ))}
              </div>
            </div>

            <div>
              <button
                type="submit"
                disabled={translateMutation.isLoading}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {translateMutation.isLoading ? 'Translating...' : 'Translate to FIBO'}
              </button>
            </div>
          </form>

          {result && (
            <div className="mt-8 space-y-6">
              <div className="border-t border-gray-200 pt-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">AI Analysis</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <p className="text-sm font-medium text-blue-900">Intent</p>
                    <p className="mt-1 text-sm text-blue-700">{result.intent}</p>
                  </div>
                  <div className="bg-purple-50 p-4 rounded-lg">
                    <p className="text-sm font-medium text-purple-900">Mood</p>
                    <p className="mt-1 text-sm text-purple-700">{result.mood}</p>
                  </div>
                </div>

                <div className="bg-gray-50 p-4 rounded-lg mb-6">
                  <div className="flex justify-between items-center mb-3">
                    <p className="text-sm font-medium text-gray-900">FIBO Parameters (JSON)</p>
                    <div className="flex gap-2">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        Confidence: {(result.confidence * 100).toFixed(0)}%
                      </span>
                      <button
                        onClick={handleUseParameters}
                        className="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
                      >
                        Use These Parameters
                      </button>
                    </div>
                  </div>
                  <pre className="text-xs bg-white p-3 rounded border border-gray-200 overflow-x-auto">
                    {JSON.stringify(result.parameters, null, 2)}
                  </pre>
                </div>

                <div className="mb-6">
                  <p className="text-sm font-medium text-gray-900 mb-3">Reasoning</p>
                  <div className="space-y-2">
                    {Object.entries(result.reasoning || {}).map(([param, reason]) => (
                      <div key={param} className="flex">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-medium bg-indigo-100 text-indigo-800 mr-2">
                          {param.replace('_', ' ')}
                        </span>
                        <span className="text-sm text-gray-600">{reason}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {result.suggestions && result.suggestions.length > 0 && (
                  <div>
                    <p className="text-sm font-medium text-gray-900 mb-2">Alternative Suggestions</p>
                    <ul className="list-disc list-inside space-y-1">
                      {result.suggestions.map((suggestion, idx) => (
                        <li key={idx} className="text-sm text-gray-600">{suggestion}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {result.fallback && (
                  <div className="mt-4 bg-yellow-50 border-l-4 border-yellow-400 p-4">
                    <div className="flex">
                      <div className="flex-shrink-0">
                        <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <div className="ml-3">
                        <p className="text-sm text-yellow-700">
                          Smart parameter optimization applied. Ready to generate!
                        </p>
                      </div>
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

export default AITranslator;
