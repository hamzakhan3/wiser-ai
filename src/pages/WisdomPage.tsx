import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { Send, Lightbulb } from 'lucide-react';
import WisdomSidebar from '@/components/WisdomSidebar';
import WisdomTopBar from '@/components/WisdomTopBar';
import ChatInputBar from '@/components/ChatInputBar';

const WisdomPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');

  const handleSendMessage = (message: string) => {
    console.log('Sending message:', message);
    // TODO: Implement message sending logic
  };

  const suggestedQueries = [
    "Reduce Downtime for meeting high demand",
    "How to handle breakdown during production", 
    "Management Tips for a gen-z workforce",
    "How do I tackle upcoming maintenance tasks",
    "How Do I reduce My Power Consumption",
    "Leading with stoicism"
  ];

  const handleQueryClick = (query: string) => {
    setSearchQuery(query);
    // Navigate to chat page with the query
    window.location.href = `/chat?q=${encodeURIComponent(query)}`;
  };

  const handleSearch = (message?: string) => {
    const query = message || searchQuery;
    if (query.trim()) {
      // Navigate to chat page with the query
      window.location.href = `/chat?q=${encodeURIComponent(query)}`;
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div 
      className="flex flex-row items-center bg-white w-full h-screen"
      style={{
        gap: '0px',
        opacity: 1
      }}
    >
      {/* Sidebar */}
      <WisdomSidebar />

      {/* Main Content Area */}
      <div 
        className="flex flex-col items-center justify-center flex-1 bg-white"
        style={{
          padding: '0px',
          gap: '40px',
          height: '100vh',
          borderRadius: '0px'
        }}
      >
        {/* Top Bar */}
        <WisdomTopBar />

        {/* Screen Content */}
        <div 
          className="flex flex-col items-center justify-center w-full"
          style={{
            padding: '0px',
            gap: '40px',
            height: '100%',
            borderRadius: '0px'
          }}
        >
          {/* Hero Section */}
          <div 
            className="flex flex-col items-center justify-center"
            style={{
              padding: '0px',
              gap: '16px',
              height: 'auto',
              borderRadius: '0px'
            }}
          >
            {/* Frame 13884 - Icon */}
            <div 
              className="flex flex-row justify-center items-center"
              style={{
                padding: '0px',
                gap: '0px',
                width: 'auto',
                height: 'auto',
                borderRadius: '0px'
              }}
            >
              <span 
                style={{
                  fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                  fontSize: '24px',
                  fontWeight: 400,
                  color: '#437874',
                  letterSpacing: '0em'
                }}
              >
                (
              </span>
              <span 
                style={{
                  fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                  fontSize: '24px',
                  fontWeight: 400,
                  color: '#437874',
                  marginLeft: '-0.05em',
                  marginRight: '-0.05em'
                }}
              >
                *
              </span>
              <span 
                style={{
                  fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                  fontSize: '24px',
                  fontWeight: 400,
                  color: '#437874',
                  letterSpacing: '0em'
                }}
              >
                )
              </span>
            </div>

            {/* Title */}
            <h2 
              style={{
                fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                fontWeight: 500,
                fontSize: '28px',
                lineHeight: '1.2',
                letterSpacing: '-0.02em',
                color: '#2d3748',
                textTransform: 'none',
                textAlign: 'center'
              }}
            >
              Discover Infinite Wisdom
            </h2>
          </div>

          {/* Suggested Queries */}
          <div className="w-full max-w-4xl">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {suggestedQueries.map((query, index) => (
                <button
                  key={index}
                  onClick={() => handleQueryClick(query)}
                  className="flex items-center justify-center bg-[#EDF2F2] rounded-lg p-4 hover:bg-[#E0E8E8] transition-colors duration-200"
                  style={{
                    minHeight: '60px',
                    borderRadius: '8px'
                  }}
                >
                  <span 
                    className="text-center font-medium"
                    style={{
                      fontFamily: 'Space Grotesk, Inter, sans-serif',
                      fontSize: '14px',
                      lineHeight: '1.4',
                      color: '#36635F',
                      textTransform: 'none'
                    }}
                  >
                    {query}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Chat Input Bar */}
          <div className="w-full max-w-2xl">
            <ChatInputBar 
              onSendMessage={handleSearch}
              placeholder="Ask away !"
            />
          </div>
        </div>

        {/* Frame 19 - Footer */}
        <div 
          className="flex flex-col items-start w-full max-w-md"
          style={{
            padding: '0px',
            gap: '18.42px'
          }}
        >
          {/* Frame 18 */}
          <div 
            className="flex flex-row justify-center items-center w-full"
            style={{
              padding: '0px',
              gap: '10.23px',
              height: '8px'
            }}
          >
            <a 
              href="#" 
              style={{
                width: '93px',
                height: '8px',
                fontFamily: 'Space Grotesk, sans-serif',
                fontStyle: 'normal',
                fontWeight: 400,
                fontSize: '12px',
                lineHeight: '15px',
                color: '#444444'
              }}
            >
              Privacy Policy
            </a>
            <span 
              style={{
                width: '16.3694px',
                height: '8px',
                fontFamily: 'Space Grotesk, sans-serif',
                fontStyle: 'normal',
                fontWeight: 400,
                fontSize: '16.3694px',
                lineHeight: '21px',
                color: '#444444'
              }}
            >
              .
            </span>
            <a 
              href="#" 
              style={{
                width: '93px',
                height: '8px',
                fontFamily: 'Space Grotesk, sans-serif',
                fontStyle: 'normal',
                fontWeight: 400,
                fontSize: '12px',
                lineHeight: '15px',
                color: '#444444'
              }}
            >
              User Agreement
            </a>
          </div>

          {/* Frame 17 */}
          <div 
            className="flex flex-row justify-center items-center w-full"
            style={{
              padding: '0px',
              gap: '10.23px',
              height: '8px'
            }}
          >
            <p 
              style={{
                width: '191px',
                height: '8px',
                fontFamily: 'Space Grotesk, sans-serif',
                fontStyle: 'normal',
                fontWeight: 700,
                fontSize: '12px',
                lineHeight: '15px',
                color: '#444444'
              }}
            >
              A Product of Wiser Machines Inc.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WisdomPage;
