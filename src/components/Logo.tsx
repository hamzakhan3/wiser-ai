
import React from 'react';

export const Logo = () => {
  return (
    <div className="flex items-center gap-2">
      <div className="text-2xl text-sage-500 font-light">
        <span>(</span>
        <span className="text-sage-400">*</span>
        <span>)</span>
      </div>
      <span className="text-sage-500 font-medium text-lg">sage</span>
    </div>
  );
};
