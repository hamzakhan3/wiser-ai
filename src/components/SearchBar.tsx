import React, { useState } from 'react';
import { Input } from './ui/input';
import { ArrowRight } from 'lucide-react';
import { Button } from './ui/button';
import { useNavigate } from 'react-router-dom';
import { sendQuery } from '@/services/apiService';
import { toast } from '@/hooks/use-toast';

export const SearchBar = () => {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setIsLoading(true);
    try {
      // First, try to send the query to the backend with source identifier
      await sendQuery(query, 'discover-page');
      
      // If successful, navigate to the chat page with the query
      navigate(`/chat?q=${encodeURIComponent(query)}`);
    } catch (error) {
      console.error('Failed to process query:', error);
      toast({
        title: "Backend Connection Error",
        description: "Could not connect to the backend service. Please try again later.",
        variant: "destructive"
      });
      
      // Even if the backend call fails, still navigate to the chat page
      navigate(`/chat?q=${encodeURIComponent(query)}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative flex items-center w-full">
      <Input 
        className="pr-10 bg-sage-50 border-none focus-visible:ring-sage-200 text-gray-600 placeholder:text-gray-400"
        placeholder="Ask away!" 
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        disabled={isLoading}
      />
      <Button 
        type="submit"
        size="icon" 
        variant="ghost" 
        className="absolute right-1 text-sage-500 hover:text-sage-700 hover:bg-transparent"
        disabled={isLoading}
      >
        <ArrowRight size={18} />
      </Button>
    </form>
  );
};
