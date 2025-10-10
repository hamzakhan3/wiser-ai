import React, { useState, useEffect } from 'react';
import WisdomSidebar from '@/components/WisdomSidebar';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Calendar } from '@/components/ui/calendar';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { CalendarDays, Clock, Wrench, Sparkles, ChevronDown, CheckCircle, Edit, Calendar as CalendarIcon } from 'lucide-react';
import { format, isSameDay } from 'date-fns';
import { fetchMaintenanceTasks, MaintenanceTask } from '@/services/apiService';
import { useToast } from '@/hooks/use-toast';
import { WorkOrderForm } from '@/components/WorkOrderForm';

const MaintenanceSchedulePage = () => {
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());
  const [viewMode, setViewMode] = useState<'calendar' | 'list'>('list');
  const [maintenanceTasks, setMaintenanceTasks] = useState<MaintenanceTask[]>([]);
  const [loading, setLoading] = useState(true);
  const [showWorkOrderForm, setShowWorkOrderForm] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    const loadMaintenanceTasks = async () => {
      try {
        const tasks = await fetchMaintenanceTasks();
        setMaintenanceTasks(tasks);
      } catch (error) {
        console.error('Failed to load maintenance tasks:', error);
        toast({
          title: "Error",
          description: "Failed to load maintenance tasks. Please try again.",
          variant: "destructive",
        });
      } finally {
        setLoading(false);
      }
    };

    loadMaintenanceTasks();
  }, [toast]);

  const getTasksForDate = (date: Date) => {
    return maintenanceTasks.filter(task => isSameDay(new Date(task.scheduledDate), date));
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'resolved': return 'bg-[#437874] text-white';
      case 'in-progress': return 'bg-blue-100 text-blue-800';
      case 'overdue': return 'bg-red-100 text-red-800';
      case 'scheduled': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  // Get dates that have maintenance tasks for the main calendar
  const getDatesWithTasks = () => {
    return maintenanceTasks.map(task => new Date(task.scheduledDate));
  };

  const datesWithTasks = getDatesWithTasks();
  const selectedDateTasks = getTasksForDate(selectedDate);

  const handleWorkOrderSubmit = (workOrderData: any) => {
    console.log('Work order data:', workOrderData);
    setShowWorkOrderForm(false);
    
    toast({
      title: "Work Order Generated",
      description: "Work order has been successfully created.",
    });
  };

  const handleTaskAction = (taskId: string, action: 'resolve' | 'edit' | 'reschedule' 
  | 'in-progress'
  ) => {
  console.log(`${action} task:`, taskId);

  if (action === 'resolve') {
    setMaintenanceTasks(prev =>
      prev.map(task =>
        task.id === taskId ? { ...task, status: 'resolved' } : task
      )
    );
    toast({
      title: "Task Resolved",
      description: "Maintenance task has been marked as resolved.",
    });
    return;
  }
    if (action === 'in-progress') {
    setMaintenanceTasks(prev =>
      prev.map(task =>
        task.id === taskId ? { ...task, status: 'in-progress' } : task
      )
    );
    toast({
      title: "Task In Progress",
      description: "Maintenance task is now in progress.",
    });
    return;
  }
  if (action === 'reschedule') {
    setMaintenanceTasks(prev =>
      prev.map(task =>
        task.id === taskId ? { ...task, status: 'scheduled' } : task
      )
    );
    toast({
      title: "Task Rescheduled",
      description: "Maintenance task has been re-scheduled.",
    });
    return;
  }
  
  switch (action) {
    case 'edit':
      toast({
        title: "Edit Task",
        description: "Edit task functionality will be implemented.",
      });
      break;
  }
};

  if (loading) {
    return (
      <div className="min-h-screen flex w-full">
        <WisdomSidebar />
        
        <div className="flex-1 flex flex-col bg-gray-50">
          <div className="bg-white border-b border-gray-200 px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <CalendarDays className="h-8 w-8 text-sage-500" />
                <div>
                  <h1 
                    style={{
                      fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                      fontWeight: 500,
                      fontSize: '28px',
                      lineHeight: '1.2',
                      letterSpacing: '-0.02em',
                      color: '#2d3748',
                      textTransform: 'none',
                      textAlign: 'left'
                    }}
                  >
                    Preventive Maintenance Scheduler
                  </h1>
                  <p className="text-gray-600">Schedule and track machine maintenance tasks</p>
                </div>
              </div>
            </div>
          </div>

          <div className="flex-1 p-6 flex items-center justify-center">
            <p className="text-gray-500">Loading maintenance tasks...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex w-full">
      <WisdomSidebar />
      
      <div className="flex-1 flex flex-col bg-gray-50">
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <CalendarDays className="h-8 w-8 text-sage-500" />
              <div>
                <h1 
                  style={{
                    fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                    fontWeight: 500,
                    fontSize: '28px',
                    lineHeight: '1.2',
                    letterSpacing: '-0.02em',
                    color: '#2d3748',
                    textTransform: 'none',
                    textAlign: 'left'
                  }}
                >
                  Preventive Maintenance Scheduler
                </h1>
                <p className="text-gray-600">Schedule and track machine maintenance tasks</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-1 bg-gray-100 rounded-lg p-0.5 mt-6 ml-auto">
              <button
                onClick={() => setViewMode('calendar')}
                className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                  viewMode === 'calendar'
                    ? 'bg-white text-gray-900 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                Calendar View
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                  viewMode === 'list'
                    ? 'bg-white text-gray-900 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                List View
              </button>
            </div>
          </div>
        </div>

        <div className="flex-1 p-6">
          {viewMode === 'calendar' ? (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Main Calendar */}
              <Card>
                <CardHeader>
                  <CardTitle>Maintenance Calendar</CardTitle>
                </CardHeader>
                <CardContent className="flex justify-center">
                  <Calendar
                    mode="single"
                    selected={selectedDate}
                    onSelect={(date) => {
                      if (date) {
                        setSelectedDate(date);
                      }
                    }}
                    className="rounded-md border"
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
                </CardContent>
              </Card>

              {/* Selected Date Tasks */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <span>Tasks for {format(selectedDate, 'MMM dd, yyyy')}</span>
                    <span className="text-sm text-gray-500">({selectedDateTasks.length} tasks)</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {selectedDateTasks.length === 0 ? (
                    <p className="text-gray-500 text-center py-4">No maintenance tasks scheduled for this date</p>
                  ) : (
                    <div className="space-y-4">
                      {selectedDateTasks.map((task) => (
                        <div key={task.id} className="border rounded-lg p-4 bg-white shadow-sm">
                          <div className="flex items-start justify-between mb-2">
                            <div>
                              <h4 className="font-medium text-gray-900">{task.machineName}</h4>
                              <p className="text-sm text-gray-600">{task.taskType}</p>
                            </div>
                                  <div
                                    className={`w-3 h-3 rounded-full ${
                                      task.status === 'resolved'
                                          ? 'bg-sage-500'
                                          : task.status === 'scheduled'
                                          ? 'bg-gray-400'
                                          : task.status === 'in-progress'
                                          ? 'bg-blue-500'
                                          : getPriorityColor(task.priority)

                                    }`}
                                  />                          
                                  </div>
                          
                          <p className="text-sm text-gray-500 mb-2">{task.description}</p>
                          
                          <div className="flex items-center justify-between text-sm">
                            <div className="flex items-center space-x-2">
                              <Clock className="h-4 w-4" />
                              <span>{task.duration}h</span>
                            </div>
                            <Badge className={getStatusColor(task.status)}>
                              {task.status}
                            </Badge>
                          </div>
                          
                          {task.assignedTechnician && (
                            <p className="text-sm text-gray-500 mt-2">
                              Assigned: {task.assignedTechnician}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          ) : (
            /* List View */
            <div className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle 
                    style={{
                      fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                      fontWeight: 500,
                      fontSize: '28px',
                      lineHeight: '1.2',
                      letterSpacing: '-0.02em',
                      color: '#2d3748',
                      textTransform: 'none',
                      textAlign: 'left'
                    }}
                  >
                    All Scheduled Maintenance Tasks
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {maintenanceTasks.length === 0 ? (
                    <p className="text-gray-500 text-center py-4">No maintenance tasks found</p>
                  ) : (
                    <div className="space-y-3">
                      {maintenanceTasks.map((task) => (
                        <div key={task.id} className="border rounded-lg p-4 bg-white shadow-sm">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <div className="flex items-center space-x-3 mb-2">
                                <h4 className="font-medium text-gray-900">{task.machineName}</h4>
                                <Badge className={getStatusColor(task.status)}>
                                  {task.status}
                                </Badge>
                                    <div
                                      className={`w-3 h-3 rounded-full ${
                                        task.status === 'resolved'
                                          ? 'bg-sage-500'
                                          : task.status === 'scheduled'
                                          ? 'bg-gray-400'
                                          : task.status === 'in-progress'
                                          ? 'bg-blue-500'
                                          : getPriorityColor(task.priority)
                                      }`}
                                    />                             </div>
                              
                              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                                <div>
                                  <span className="text-gray-500">Task:</span>
                                  <p className="font-medium">{task.taskType}</p>
                                </div>
                                <div>
                                  <span className="text-gray-500">Date:</span>
                                  <p className="font-medium">{format(new Date(task.scheduledDate), 'MMM dd, yyyy')}</p>
                                </div>
                                <div>
                                  <span className="text-gray-500">Duration:</span>
                                  <p className="font-medium">{task.duration} hours</p>
                                </div>
                                <div>
                                  <span className="text-gray-500">Technician:</span>
                                  <p className="font-medium">{task.assignedTechnician || 'Unassigned'}</p>
                                </div>
                              </div>
                              
                              <p className="text-sm text-gray-600 mt-2">{task.description}</p>
                            </div>
                            
                            <div className="ml-4">
                              <DropdownMenu>
                                <DropdownMenuTrigger asChild>
                                  <Button variant="outline" size="sm">
                                    <Wrench className="h-4 w-4 mr-1" />
                                    Manage
                                    <ChevronDown className="h-4 w-4 ml-1" />
                                  </Button>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent align="end">
                                  <DropdownMenuItem onClick={() => handleTaskAction(task.id, 'resolve')}>
                                    <CheckCircle className="h-4 w-4 mr-2" />
                                    Resolve Task
                                  </DropdownMenuItem>
                                  <DropdownMenuItem onClick={() => handleTaskAction(task.id, 'in-progress')}>
                                    <Clock className="h-4 w-4 mr-2" />
                                    Mark In Progress
                                  </DropdownMenuItem>
                                  <DropdownMenuItem onClick={() => handleTaskAction(task.id, 'edit')}>
                                    <Edit className="h-4 w-4 mr-2" />
                                    Edit Task
                                  </DropdownMenuItem>
                                  <DropdownMenuItem onClick={() => handleTaskAction(task.id, 'reschedule')}>
                                    <CalendarIcon className="h-4 w-4 mr-2" />
                                    Reschedule Task
                                  </DropdownMenuItem>
                                </DropdownMenuContent>
                              </DropdownMenu>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </div>

      {/* Work Order Form Modal */}
      {showWorkOrderForm && (
        <WorkOrderForm
          onClose={() => setShowWorkOrderForm(false)}
          onSubmit={handleWorkOrderSubmit}
        />
      )}
    </div>
  );
};

export default MaintenanceSchedulePage;
