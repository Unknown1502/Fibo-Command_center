export const handleAPIError = (error) => {
  if (error.response) {
    const status = error.response.status;
    const detail = error.response.data?.detail;
    
    if (status === 400) {
      return {
        title: 'Bad Request',
        message: detail || 'Invalid request parameters',
        code: status,
      };
    }
    
    if (status === 401) {
      return {
        title: 'Unauthorized',
        message: 'Please log in to continue',
        code: status,
      };
    }
    
    if (status === 403) {
      return {
        title: 'Forbidden',
        message: 'You do not have permission to perform this action',
        code: status,
      };
    }
    
    if (status === 404) {
      return {
        title: 'Not Found',
        message: detail || 'The requested resource was not found',
        code: status,
      };
    }
    
    if (status === 429) {
      return {
        title: 'Rate Limit Exceeded',
        message: 'Too many requests. Please try again later',
        code: status,
      };
    }
    
    if (status >= 500) {
      return {
        title: 'Server Error',
        message: 'An error occurred on the server. Please try again later',
        code: status,
      };
    }
    
    return {
      title: 'Error',
      message: detail || 'An unexpected error occurred',
      code: status,
    };
  }
  
  if (error.request) {
    return {
      title: 'Network Error',
      message: 'Unable to connect to the server. Please check your internet connection',
      code: null,
    };
  }
  
  return {
    title: 'Error',
    message: error.message || 'An unexpected error occurred',
    code: null,
  };
};

export const formatErrorMessage = (error) => {
  const errorData = handleAPIError(error);
  return `${errorData.title}: ${errorData.message}`;
};
