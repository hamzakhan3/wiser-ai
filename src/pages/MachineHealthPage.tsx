import React, { useState, useEffect } from 'react';
import WisdomSidebar from '@/components/WisdomSidebar';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { useToast } from '@/hooks/use-toast';
import { useNavigate } from 'react-router-dom';

// Use localhost for local development
const API_URL = 'http://localhost:5001';

// Debug: Log the current hostname
console.log('Current hostname:', window.location.hostname);
console.log('Current origin:', window.location.origin);
console.log('API_URL constant:', API_URL);

// Test the API_URL by making a simple request to the root
fetch(API_URL)
  .then(response => {
    console.log('Root API test - Status:', response.status);
    console.log('Root API test - OK:', response.ok);
  })
  .catch(error => {
    console.error('Root API test failed:', error);
  });

// Test the working maintenance-tasks endpoint for comparison
fetch(`${API_URL}/maintenance-tasks`)
  .then(response => response.text())
  .then(text => {
    console.log('Maintenance-tasks test - Response length:', text.length);
    console.log('Maintenance-tasks test - First 100 chars:', text.substring(0, 100));
    console.log('Maintenance-tasks test - Is JSON?', text.startsWith('{'));
  })
  .catch(error => {
    console.error('Maintenance-tasks test failed:', error);
  });

// Add a button to test the URL directly
console.log('🔗 Test URL directly:', `${API_URL}/maintenance-tasks`);
console.log('🔗 Open this URL in a new tab to see if it shows the ngrok warning page');

interface MachineData {
  id: string;
  machine: string;
  severityLevel: string;
  lastAnomaly: string;
  sensorType: string;
}

