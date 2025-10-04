import React from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface ChartData {
  type: 'pie' | 'bar';
  title: string;
  data: {
    labels: string[];
    datasets: Array<{
      label: string;
      data: number[];
      backgroundColor?: string[];
      borderColor?: string[];
      borderWidth?: number;
    }>;
  };
  options?: {
    responsive?: boolean;
    plugins?: {
      legend?: {
        position?: string;
      };
      title?: {
        display?: boolean;
        text?: string;
      };
    };
    scales?: {
      y?: {
        beginAtZero?: boolean;
      };
    };
  };
}

interface ChartProps {
  chartData: ChartData;
  className?: string;
}

export const Chart: React.FC<ChartProps> = ({ chartData, className = "" }) => {
  const { type, title, data, options } = chartData;

  // Transform data for Recharts
  const rechartsData = data.labels.map((label, index) => ({
    name: label,
    value: data.datasets[0]?.data[index] || 0,
    fill: data.datasets[0]?.backgroundColor?.[index] || '#8884d8'
  }));

  const colors = data.datasets[0]?.backgroundColor || ['#8884d8', '#82ca9d', '#ffc658', '#ff7300'];

  if (type === 'pie') {
    return (
      <div className={`bg-white p-6 rounded-lg shadow-sm border ${className}`}>
        <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">{title}</h3>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={rechartsData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {rechartsData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  }

  if (type === 'bar') {
    return (
      <div className={`bg-white p-6 rounded-lg shadow-sm border ${className}`}>
        <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">{title}</h3>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={rechartsData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill={colors[0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  }

  return null;
};

interface ChartContainerProps {
  chartData?: ChartData;
  statusChart?: ChartData;
  asciiChart?: string;
}

export const ChartContainer: React.FC<ChartContainerProps> = ({ 
  chartData, 
  statusChart, 
  asciiChart 
}) => {
  return (
    <div className="space-y-6 my-6">
      {/* ASCII Chart Fallback */}
      {asciiChart && (
        <div className="bg-gray-50 p-4 rounded-lg border">
          <pre className="text-sm font-mono text-gray-700 whitespace-pre-wrap">
            {asciiChart}
          </pre>
        </div>
      )}
      
      {/* Main Chart */}
      {chartData && (
        <Chart chartData={chartData} />
      )}
      
      {/* Status Chart */}
      {statusChart && (
        <Chart chartData={statusChart} />
      )}
    </div>
  );
};
