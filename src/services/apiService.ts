// API service for communicating with the Python backend

const API_URL = 'http://localhost:5001';

export interface QueryResponse {
  response: string;
  metadata?: any;
  format?: 'markdown' | 'text';
  chart_data?: any;
  status_chart?: any;
  ascii_chart?: string;
  chart_type?: string;
}

export interface InspectionFilters {
  machineId?: string;
  machineName?: string;
  sensorType?: string;
}

export interface MultiValueDataPoint {
  timestamp: string;
  value1: number;
  value2: number;
  value3: number;
}

export interface SingleValueDataPoint {
  timestamp: string;
  value: number;
}

export interface Anomaly {
  start: string;
  end: string;
}

export interface GraphData {
  title: string;
  x_label: string;
  y_label: string;
  x_tick_labels: string[];
  vibration_data?: SingleValueDataPoint[];
  multi_value_data?: MultiValueDataPoint[];
  anomalies: Anomaly[];
  data_type: 'single' | 'multi';
}

export interface MaintenanceTask {
  id: string;
  machineId: string;
  machineName: string;
  taskType: string;
  description: string;
  scheduledDate: string;
  duration: number;
  priority: 'low' | 'medium' | 'high' | 'critical';
  status: 'scheduled' | 'in-progress' | 'completed' | 'overdue';
  assignedTechnician?: string;
}

