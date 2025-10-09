import React from 'react';
import { Button } from './ui/button';

const WisdomTopBar: React.FC = () => {
  return (
    <div 
      className="bg-[#437874] flex flex-row items-center relative w-full"
      style={{
        height: '19.81333351135254px',
        paddingLeft: '0px',
        paddingRight: '0px',
        marginLeft: '0px',
        marginRight: '0px',
        opacity: 1
      }}
    >
      {/* Left Section - Empty for balance */}
      <div 
        className="flex flex-row items-center"
        style={{
          padding: '0px 6.1px',
          gap: '9.14px',
          width: '156.22px',
          minHeight: '24px'
        }}
      >
      </div>

      {/* Center Section - Sage Text */}
      <div 
        className="flex flex-row justify-center items-center flex-1"
        style={{
          padding: '8px 16px',
          gap: '4.57px',
          minHeight: '24px',
          mixBlendMode: 'normal',
          borderRadius: '9.14462px'
        }}
      >
        {/* Sage Text */}
        <span 
          className="text-white"
          style={{
            fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
            fontSize: '14px',
            fontWeight: 500,
            letterSpacing: '0.01em',
            textTransform: 'lowercase',
            lineHeight: '1.2',
            color: '#FFFFFF',
            textAlign: 'center'
          }}
        >
          sage
        </span>
      </div>

      {/* Right Section - Empty for balance */}
      <div 
        className="flex flex-row items-center"
        style={{
          padding: '0px 6.1px',
          gap: '9.14px',
          width: '156.22px',
          minHeight: '24px'
        }}
      >
      </div>
    </div>
  );
};

export default WisdomTopBar;
