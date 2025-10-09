import React, { useState, useEffect } from 'react';
import WisdomSidebar from '@/components/WisdomSidebar';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { useToast } from '@/hooks/use-toast';
import { useNavigate } from 'react-router-dom';

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
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:5001/machine-health', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      console.log('Response status:', response.status);
      console.log('Response ok:', response.ok);

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Raw response data:', data);
      console.log('Machines array:', data.machines);
      console.log('Number of machines:', data.machines?.length || 0);
      
      setMachines(data.machines || []);
    } catch (error) {
      console.error('Error fetching machine data:', error);
      setError('Failed to load machine data. Please check your backend connection.');
      toast({
        title: "Error",
        description: "Could not connect to backend. Please try again.",
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

  console.log('Current state - machines:', machines, 'isLoading:', isLoading, 'error:', error);

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