const MachineHealthPage = () => {
  const [machines, setMachines] = useState<MachineData[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedMachine, setSelectedMachine] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();
  const navigate = useNavigate();

  const fetchMachineData = async () => {
    console.log('Fetching machine data from backend...');
    console.log('API_URL:', API_URL);
    console.log('Full URL:', `${API_URL}/machine-health`);
    setIsLoading(true);
    setError(null);
    try {
      const fullUrl = `${API_URL}/machine-health`;
      console.log('Making request to:', fullUrl);
      console.log('Request headers:', {
        'note': 'No custom headers (removed Content-Type to avoid ngrok warning)',
      });
      
      const response = await fetch(fullUrl, {
        method: 'GET',
        // Remove Content-Type header to avoid triggering ngrok warning
        cache: 'no-cache', // Force fresh request
      });

      console.log('Response status:', response.status);
      console.log('Response ok:', response.ok);
      console.log('Response headers:', Object.fromEntries(response.headers.entries()));

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      // Log the raw response text before parsing
      const responseText = await response.text();
      console.log('Raw response text:', responseText);
      console.log('Response text length:', responseText.length);
      console.log('First 100 chars:', responseText.substring(0, 100));
      
      // Check if response is HTML (ngrok warning page)
      if (responseText.trim().startsWith('<!DOCTYPE') || responseText.trim().startsWith('<html')) {
        console.warn('Received HTML response (likely ngrok warning page)');
        throw new Error('Received HTML response instead of JSON. This might be the ngrok warning page.');
      }
      
      // Try to parse as JSON
      let data;
      try {
        data = JSON.parse(responseText);
      } catch (parseError) {
        console.error('JSON parse error:', parseError);
        console.error('Response was not valid JSON');
        throw new Error(`Invalid JSON response: ${parseError.message}`);
      }
      console.log('=== BACKEND RESPONSE DEBUG ===');
      console.log('Raw response data:', data);
      console.log('Response type:', typeof data);
      console.log('Response keys:', Object.keys(data));
      
      // Handle both machine-health and maintenance-tasks responses
      if (data.machines) {
        console.log('Machines array:', data.machines);
        console.log('Machines type:', typeof data.machines);
        console.log('Machines length:', data.machines?.length || 0);
        console.log('Is machines array?', Array.isArray(data.machines));
        console.log('First machine:', data.machines?.[0]);
        setMachines(data.machines || []);
      } else if (data.tasks) {
        console.log('Tasks array (testing with maintenance-tasks):', data.tasks);
        console.log('Tasks length:', data.tasks?.length || 0);
        // Convert tasks to machines format for testing
        const convertedMachines = data.tasks.map((task: any) => ({
          id: task.id,
          machine: task.machineName,
          severityLevel: task.priority.toUpperCase(),
          lastAnomaly: task.scheduledDate,
          sensorType: 'Maintenance'
        }));
        console.log('Converted machines:', convertedMachines);
        setMachines(convertedMachines);
      }
      console.log('=== END DEBUG ===');
    } catch (error) {
      console.error('Error fetching machine data:', error);
      console.error('Error details:', {
        message: error.message,
        name: error.name,
        stack: error.stack
      });
      setError(`Failed to load machine data: ${error.message}`);
      toast({
        title: "Error",
        description: `Could not connect to backend: ${error.message}`,
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    console.log('MachineHealthPage mounted, fetching data...');
    fetchMachineData();
  }, []);

  // Debug: Log when machines state changes
  useEffect(() => {
    console.log('=== MACHINES STATE CHANGED ===');
    console.log('New machines state:', machines);
    console.log('Machines length:', machines.length);
    console.log('=== END MACHINES STATE CHANGE ===');
  }, [machines]);

  const handleRowClick = (machineId: string) => {
    console.log('Row clicked for machine:', machineId);
    setSelectedMachine(machineId);
  };

  const handleInspectAnomaly = (machine: MachineData) => {
    console.log('Inspect Anomaly clicked for machine:', machine);
    console.log('Machine ID being passed:', machine.id);
    console.log('Machine name being passed:', machine.machine);
    console.log('Sensor type being passed:', machine.sensorType);
    
    toast({
      title: "Inspect Anomaly",
      description: `Inspecting anomaly for ${machine.machine}`,
    });
    
    // Navigate to inspection page with machine ID, machine name, and sensor type as URL parameters
    // Using machine.id (which is the machine_id from backend), machine.machine (machine name), and machine.sensorType
    navigate(`/inspection?machineId=${encodeURIComponent(machine.id)}&machineName=${encodeURIComponent(machine.machine)}&sensorType=${encodeURIComponent(machine.sensorType)}`);
  };

  console.log('=== COMPONENT STATE DEBUG ===');
  console.log('Current state - machines:', machines);
  console.log('Machines length:', machines.length);
  console.log('isLoading:', isLoading);
  console.log('error:', error);
  console.log('=== END STATE DEBUG ===');

  return (
    <div className="flex min-h-screen">
      <WisdomSidebar />
      <div className="flex-1 bg-gray-50 p-8">
        <div className="max-w-6xl mx-auto">
          <div className="flex justify-between items-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Machine Health Monitor</h1>
            <Button onClick={fetchMachineData} disabled={isLoading}>
              {isLoading ? 'Refreshing...' : 'Refresh Data'}
            </Button>
          </div>
          
          {isLoading ? (
            <div className="text-center py-8">
              <p className="text-gray-500">Loading machine data...</p>
            </div>
          ) : error ? (
            <div className="text-center py-8">
              <p className="text-red-500 mb-4">{error}</p>
              <Button onClick={fetchMachineData}>Try Again</Button>
            </div>
          ) : machines.length > 0 ? (
            <div className="bg-white rounded-lg shadow">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Machine</TableHead>
                    <TableHead>Severity Level</TableHead>
                    <TableHead>Last Anomaly</TableHead>
                    <TableHead>Sensor Type</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {machines.map((machine) => (
                    <TableRow 
                      key={machine.id}
                      className={`cursor-pointer hover:bg-gray-50 ${
                        selectedMachine === machine.id ? 'bg-blue-50' : ''
                      }`}
                      onClick={() => handleRowClick(machine.id)}
                    >
                      <TableCell className="font-medium">{machine.machine}</TableCell>
                      <TableCell>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                          machine.severityLevel === 'CRITICAL' ? 'bg-red-200 text-red-900 font-bold' :
                          machine.severityLevel === 'High' ? 'bg-red-100 text-red-800' :
                          machine.severityLevel === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {machine.severityLevel}
                        </span>
                      </TableCell>
                      <TableCell>{new Date(machine.lastAnomaly).toLocaleString()}</TableCell>
                      <TableCell>{machine.sensorType}</TableCell>
                      <TableCell>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleInspectAnomaly(machine);
                          }}
                        >
                          Inspect Anomaly
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-gray-500">No machine data available. Please try refreshing.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MachineHealthPage;
