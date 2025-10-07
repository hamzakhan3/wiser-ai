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
      <div className={`bg-gradient-to-br from-white to-gray-50 p-8 rounded-2xl shadow-lg border border-gray-200/50 ${className}`}>
        <h3 className="text-xl font-bold text-gray-800 mb-6 text-center tracking-tight">{title}</h3>
        <div className="h-96">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <defs>
                {colors.map((color, index) => (
                  <linearGradient key={`gradient-${index}`} id={`gradient-${index}`} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={color} stopOpacity={1} />
                    <stop offset="100%" stopColor={color} stopOpacity={0.7} />
                  </linearGradient>
                ))}
              </defs>
              <Pie
                data={rechartsData}
                cx="50%"
                cy="50%"
                labelLine={true}
                label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                outerRadius={120}
                innerRadius={70}
                fill="#8884d8"
                dataKey="value"
                paddingAngle={2}
                stroke="#fff"
                strokeWidth={3}
              >
                {rechartsData.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={`url(#gradient-${index})`}
                  />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(255, 255, 255, 0.98)', 
                  border: 'none', 
                  borderRadius: '12px', 
                  boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
                  padding: '12px'
                }}
              />
              <Legend 
                verticalAlign="bottom" 
                height={36}
                wrapperStyle={{ paddingTop: '20px' }}
                iconType="circle"
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    );
  }

  if (type === 'bar') {
    return (
      <div className={`bg-gradient-to-br from-white to-gray-50 p-8 rounded-2xl shadow-lg border border-gray-200/50 ${className}`}>
        <h3 className="text-xl font-bold text-gray-800 mb-6 text-center tracking-tight">{title}</h3>
        <div className="h-[500px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart 
              data={rechartsData} 
              layout="horizontal" 
              margin={{ top: 10, right: 40, left: 140, bottom: 30 }}
            >
              <defs>
                <linearGradient id="barGradient" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor={colors[0]} stopOpacity={0.8} />
                  <stop offset="100%" stopColor={colors[0]} stopOpacity={1} />
                </linearGradient>
              </defs>
              <CartesianGrid 
                strokeDasharray="3 3" 
                stroke="#e5e7eb" 
                vertical={false}
              />
              <XAxis 
                type="number" 
                tick={{ fontSize: 13, fill: '#6b7280' }}
                axisLine={{ stroke: '#d1d5db' }}
                tickLine={{ stroke: '#d1d5db' }}
              />
              <YAxis 
                type="category" 
                dataKey="name" 
                width={130}
                tick={{ fontSize: 13, fill: '#374151', fontWeight: 500 }}
                axisLine={{ stroke: '#d1d5db' }}
                tickLine={{ stroke: '#d1d5db' }}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(255, 255, 255, 0.98)', 
                  border: 'none', 
                  borderRadius: '12px', 
                  boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
                  padding: '12px'
                }}
                cursor={{ fill: 'rgba(107, 155, 151, 0.1)' }}
              />
              <Legend 
                wrapperStyle={{ paddingTop: '10px' }}
                iconType="circle"
              />
              <Bar 
                dataKey="value" 
                fill="url(#barGradient)" 
                radius={[0, 8, 8, 0]}
                maxBarSize={40}
              >
                {rechartsData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                ))}
              </Bar>
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
