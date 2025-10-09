import React, { useState } from 'react';
import { FileText, Settings, Info, BookmarkIcon, Heart, CalendarDays, Lightbulb } from 'lucide-react';
import { Button } from './ui/button';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from './ui/tooltip';
import { Calendar } from './ui/calendar';
import { useNavigate, useLocation } from 'react-router-dom';
import { isSameDay } from 'date-fns';

interface MaintenanceTask {
  id: string;
  machineId: string;
  machineName: string;
  taskType: string;
  description: string;
  scheduledDate: Date;
  duration: number;
  priority: 'low' | 'medium' | 'high' | 'critical';
  status: 'scheduled' | 'in-progress' | 'completed' | 'overdue';
  assignedTechnician?: string;
}

interface SidebarProps {
  maintenanceTasks?: MaintenanceTask[];
  selectedDate?: Date;
  onDateSelect?: (date: Date) => void;
}

export const Sidebar = ({ maintenanceTasks = [], selectedDate, onDateSelect }: SidebarProps) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [showCalendar, setShowCalendar] = useState(false);

  const handleSettingsClick = () => {
    navigate('/settings');
  };

  const handleLogoClick = () => {
    navigate('/');
  };

  const handleMachineHealthClick = () => {
    console.log('Heart icon clicked - navigating to /machine-health');
    navigate('/machine-health');
  };

  const handleMaintenanceScheduleClick = () => {
    console.log('Calendar icon clicked');
    
    // If we're already on the maintenance schedule page, just toggle the calendar
    if (location.pathname === '/maintenance-schedule') {
      console.log('Already on maintenance schedule page, toggling calendar');
      setShowCalendar(!showCalendar);
    } else {
      // If we're on a different page, navigate to maintenance schedule
      console.log('Navigating to /maintenance-schedule');
      navigate('/maintenance-schedule');
      setShowCalendar(true); // Show calendar when navigating to the page
    }
  };

  const handleWisdomClick = () => {
    navigate('/wisdom');
  };

  // Get dates that have maintenance tasks
  const getDatesWithTasks = () => {
    return maintenanceTasks.map(task => task.scheduledDate);
  };

  const datesWithTasks = getDatesWithTasks();

  return (
    <div className="h-screen bg-primary flex text-white relative">
      {/* Main sidebar */}
      <div className="w-[80px] flex flex-col items-center py-4">
        <button 
          onClick={handleLogoClick}
          className="mb-8 text-xl font-bold hover:opacity-80 transition-opacity cursor-pointer"
        >
          <span className="text-white">(</span>
          <span className="text-sage-200">*</span>
          <span className="text-white">)</span>
        </button>
        
        <div className="flex flex-col space-y-6">
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost" size="icon" className="text-white hover:bg-primary/80">
                  <FileText size={20} />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="right">
                <p>Documents</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>

          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost" size="icon" className="text-white hover:bg-primary/80">
                  <BookmarkIcon size={20} />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="right">
                <p>Saved Queries</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>

          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button 
                  variant="ghost" 
                  size="icon" 
                  className="text-white hover:bg-primary/80"
                  onClick={handleWisdomClick}
                >
                  <Lightbulb size={20} />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="right">
                <p>Discover Wisdom</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>

          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button 
                  variant="ghost" 
                  size="icon" 
                  className="text-white hover:bg-primary/80"
                  onClick={handleMachineHealthClick}
                >
                  <Heart size={20} />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="right">
                <p>Machine Health</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>

          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button 
                  variant="ghost" 
                  size="icon" 
                  className={`text-white hover:bg-primary/80 ${showCalendar && location.pathname === '/maintenance-schedule' ? 'bg-primary/80' : ''}`}
                  onClick={handleMaintenanceScheduleClick}
                >
                  <CalendarDays size={20} />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="right">
                <p>Maintenance Schedule</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>

          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button 
                  variant="ghost" 
                  size="icon" 
                  className="text-white hover:bg-primary/80"
                  onClick={handleSettingsClick}
                >
                  <Settings size={20} />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="right">
                <p>Settings</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>

          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost" size="icon" className="text-white hover:bg-primary/80">
                  <Info size={20} />
                </Button>
              </TooltipTrigger>
              <TooltipContent side="right">
                <p>Information</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        </div>
      </div>

      {/* Calendar panel - only show on maintenance schedule page */}
      {showCalendar && location.pathname === '/maintenance-schedule' && (
        <div className="w-[320px] bg-white text-black p-4 shadow-lg border-l border-gray-200">
          <h3 className="font-semibold mb-4 text-gray-900">Maintenance Calendar</h3>
          <Calendar
            mode="single"
            selected={selectedDate}
            onSelect={(date) => {
              if (date && onDateSelect) {
                onDateSelect(date);
              }
            }}
            className="rounded-md border w-full"
            modifiers={{
              hasTask: datesWithTasks,
            }}
            modifiersStyles={{
              hasTask: {
                backgroundColor: '#10b981',
                color: 'white',
                fontWeight: 'bold',
              },
            }}
          />
          
          {/* Show tasks for selected date */}
          {selectedDate && (
            <div className="mt-4">
              <h4 className="font-medium text-gray-900 mb-2">
                Tasks for {selectedDate.toLocaleDateString()}
              </h4>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {maintenanceTasks
                  .filter(task => isSameDay(task.scheduledDate, selectedDate))
                  .map(task => (
                    <div key={task.id} className="text-xs bg-gray-50 p-2 rounded">
                      <div className="font-medium">{task.machineName}</div>
                      <div className="text-gray-600">{task.taskType}</div>
                      <div className="text-gray-500">{task.duration}h</div>
                    </div>
                  ))}
                {maintenanceTasks.filter(task => isSameDay(task.scheduledDate, selectedDate)).length === 0 && (
                  <p className="text-gray-500 text-xs">No tasks scheduled</p>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};