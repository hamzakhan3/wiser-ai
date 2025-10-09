import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';
import WisdomSidebar from '@/components/WisdomSidebar';
import { Database, Cloud, FileText, Link, Clipboard, CheckCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const SettingsPage = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const isConnected = true; // Hardcoded as connected

  const handleDataSourceSelect = (source: string) => {
    if (source === 'SQL') {
      navigate('/postgresql-setup');
      return;
    }
    
    // Handle other data sources here if needed
    toast({
      title: "Coming Soon",
      description: `${source} integration is not yet available`,
      variant: "destructive",
    });
  };

  const dataSourceOptions = [
    {
      category: "Database Connections",
      options: [
        { id: "SQL", name: "PostgreSQL", icon: Database },
        { id: "MYSQL", name: "MySQL", icon: Database },
        { id: "MONGO", name: "MongoDB", icon: Database },
      ]
    },
    {
      category: "Cloud Services",
      options: [
        { id: "REDSHIFT", name: "Amazon Redshift", icon: Cloud },
        { id: "BIGQUERY", name: "Google BigQuery", icon: Cloud },
        { id: "SNOWFLAKE", name: "Snowflake", icon: Cloud },
      ]
    },
    {
      category: "Import Options",
      options: [
        { id: "IMPORT_FILE", name: "Import from File", icon: FileText },
        { id: "IMPORT_URL", name: "Import from URL", icon: Link },
        { id: "IMPORT_CLIPBOARD", name: "Import from Clipboard", icon: Clipboard },
      ]
    }
  ];

  return (
    <div className="flex min-h-screen">
      <WisdomSidebar />
      <div className="flex-1 bg-gray-50 p-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Settings</h1>
          
          <Card className="h-fit">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Data Source Options</span>
                {isConnected && (
                  <div className="flex items-center gap-2 text-green-600 text-sm font-normal">
                    <CheckCircle size={16} />
                    <span>PostgreSQL Connected</span>
                  </div>
                )}
              </CardTitle>
              <CardDescription>
                Choose a data source to connect to your application.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {dataSourceOptions.map((category) => (
                <div key={category.category} className="space-y-3">
                  <Label className="text-sm font-medium text-gray-500 uppercase tracking-wide">
                    {category.category}
                  </Label>
                  <div className="space-y-2">
                    {category.options.map((option) => (
                      <button
                        key={option.id}
                        onClick={() => handleDataSourceSelect(option.id)}
                        className={`w-full flex items-center space-x-3 p-3 rounded-lg border transition-colors ${
                          option.id === 'SQL' && isConnected
                            ? 'bg-green-50 border-green-200 text-green-700'
                            : 'bg-white border-gray-200 text-gray-700 hover:bg-gray-50'
                        }`}
                      >
                        <option.icon size={20} />
                        <span className="text-sm font-medium flex-1 text-left">{option.name}</span>
                        {option.id === 'SQL' && isConnected && (
                          <CheckCircle size={16} className="text-green-600" />
                        )}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
