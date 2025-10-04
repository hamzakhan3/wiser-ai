
import React from 'react';

export const Footer = () => {
  return (
    <footer className="text-xs text-gray-500 py-4 text-center">
      <div className="flex justify-center gap-4 mb-1">
        <a href="#" className="hover:text-sage-600 hover:underline">Privacy Policy</a>
        <span>•</span>
        <a href="#" className="hover:text-sage-600 hover:underline">User Agreement</a>
      </div>
      <p>A Product of Wiser Machines Inc.</p>
    </footer>
  );
};