export async function sendQuery(query: string, source?: string, machineId?: string): Promise<QueryResponse> {
  console.log(`sendQuery called with query: ${query}`);
  console.log(`Source: ${source || 'unknown'}`);
  console.log(`Machine ID: ${machineId || 'not provided'}`);
  console.log(`Sending POST request to: ${API_URL}/query`);

  const payload: any = { 
    query,
    source: source || 'unknown',
    responseFormat: 'markdown' // Request markdown format from backend
  };
  
  // Add machine_id to payload if we're on anomaly inspection page and have machine data
  if (source === 'anomaly' && machineId) {
    payload.machine_id = machineId;
    console.log('✅ Added machine_id to query payload:', machineId);
  }
  
  console.log('Request payload:', JSON.stringify(payload, null, 2));

  try {
    const response = await fetch(`${API_URL}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    console.log(`Response status: ${response.status}`);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    console.log('Response data:', data);
    
    return {
      response: data.response || data,
      format: 'markdown'
    };
  } catch (error) {
    console.error('Error querying the API:', error);
    throw error;
  }
}

export async function fetchInspectionData(filters?: InspectionFilters): Promise<GraphData> {
  console.log('🔧 fetchInspectionData called with filters:', filters);
  console.log('🏭 Machine ID from filters:', filters?.machineId);
  console.log('🏷️ Machine name from filters:', filters?.machineName);
  console.log('📡 Sensor type from filters:', filters?.sensorType);
  
  // Build query parameters for API call
  const queryParams = new URLSearchParams();
  
  if (filters?.machineId) {
    queryParams.append('machine_id', filters.machineId);
    console.log('✅ Added machine_id to query params:', filters.machineId);
  } else {
    console.log('❌ No machineId provided in filters');
  }
  
  if (filters?.machineName) {
    queryParams.append('machine_name', filters.machineName);
    console.log('✅ Added machine_name to query params:', filters.machineName);
  } else {
    console.log('❌ No machineName provided in filters');
  }
  
  if (filters?.sensorType) {
    queryParams.append('sensor_type', filters.sensorType);
    console.log('✅ Added sensor_type to query params:', filters.sensorType);
  } else {
    console.log('❌ No sensorType provided in filters');
  }
  
  const url = `${API_URL}/inspection${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;
  console.log(`🚀 Final URL being called: ${url}`);
  console.log(`📋 Query params string: ${queryParams.toString()}`);

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log(`📡 Response status: ${response.status}`);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    console.log('📊 Raw backend response:', JSON.stringify(data, null, 2));
    console.log('📈 Data type received:', data.data_type);
    console.log('📋 Title:', data.title);
    
    if (data.data_type === 'multi') {
      console.log('🔢 Multi-value data points:', data.multi_value_data?.length || 0);
      console.log('🔍 First multi-value data point:', data.multi_value_data?.[0]);
    } else {
      console.log('📈 Single-value data points:', data.vibration_data?.length || 0);
      console.log('🔍 First single-value data point:', data.vibration_data?.[0]);
    }
    
    // Fix the anomalies logging - ensure we handle both array and undefined cases
    const anomaliesArray = Array.isArray(data.anomalies) ? data.anomalies : [];
    console.log('⚠️ Anomalies count:', anomaliesArray.length);
    console.log('⚠️ Anomalies data:', anomaliesArray);
    
    // Ensure anomalies is always an array in the returned data
    return {
      ...data,
      anomalies: anomaliesArray
    };
  } catch (error) {
    console.error('❌ Error fetching inspection data:', error);
    throw error;
  }
}

export async function checkBackendStatus(): Promise<boolean> {
  console.log('checkBackendStatus called');
  console.log(`Attempting to fetch: ${API_URL}/status`);
  try {
    const response = await fetch(`${API_URL}/status`, {
      method: 'GET',
    });
    console.log(`Response status: ${response.status}`);
    return response.ok;
  } catch (error) {
    console.error('Backend connection error:', error);
    return false;
  }
}

export async function fetchMaintenanceTasks(): Promise<MaintenanceTask[]> {
  console.log('Fetching maintenance tasks from backend');
  console.log(`Sending GET request to: ${API_URL}/maintenance-tasks`);

  try {
    const response = await fetch(`${API_URL}/maintenance-tasks`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    console.log(`Response status: ${response.status}`);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    console.log('Maintenance tasks response:', data);
    
    // Extract tasks array from the response object
    return data.tasks || [];
  } catch (error) {
    console.error('Error fetching maintenance tasks:', error);
    throw error;
  }
}

export const streamResponse = async (
  query: string,
  onChar: (char: string) => void,
  onCursor: (cursor: string) => void,
  onComplete: () => void,
  onGraph?: (chartData: any) => void
): Promise<void> => {
  try {
    const response = await fetch(`${API_URL}/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('No response body');
    }

    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            if (data.type === 'char') {
              onChar(data.content);
            } else if (data.type === 'cursor') {
              onCursor(data.content);
            } else if (data.type === 'graph') {
              console.log('📊 Graph event received:', data.data);
              if (onGraph) {
                onGraph(data.data);
              }
            } else if (data.type === 'complete') {
              onComplete();
            }
          } catch (e) {
            console.error('Error parsing streaming data:', e);
          }
        }
      }
    }
  } catch (error) {
    console.error('Error streaming response:', error);
    throw error;
  }
};

export async function streamQuery(
  query: string, 
  source?: string, 
  onChunk?: (chunk: string) => void,
  onStatus?: (status: string) => void,
  onComplete?: () => void
): Promise<void> {
  console.log(`streamQuery called with query: ${query}`);
  console.log(`Source: ${source || 'unknown'}`);

  const payload = { 
    query,
    source: source || 'unknown',
    responseFormat: 'markdown',
    stream: true  // Enable streaming
  };
  
  console.log('Request payload:', JSON.stringify(payload, null, 2));

  try {
    const response = await fetch(`${API_URL}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    console.log(`Response status: ${response.status}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('No response body reader available');
    }

    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      
      if (done) {
        console.log('Stream completed');
        onComplete?.();
        break;
      }

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || ''; // Keep incomplete line in buffer

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            console.log('Received chunk:', data);
            
            switch (data.type) {
              case 'char':
                onChunk?.(data.content);
                break;
              case 'status':
                onStatus?.(data.content);
                break;
              case 'complete':
                onComplete?.();
                return;
            }
          } catch (e) {
            console.error('Error parsing SSE data:', e);
          }
        }
      }
    }
  } catch (error) {
    console.error('Error in streamQuery:', error);
    throw error;
  }
}