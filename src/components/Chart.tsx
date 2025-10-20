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
    // Calculate total for center display
    const total = rechartsData.reduce((sum, entry) => sum + entry.value, 0);
    
    return (
      <div 
        className={`relative bg-gradient-to-br from-sage-50/80 via-white to-sage-100/40 p-12 rounded-3xl shadow-2xl border-2 border-sage-200/50 backdrop-blur-sm overflow-hidden ${className}`}
        style={{
          animation: 'chartFadeIn 0.8s ease-out forwards, chartSlideUp 0.8s ease-out forwards',
          opacity: 0,
          transform: 'translateY(20px)'
        }}
      >
        <style>{`
          @keyframes chartFadeIn {
            from {
              opacity: 0;
            }
            to {
              opacity: 1;
            }
          }
          
          @keyframes chartSlideUp {
            from {
              transform: translateY(20px) scale(0.98);
            }
            to {
              transform: translateY(0) scale(1);
            }
          }
          
          @keyframes chartPulse {
            0%, 100% {
              transform: scale(1);
            }
            50% {
              transform: scale(1.02);
            }
          }
          
          @keyframes lineExpand {
            from {
              width: 0;
            }
            to {
              width: 3rem;
            }
          }
          
          @keyframes statsSlideIn {
            from {
              opacity: 0;
              transform: translateY(10px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }
        `}</style>
        {/* Decorative background elements */}
        <div 
          className="absolute top-0 right-0 w-64 h-64 bg-sage-200/20 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"
          style={{
            animation: 'chartFadeIn 1s ease-out 0.2s forwards',
            opacity: 0
          }}
        ></div>
        <div 
          className="absolute bottom-0 left-0 w-48 h-48 bg-sage-300/20 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2"
          style={{
            animation: 'chartFadeIn 1s ease-out 0.3s forwards',
            opacity: 0
          }}
        ></div>
        
        {/* Title with decorative line */}
        <div 
          className="relative mb-10"
          style={{
            animation: 'chartFadeIn 0.6s ease-out 0.3s forwards, chartSlideUp 0.6s ease-out 0.3s forwards',
            opacity: 0,
            transform: 'translateY(10px)'
          }}
        >
          <div className="flex items-center justify-center gap-4 mb-2">
            <div 
              className="h-px w-12 bg-gradient-to-r from-transparent to-sage-400"
              style={{
                animation: 'lineExpand 0.6s ease-out 0.5s forwards',
                width: 0
              }}
            ></div>
            <h3 className="text-2xl font-bold bg-gradient-to-r from-sage-700 via-sage-600 to-sage-700 bg-clip-text text-transparent text-center tracking-tight">
              {title}
            </h3>
            <div 
              className="h-px w-12 bg-gradient-to-l from-transparent to-sage-400"
              style={{
                animation: 'lineExpand 0.6s ease-out 0.5s forwards',
                width: 0
              }}
            ></div>
          </div>
          <p className="text-center text-sage-600/70 text-sm font-medium">Real-time Status Overview</p>
        </div>
        
        <div className="h-[480px] relative">
          {/* Subtle glow effect behind chart */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-72 h-72 bg-gradient-radial from-sage-200/30 via-sage-100/20 to-transparent rounded-full blur-2xl"></div>
          </div>
          
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <defs>
                {/* Enhanced gradients with multiple stops */}
                {colors.map((color, index) => (
                  <linearGradient key={`gradient-${index}`} id={`gradient-${index}`} x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stopColor={color} stopOpacity={1} />
                    <stop offset="50%" stopColor={color} stopOpacity={0.9} />
                    <stop offset="100%" stopColor={color} stopOpacity={0.8} />
                  </linearGradient>
                ))}
                {/* Radial gradient for center */}
                <radialGradient id="centerGradient">
                  <stop offset="0%" stopColor="#ffffff" stopOpacity={1} />
                  <stop offset="70%" stopColor="#f0f5f5" stopOpacity={1} />
                  <stop offset="100%" stopColor="#dde9e8" stopOpacity={1} />
                </radialGradient>
                {/* Enhanced shadows */}
                {colors.map((color, index) => (
                  <filter key={`shadow-${index}`} id={`shadow-${index}`} x="-50%" y="-50%" width="200%" height="200%">
                    <feGaussianBlur in="SourceAlpha" stdDeviation="4"/>
                    <feOffset dx="0" dy="6" result="offsetblur"/>
                    <feFlood floodColor={color} floodOpacity="0.35"/>
                    <feComposite in2="offsetblur" operator="in"/>
                    <feMerge>
                      <feMergeNode/>
                      <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                  </filter>
                ))}
              </defs>
              
              <Pie
                data={rechartsData}
                cx="50%"
                cy="50%"
                labelLine={{
                  stroke: '#6f9794',
                  strokeWidth: 2.5,
                  strokeDasharray: '5 5'
                }}
                label={({ name, percent, cx, cy, midAngle, innerRadius, outerRadius }) => {
                  const RADIAN = Math.PI / 180;
                  const radius = outerRadius + 40;
                  const x = cx + radius * Math.cos(-midAngle * RADIAN);
                  const y = cy + radius * Math.sin(-midAngle * RADIAN);
                  return (
                    <text 
                      x={x} 
                      y={y} 
                      fill="#2f544f" 
                      textAnchor={x > cx ? 'start' : 'end'} 
                      dominantBaseline="central"
                      className="font-bold text-sm drop-shadow-sm"
                      style={{ letterSpacing: '0.02em' }}
                    >
                      {`${name} ${(percent * 100).toFixed(0)}%`}
                    </text>
                  );
                }}
                outerRadius={140}
                innerRadius={85}
                fill="#8884d8"
                dataKey="value"
                paddingAngle={4}
                stroke="rgba(255, 255, 255, 1)"
                strokeWidth={5}
                animationBegin={0}
                animationDuration={1400}
                animationEasing="ease-out"
                isAnimationActive={true}
              >
                {rechartsData.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={`url(#gradient-${index})`}
                    filter={`url(#shadow-${index})`}
                    className="hover:opacity-90 transition-opacity duration-300 cursor-pointer"
                  />
                ))}
              </Pie>
              
              {/* Center text overlay */}
              <text 
                x="50%" 
                y="48%" 
                textAnchor="middle" 
                dominantBaseline="middle"
                className="font-bold text-4xl"
                fill="url(#centerGradient)"
                stroke="#437874"
                strokeWidth="0.5"
              >
                {total}
              </text>
              <text 
                x="50%" 
                y="56%" 
                textAnchor="middle" 
                dominantBaseline="middle"
                className="font-semibold text-sm"
                fill="#6f9794"
              >
                Total Machines
              </text>
              
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(255, 255, 255, 0.98)', 
                  border: '2px solid rgba(67, 120, 116, 0.3)',
                  borderRadius: '20px', 
                  boxShadow: '0 20px 40px rgba(0,0,0,0.15), 0 0 0 1px rgba(255,255,255,0.5) inset',
                  padding: '18px 22px',
                  backdropFilter: 'blur(12px)'
                }}
                itemStyle={{
                  color: '#2f544f',
                  fontWeight: '700',
                  fontSize: '15px',
                  letterSpacing: '0.02em'
                }}
                cursor={{ fill: 'rgba(67, 120, 116, 0.05)' }}
              />
              
              <Legend 
                verticalAlign="bottom" 
                height={56}
                wrapperStyle={{ 
                  paddingTop: '32px',
                  fontSize: '15px',
                  fontWeight: '700',
                  letterSpacing: '0.02em'
                }}
                iconType="circle"
                iconSize={14}
                formatter={(value) => <span className="text-sage-800">{value}</span>}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
        
        {/* Stats bar at bottom */}
        <div 
          className="mt-8 pt-6 border-t border-sage-200/50"
          style={{
            animation: 'chartFadeIn 0.6s ease-out 1.6s forwards',
            opacity: 0
          }}
        >
          <div className="flex justify-center gap-8">
            {rechartsData.map((entry, index) => (
              <div 
                key={index} 
                className="flex items-center gap-2 group cursor-pointer"
                style={{
                  animation: `statsSlideIn 0.5s ease-out ${1.8 + index * 0.1}s forwards`,
                  opacity: 0
                }}
              >
                <div 
                  className="w-3 h-3 rounded-full shadow-lg transition-transform group-hover:scale-125"
                  style={{ backgroundColor: colors[index] }}
                ></div>
                <span className="text-sm font-semibold text-sage-700 group-hover:text-sage-900 transition-colors">
                  {entry.value} {entry.name}
                </span>
              </div>
            ))}
          </div>
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
