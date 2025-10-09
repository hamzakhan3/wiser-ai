import React, { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { 
  Calendar, 
  Droplets, 
  PieChart, 
  Bell, 
  Bookmark, 
  Plus, 
  Download,
  Settings,
  Info
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const WisdomSidebar: React.FC = () => {
  const navigate = useNavigate();
  const [queryTitle, setQueryTitle] = useState('Query Title');

  const handleNavigation = (page: string) => {
    navigate(`/${page}`);
  };

  return (
    <div className="w-[163px] h-screen bg-[#437874] flex flex-col">
      {/* Top Section - Icon Buttons */}
      <div className="pt-1 pl-4 pr-1 flex justify-start">
        <div className="grid grid-cols-2 gap-1">
          {/* Parentheses with Asterisk Icon */}
          <Button 
            variant="ghost" 
            className="w-3 h-3 bg-white/10 hover:bg-white/15 rounded flex items-center justify-center p-0"
          >
            <div className="flex items-center text-white text-xs font-medium">
              <span className="text-[#437874] text-xs">(</span>
              <span className="text-[#437874] mx-0.5 text-xs">*</span>
              <span className="text-[#437874] text-xs">)</span>
            </div>
          </Button>
          
          {/* Overlapping Panels Icon */}
          <Button 
            variant="ghost" 
            className="w-3 h-3 bg-white/10 hover:bg-white/15 rounded flex items-center justify-center p-0"
          >
            <div className="relative w-1.5 h-1">
              {/* Left panel */}
              <div className="absolute left-0 top-0 w-0.5 h-1 border border-[#437874] rounded-sm"></div>
              {/* Right panel */}
              <div className="absolute right-0 top-0 w-0.5 h-1 border border-[#437874] rounded-sm"></div>
            </div>
          </Button>
        </div>
      </div>

      {/* Navigation Section */}
      <div className="px-1 space-y-0.5 mt-2">
        
        {/* Navigation Items - 2x2 Grid with Drop Shadows - Centered */}
        <div className="flex justify-center">
          <div className="grid grid-cols-2 gap-2">
          {/* Calendar Icon - Top Left */}
          <Button 
            variant="ghost" 
            onClick={() => handleNavigation('maintenance-schedule')}
            className="w-16 h-10 bg-white/10 hover:bg-white/15 rounded-lg flex items-center justify-center p-0 shadow-lg hover:shadow-xl transition-all duration-200"
            style={{
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)',
            }}
          >
            <Calendar className="w-6 h-6 text-white" />
          </Button>
          
          {/* Droplets/Sprinkler Icon - Top Right */}
          <Button 
            variant="ghost" 
            onClick={() => handleNavigation('droplets')}
            className="w-16 h-10 bg-white/10 hover:bg-white/15 rounded-lg flex items-center justify-center p-0 shadow-lg hover:shadow-xl transition-all duration-200"
            style={{
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)',
            }}
          >
            <Droplets className="w-6 h-6 text-white" />
          </Button>
          
          {/* Pie Chart Icon - Bottom Left */}
          <Button 
            variant="ghost" 
            onClick={() => handleNavigation('machine-health')}
            className="w-16 h-10 bg-white/10 hover:bg-white/15 rounded-lg flex items-center justify-center p-0 shadow-lg hover:shadow-xl transition-all duration-200"
            style={{
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)',
            }}
          >
            <PieChart className="w-6 h-6 text-white" />
          </Button>
          
          {/* Bell/Notification Icon - Bottom Right */}
          <Button 
            variant="ghost" 
            onClick={() => handleNavigation('notifications')}
            className="w-16 h-10 bg-white/10 hover:bg-white/15 rounded-lg flex items-center justify-center p-0 shadow-lg hover:shadow-xl transition-all duration-200"
            style={{
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)',
            }}
          >
            <Bell className="w-6 h-6 text-white" />
          </Button>
          </div>
        </div>
      </div>

      {/* Middle Section - Saved Queries */}
      <div className="flex-1 px-2 py-0.5 space-y-1 mt-3">
        {/* Saved Queries Section */}
        <div className="flex items-center space-x-2 px-2 py-1">
          <Bookmark className="w-4 h-4 text-white/60" />
          <span className="text-sm font-semibold text-white/60" style={{ fontFamily: 'SF Pro Text, sans-serif' }}>
            Saved Queries
          </span>
        </div>
        
        {/* Spacing */}
        <div className="py-2"></div>
        
        {/* Horizontal Separator */}
        <div className="h-px bg-white/20 mx-2"></div>
        
        {/* Spacing */}
        <div className="py-2"></div>
        
        {/* New Tab Button */}
        <Button 
          variant="ghost" 
          onClick={() => handleNavigation('new-tab')}
          className="group w-full h-10 bg-transparent hover:bg-white/20 hover:scale-[1.02] rounded-xl flex items-center justify-start px-2 space-x-2 transition-all duration-200 ease-in-out"
        >
          <Plus className="w-4 h-4 text-white/60 group-hover:text-white/80 transition-colors duration-200" />
          <span className="text-sm font-semibold text-white/60 group-hover:text-white/80 transition-colors duration-200" style={{ fontFamily: 'SF Pro Text, sans-serif' }}>
            New Tab
          </span>
        </Button>
        
        {/* Selected Query Tab - Input Field */}
        <div className="bg-white/20 rounded-xl p-3">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 bg-white rounded-full flex items-center justify-center">
              <span className="text-[#437874] text-xs font-bold">*</span>
            </div>
            <Input
              value={queryTitle}
              onChange={(e) => setQueryTitle(e.target.value)}
              className="bg-transparent border-none text-sm font-semibold text-white/70 placeholder:text-white/50 focus:ring-0 focus:border-none p-0 h-auto"
              style={{ fontFamily: 'SF Pro Text, sans-serif' }}
              placeholder="Query Title"
            />
          </div>
        </div>
      </div>

      {/* Footer Section */}
      <div className="p-1">
        <div className="flex items-center justify-between">
          <Button 
            variant="ghost" 
            size="sm"
            className="w-5 h-5 p-0 hover:bg-white/12 rounded"
            onClick={() => handleNavigation('download')}
          >
            <Download className="w-4 h-4 text-white rotate-180" />
          </Button>
          
          <div className="flex items-center space-x-1">
            <Button 
              variant="ghost" 
              size="sm"
              className="w-5 h-5 p-0 hover:bg-white/12 rounded"
              onClick={() => handleNavigation('settings')}
            >
              <Settings className="w-4 h-4 text-white" />
            </Button>
            <Button 
              variant="ghost" 
              size="sm"
              className="w-5 h-5 p-0 hover:bg-white/12 rounded"
              onClick={() => handleNavigation('info')}
            >
              <Info className="w-4 h-4 text-white" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WisdomSidebar;
