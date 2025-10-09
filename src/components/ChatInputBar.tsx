import React, { useState } from 'react';
import { Mic, Send } from 'lucide-react';

interface ChatInputBarProps {
  onSendMessage: (message: string) => void;
  placeholder?: string;
}

const ChatInputBar: React.FC<ChatInputBarProps> = ({ 
  onSendMessage, 
  placeholder = "Ask away !" 
}) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="w-full">
      {/* Chat Input Bar */}
      <form onSubmit={handleSubmit} className="relative">
        <div className="flex items-center bg-gray-50 rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow duration-200">
          {/* Left Arrow Icon */}
          <div className="pl-3 pr-2">
            <Mic className="w-5 h-5 text-gray-400" />
          </div>
          
          {/* Text Input Area */}
          <div className="flex-1">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={placeholder}
              className="w-full py-3 px-2 bg-transparent border-none outline-none text-gray-700 placeholder:text-gray-400 text-sm"
              style={{ fontFamily: 'SF Pro Text, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' }}
            />
          </div>
          
          {/* Right Send Icon */}
          <div className="pr-3 pl-2">
            <button
              type="submit"
              disabled={!message.trim()}
              className="p-1 rounded-full hover:bg-gray-200 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-5 h-5 text-gray-400" />
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default ChatInputBar;
