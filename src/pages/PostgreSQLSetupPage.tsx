import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';
import { Sidebar } from '@/components/Sidebar';
import { Database, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const PostgreSQLSetupPage = () => {
  const [databaseUrl, setDatabaseUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();
  const navigate = useNavigate();

  const handleAddConnection = async () => {
    if (!databaseUrl) {
      toast({
        title: "Error",
        description: "Please enter a database URL",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    
    try {
      const response = await fetch('http://localhost:5001/addConnection', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          databaseType: 'SQL',
          url: databaseUrl,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      
      toast({
        title: "Success",
        description: "Database connection added successfully",
      });

      // Reset form
      setDatabaseUrl('');
    } catch (error) {
      console.error('Error adding connection:', error);
      toast({
        title: "Error",
        description: "Failed to add database connection",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex-1 bg-gray-50 p-8">
        <div className="max-w-2xl mx-auto">
          <div className="mb-6">
            <Button
              variant="ghost"
              onClick={() => navigate('/settings')}
              className="mb-4"
            >
              <ArrowLeft size={16} className="mr-2" />
              Back to Settings
            </Button>
            <h1 className="text-3xl font-bold text-gray-900">PostgreSQL Setup</h1>
          </div>
          
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Database size={24} />
                <span>PostgreSQL Connection</span>
              </CardTitle>
              <CardDescription>
                Configure your PostgreSQL database connection
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="url" className="text-base font-medium">
                  Database URL
                </Label>
                <Input
                  id="url"
                  type="url"
                  placeholder="postgresql://username:password@host:port/database"
                  value={databaseUrl}
                  onChange={(e) => setDatabaseUrl(e.target.value)}
                  className="w-full"
                />
                <p className="text-xs text-gray-500">
                  Enter your PostgreSQL connection string
                </p>
              </div>

              <Button 
                onClick={handleAddConnection}
                disabled={isLoading || !databaseUrl}
                className="w-full"
              >
                {isLoading ? 'Adding Connection...' : 'Add Connection'}
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default PostgreSQLSetupPage;