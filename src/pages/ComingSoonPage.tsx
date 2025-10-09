import React from 'react';

const ComingSoonPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#437874] flex items-center justify-center">
      <div className="text-center">
        <div className="mb-8">
          <div className="w-24 h-24 mx-auto bg-white/20 rounded-full flex items-center justify-center mb-6">
            <div className="w-16 h-16 bg-white/30 rounded-full flex items-center justify-center">
              <div className="w-8 h-8 bg-white rounded-full"></div>
            </div>
          </div>
        </div>
        
        <h1 className="text-4xl font-bold text-white mb-4" style={{ fontFamily: 'Inter, sans-serif' }}>
          Coming Soon
        </h1>
        
        <p className="text-xl text-white/80 mb-8 max-w-md mx-auto" style={{ fontFamily: 'Inter, sans-serif' }}>
          This feature is currently under development. We're working hard to bring you something amazing!
        </p>
        
        <div className="flex justify-center space-x-4">
          <button 
            onClick={() => window.history.back()}
            className="px-6 py-3 bg-white/20 hover:bg-white/30 text-white rounded-lg transition-colors duration-200 font-medium"
            style={{ fontFamily: 'Inter, sans-serif' }}
          >
            Go Back
          </button>
          <button 
            onClick={() => window.location.href = '/wisdom'}
            className="px-6 py-3 bg-white hover:bg-white/90 text-[#437874] rounded-lg transition-colors duration-200 font-medium"
            style={{ fontFamily: 'Inter, sans-serif' }}
          >
            Return to Wisdom
          </button>
        </div>
      </div>
    </div>
  );
};

export default ComingSoonPage;
