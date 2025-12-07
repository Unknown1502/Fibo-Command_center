import React from 'react';

const ImageGallery = ({ images = [], onImageClick = null }) => {
  if (!images || images.length === 0) {
    return (
      <div className="text-center py-12 bg-gray-50 rounded-lg">
        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <p className="mt-2 text-sm text-gray-500">No images to display</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {images.map((image, index) => (
        <div
          key={image.id || index}
          className="bg-white border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow"
        >
          <div
            className={`aspect-w-16 aspect-h-9 ${onImageClick ? 'cursor-pointer' : ''}`}
            onClick={() => onImageClick && onImageClick(image)}
          >
            <img
              src={image.image_url || image.url}
              alt={image.prompt || image.description || `Image ${index + 1}`}
              className="w-full h-48 object-cover"
            />
          </div>
          <div className="p-4">
            {image.prompt && (
              <p className="text-sm text-gray-700 line-clamp-2 mb-2">{image.prompt}</p>
            )}
            <div className="flex items-center justify-between text-xs text-gray-500">
              {image.quality_score !== undefined && (
                <span className="inline-flex items-center px-2 py-1 rounded-full bg-green-100 text-green-800">
                  Quality: {image.quality_score.toFixed(2)}
                </span>
              )}
              {image.generation_time && (
                <span>{image.generation_time.toFixed(2)}s</span>
              )}
              {image.created_at && (
                <span>{new Date(image.created_at).toLocaleDateString()}</span>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ImageGallery;
