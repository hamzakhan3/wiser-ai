import React, { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { ArrowRight } from 'lucide-react';

interface ChatPromptBarProps {
  onMessageSent: (message: string) => void;
  onTyping: (isTyping: boolean) => void;
  source?: string;
}

export const ChatPromptBar = ({ onMessageSent, onTyping, source = 'chat' }: ChatPromptBarProps) => {
  const [input, setInput] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setInput(value);
    onTyping(value.length > 0);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;
    
    console.log(`Message sent from source: ${source}`);
    onMessageSent(input.trim());
    setInput('');
    onTyping(false);
  };

  return (
    <div className="w-full max-w-xl mx-auto">
      <form onSubmit={handleSubmit} className="relative flex items-center w-full">
        <Input 
          className="pr-10 bg-sage-50 border-none focus-visible:ring-sage-200 text-gray-600 placeholder:text-gray-400"
          placeholder="Ask away!" 
          value={input}
          onChange={handleInputChange}
        />
        <Button 
          type="submit"
          size="icon" 
          variant="ghost" 
          className="absolute right-1 text-sage-500 hover:text-sage-700 hover:bg-transparent"
          disabled={!input.trim()}
        >
          <ArrowRight size={18} />
        </Button>
      </form>
    </div>
  );
};