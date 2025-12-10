import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { projectsAPI } from '../services/api';
import { FolderPlus, Folder, Trash2, Calendar, Package } from 'lucide-react';

const Projects = () => {
  const [isCreating, setIsCreating] = useState(false);
  const [newProject, setNewProject] = useState({
    name: '',
    description: '',
    project_type: 'ecommerce',
  });
  
  const queryClient = useQueryClient();
  
  const { data: projects, isLoading } = useQuery('projects', () =>
    projectsAPI.list({ user_id: 1, limit: 20 })
  );
  
  const createMutation = useMutation(projectsAPI.create, {
    onSuccess: () => {
      queryClient.invalidateQueries('projects');
      setIsCreating(false);
      setNewProject({ name: '', description: '', project_type: 'ecommerce' });
    },
    onError: (error) => {
      alert('Failed to create project: ' + (error.response?.data?.detail || error.message));
    },
  });
  
  const deleteMutation = useMutation(projectsAPI.delete, {
    onSuccess: () => {
      queryClient.invalidateQueries('projects');
    },
  });
  
  const handleCreate = (e) => {
    e.preventDefault();
    createMutation.mutate({
      ...newProject,
      user_id: 1,
    });
  };
  
  return (
    <div className="max-w-7xl mx-auto p-6">
      {/* Header */}
      <div className="mb-8 animate-fade-in">
        <div className="flex items-center justify-between">
          <div>
            <div className="inline-flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 rounded-full mb-4">
              <Folder className="w-4 h-4 text-indigo-400" />
              <span className="text-sm font-medium text-white">Organization</span>
            </div>
            <h1 className="text-5xl font-bold text-white mb-3">
              <span className="text-gradient">Projects</span>
            </h1>
            <p className="text-xl text-gray-300">
              Organize generations, track campaigns, and manage brand guidelines
            </p>
          </div>
          <button
            onClick={() => setIsCreating(!isCreating)}
            className="btn-modern bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 flex items-center space-x-2"
          >
            <FolderPlus className="w-5 h-5" />
            <span>New Project</span>
          </button>
        </div>
      </div>

      {/* Create Project Form */}
      {isCreating && (
        <div className="glass-card p-8 mb-8 animate-slide-in">
          <h3 className="text-2xl font-bold text-white mb-6">Create New Project</h3>
          <form onSubmit={handleCreate} className="space-y-6">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-300 mb-2">
                Project Name <span className="text-red-400">*</span>
              </label>
              <input
                type="text"
                id="name"
                required
                className="input-modern w-full"
                value={newProject.name}
                onChange={(e) => setNewProject({ ...newProject, name: e.target.value })}
                placeholder="Enter project name..."
              />
            </div>
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-300 mb-2">
                Description
              </label>
              <textarea
                id="description"
                rows={3}
                className="textarea-modern w-full"
                value={newProject.description}
                onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
                placeholder="Describe your project..."
              />
            </div>
            <div>
              <label htmlFor="project_type" className="block text-sm font-medium text-gray-300 mb-2">
                Project Type
              </label>
              <select
                id="project_type"
                className="input-modern w-full"
                value={newProject.project_type}
                onChange={(e) => setNewProject({ ...newProject, project_type: e.target.value })}
              >
                <option value="ecommerce">E-commerce</option>
                    <option value="social">Social Media</option>
                    <option value="branding">Branding</option>
                    <option value="marketing">Marketing</option>
                  </select>
                </div>
                <div className="flex space-x-3">
                  <button
                    type="submit"
                    disabled={createMutation.isLoading}
                    className="btn-modern bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 flex items-center space-x-2"
                  >
                    <FolderPlus className="w-5 h-5" />
                    <span>{createMutation.isLoading ? 'Creating...' : 'Create Project'}</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setIsCreating(false)}
                    className="btn-modern bg-white/10 hover:bg-white/20 border border-white/20"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          )}
          
          {isLoading ? (
            <div className="glass-card p-12 text-center">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
              <p className="mt-4 text-sm text-gray-400">Loading projects...</p>
            </div>
          ) : projects && projects.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {projects.map((project) => (
                <div key={project.id} className="glass-card p-6 hover-glow group animate-slide-in">
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex items-start space-x-3">
                      <div className="w-10 h-10 rounded-lg bg-gradient-to-r from-indigo-500 to-purple-500 flex items-center justify-center flex-shrink-0">
                        <Package className="w-5 h-5 text-white" />
                      </div>
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-white">{project.name}</h3>
                      </div>
                    </div>
                    <button
                      onClick={() => {
                        if (window.confirm('Are you sure you want to delete this project?')) {
                          deleteMutation.mutate(project.id);
                        }
                      }}
                      className="text-red-400 hover:text-red-300 opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>
                  
                  {project.description && (
                    <p className="text-sm text-gray-400 mb-4 line-clamp-2">{project.description}</p>
                  )}
                  
                  <div className="flex items-center justify-between text-sm pt-3 border-t border-white/10">
                    <span className="badge-modern bg-indigo-500/20 text-indigo-400">
                      {project.project_type || 'General'}
                    </span>
                    <div className="flex items-center space-x-2 text-gray-400">
                      <Calendar className="w-4 h-4" />
                      <span>{new Date(project.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="glass-card p-12 text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-white/5 flex items-center justify-center">
                <Folder className="w-8 h-8 text-gray-400" />
              </div>
              <h3 className="text-lg font-medium text-white mb-2">No projects yet</h3>
              <p className="text-sm text-gray-400 mb-6">Get started by creating your first project.</p>
              <button
                onClick={() => setIsCreating(true)}
                className="btn-modern bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 inline-flex items-center space-x-2"
              >
                <FolderPlus className="w-5 h-5" />
                <span>Create Project</span>
              </button>
            </div>
          )}
    </div>
  );
};

export default Projects;
