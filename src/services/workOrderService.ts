
export interface WorkOrderData {
  pageNo: string;
  priority: string;
  companyName: string;
  workOrderNo: string;
  weekNo: string;
  weekOf: string;
  equipmentId: string;
  category: string;
  equipmentDescription: string;
  building: string;
  floor: string;
  room: string;
  description: string;
  emergencyContact: string;
  specialInstructions: string;
  shopVendor: string;
  departmentName: string;
  employee: string;
  taskNo: string;
  workDescription: string;
  frequency: string;
  partNumbers: Array<{
    partNo: string;
    description: string;
    quantity: string;
    qtyInStock: string;
    location: string;
  }>;
  workPerformedBy: string;
  date: string;
  standardHours: string;
  overtimeHours: string;
  materialsUsed: Array<{
    description: string;
    quantity: string;
    partNo: string;
  }>;
}

const API_URL = 'http://localhost:5001';

export async function submitWorkOrder(workOrderData: WorkOrderData, machineId?: string): Promise<any> {
  console.log('Submitting work order data:', workOrderData);
  
  try {
    const response = await fetch(`${API_URL}/work-order`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...workOrderData,
        ...(machineId && { machineId })
      }),
    });

    console.log(`Submit response status: ${response.status}`);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const result = await response.json();
    console.log('Work order submitted successfully:', result);
    return result;
    
  } catch (error) {
    console.error('Error submitting work order:', error);
    throw error;
  }
}
