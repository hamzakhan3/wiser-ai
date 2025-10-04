
import React from 'react';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { PlusCircle } from 'lucide-react';

export const NewTab = () => {
  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center gap-2">
        <Button variant="outline" size="sm" className="flex items-center gap-1 bg-white">
          <PlusCircle size={14} />
          <span>New Tab</span>
        </Button>
      </div>
      
      <Card className="border-dashed border-gray-300 bg-gray-50 shadow-none">
        <CardContent className="p-4">
          <Input 
            placeholder="Query Title"
            className="bg-white border-gray-200" 
          />
        </CardContent>
      </Card>
    </div>
  );
};
