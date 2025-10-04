
import React from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './ui/card';
import { useNavigate } from 'react-router-dom';
import { sendQuery } from '@/services/apiService';
import { toast } from '@/hooks/use-toast';

type ArticleCardProps = {
  title: string;
  description?: string;
  stats?: {
    views?: number;
    comments?: number;
    likes?: number;
  };
  compact?: boolean;
};

export const ArticleCard = ({ title, description, compact = false }: ArticleCardProps) => {
  const navigate = useNavigate();

  const handleClick = async () => {
    try {
      // Send the article title as a query to the backend
      await sendQuery(title);
      
      // Navigate to the chat page with the title as a query parameter
      navigate(`/chat?q=${encodeURIComponent(title)}`);
    } catch (error) {
      console.error('Failed to process article query:', error);
      toast({
        title: "Backend Connection Error",
        description: "Could not connect to the backend service. Continuing anyway.",
        variant: "destructive"
      });
      
      // Still navigate even if the API call fails
      navigate(`/chat?q=${encodeURIComponent(title)}`);
    }
  };

  return (
    <Card 
      className={`border shadow-sm hover:shadow-md transition-shadow cursor-pointer ${compact ? 'h-28' : ''}`}
      onClick={handleClick}
    >
      <CardHeader className={`${compact ? 'p-3' : 'p-4'}`}>
        <CardTitle className={`${compact ? 'text-sm' : 'text-lg'}`}>{title}</CardTitle>
        {description && !compact && (
          <CardDescription className="text-sm line-clamp-2">{description}</CardDescription>
        )}
      </CardHeader>
    </Card>
  );
};
