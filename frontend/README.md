# FIBO Command Center - Frontend

Professional React frontend for the FIBO Command Center image generation platform.

## Architecture

### Components
- `Navigation.js`: Main navigation bar with routing
- `ErrorBoundary.js`: Global error handling component
- `LoadingSpinner.js`: Reusable loading indicator
- `ImageGallery.js`: Grid-based image display component

### Pages
- `Dashboard.js`: Landing page with feature overview
- `Generator.js`: Image generation interface with AI and manual modes
- `Workflows.js`: Automated workflow execution interface
- `Projects.js`: Project management interface

### Services
- `api.js`: Centralized API communication layer with axios

### Utils
- `validation.js`: Form validation helpers
- `errorHandler.js`: API error handling utilities

## Key Features

### Secure API Integration
- Axios interceptors for request/response handling
- Automatic token management
- 401 redirect to login
- Request/response logging in development

### Professional UI/UX
- Tailwind CSS for responsive design
- Clean, professional interface without emojis
- Loading states and error handling
- Form validation

### React Query Integration
- Efficient data fetching and caching
- Automatic refetching on stale data
- Mutation handling with optimistic updates
- Query invalidation for data consistency

## Development

### Install Dependencies
```bash
cd frontend
npm install
```

### Start Development Server
```bash
npm start
```

### Build for Production
```bash
npm run build
```

## Environment Variables

Create `.env` file:
```
REACT_APP_API_URL=http://localhost:8000
```

## Technology Stack

- React 18.2.0
- React Router 6.20.1
- React Query 3.39.3
- Axios 1.6.2
- Tailwind CSS 3.3.6
- Framer Motion 10.16.16 (animations)
