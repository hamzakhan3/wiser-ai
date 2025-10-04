
import React from 'react';
import { Card, CardContent } from './ui/card';
import { BookmarkIcon } from 'lucide-react';

export const SavedQueries = () => {
  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center gap-2 text-sm text-gray-600 font-medium pl-1">
        <BookmarkIcon size={14} />
        <span>Saved Queries</span>
      </div>
      
      <div className="space-y-1.5">
        <Card className="border-none shadow-none bg-sage-50 hover:bg-sage-100 cursor-pointer">
          <CardContent className="p-2 text-sm">How to optimize manufacturing processes</CardContent>
        </Card>
        <Card className="border-none shadow-none bg-sage-50 hover:bg-sage-100 cursor-pointer">
          <CardContent className="p-2 text-sm">Best practices for equipment maintenance</CardContent>
        </Card>
      </div>
    </div>
  );
};
