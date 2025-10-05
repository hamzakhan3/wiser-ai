
import React, { useEffect, useState } from 'react';
import { Sidebar } from '@/components/Sidebar';
import { Logo } from '@/components/Logo';
import { Footer } from '@/components/Footer';
import { useSearchParams } from 'react-router-dom';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { SendIcon, ArrowLeft, User, Bot } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { sendQuery, QueryResponse, streamResponse } from '@/services/apiService';
import { toast } from '@/hooks/use-toast';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { ChartContainer } from '@/components/Chart';
import type { ReactNode } from 'react';

interface Message {
  role: 'user' | 'system';
  content: string;
  format?: 'markdown' | 'text';
  chartData?: any;
  statusChart?: any;
  asciiChart?: string;
  chartType?: string;
  id?: string;
  isStreaming?: boolean;
  cursor?: string;
}

const ChatPage = () => {
  const [searchParams] = useSearchParams();
  const initialQuery = searchParams.get('q') || '';
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    if (initialQuery) {
      setMessages([{ role: 'user', content: initialQuery }]);
      
      // Send the initial query to the backend
      handleQueryBackend(initialQuery);
    }
  }, [initialQuery]);

  const handleQueryBackend = async (query: string) => {
    setIsLoading(true);
    
    // Add a placeholder message for streaming
    const messageId = Date.now().toString();
    setMessages(prev => [
      ...prev, 
      { 
        role: 'system', 
        content: '',
        id: messageId,
        isStreaming: true
      }
    ]);
    
    try {
      let streamedContent = '';
      
      await streamResponse(
        query,
        // onChar callback
        (char: string) => {
          streamedContent += char;
          setMessages(prev => 
            prev.map(msg => 
              msg.id === messageId 
                ? { ...msg, content: streamedContent }
                : msg
            )
          );
        },
        // onCursor callback
        (cursor: string) => {
          setMessages(prev => 
            prev.map(msg => 
              msg.id === messageId 
                ? { ...msg, cursor: cursor }
                : msg
            )
          );
        },
        // onComplete callback
        () => {
          setMessages(prev => 
            prev.map(msg => 
              msg.id === messageId 
                ? { ...msg, isStreaming: false, cursor: '' }
                : msg
            )
          );
          setIsLoading(false);
        }
      );
    } catch (error) {
      console.error('Error streaming response:', error);
      
      // Fallback to regular query if streaming fails
      try {
        const response = await sendQuery(query, 'chat-page');
        
        setMessages(prev => [
          ...prev.filter(msg => msg.id !== messageId),
          { 
            role: 'system', 
            content: response.response || "I'm sorry, I couldn't process that request.",
            format: response.format || 'markdown',
            chartData: response.chart_data,
            statusChart: response.status_chart,
            asciiChart: response.ascii_chart,
            chartType: response.chart_type
          }
        ]);
      } catch (fallbackError) {
        console.error('Error with fallback query:', fallbackError);
        
        toast({
          title: "Backend Error",
          description: "Failed to get a response from the backend. Using simulated response instead.",
          variant: "destructive"
        });
        
        // Final fallback to simulated response
        setMessages(prev => [
          ...prev.filter(msg => msg.id !== messageId),
          { 
            role: 'system', 
            content: `Here's some information about "${query}". This is a simulated response as this is a prototype or the backend is unavailable.`,
            format: 'markdown'
          }
        ]);
      }
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    
    const userQuery = input.trim();
    setInput('');
    
    // Add user message immediately
    setMessages(prev => [...prev, { role: 'user', content: userQuery }]);
    
    // Process with backend
    await handleQueryBackend(userQuery);
  };

  return (
    <div className="flex h-screen bg-white">
      <Sidebar />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="p-4 border-b flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Button 
              variant="ghost" 
              size="icon" 
              className="mr-1" 
              onClick={() => navigate('/')}
            >
              <ArrowLeft size={18} />
            </Button>
            <Logo />
          </div>
        </header>
        
        <main className="flex-1 overflow-y-auto p-4 bg-gray-50">
          <div className="max-w-4xl mx-auto space-y-6">
            {messages.map((message, index) => (
              <div key={index} className="flex gap-4 items-start">
                {/* Avatar */}
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                  message.role === 'user' ? 'bg-sage-500 text-white' : 'bg-gray-600 text-white'
                }`}>
                  {message.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                </div>
                
                {/* Message Content */}
                <div className="flex-1 min-w-0">
                  <div className="mb-1">
                    <span className="text-sm font-medium text-gray-700">
                      {message.role === 'user' ? 'You' : 'Assistant'}
                    </span>
                  </div>
                  
                  <div className="prose prose-sm max-w-none prose-gray">
                    {message.role === 'system' && message.format === 'markdown' ? (
                      <ReactMarkdown 
                        remarkPlugins={[remarkGfm]}
                        components={{
                          // Custom styling for tables
                          table: ({ children }) => (
                            <div className="overflow-x-auto my-4">
                              <table className="min-w-full border-collapse border border-gray-300">
                                {children}
                              </table>
                            </div>
                          ),
                          th: ({ children }) => (
                            <th className="border border-gray-300 px-4 py-2 bg-gray-50 text-left font-semibold">
                              {children}
                            </th>
                          ),
                          td: ({ children }) => (
                            <td className="border border-gray-300 px-4 py-2">
                              {children}
                            </td>
                          ),
                          // Better bullet points
                          ul: ({ children }) => (
                            <ul className="list-disc pl-6 space-y-1 my-3">
                              {children}
                            </ul>
                          ),
                          ol: ({ children }) => (
                            <ol className="list-decimal pl-6 space-y-1 my-3">
                              {children}
                            </ol>
                          ),
                          li: ({ children }) => (
                            <li className="text-gray-700">
                              {children}
                            </li>
                          ),
                          // Code blocks
                        code({ inline, className, children, ...props }: { inline?: boolean; className?: string; children: ReactNode }) {
                        return inline ? (
                          <code className="bg-gray-100 px-1 py-0.5 rounded text-sm font-mono text-gray-800" {...props}>
                            {children}
                          </code>
                        ) : (
                          <code className="block bg-gray-100 p-3 rounded-lg text-sm font-mono text-gray-800 overflow-x-auto" {...props}>
                            {children}
                          </code>
                        );
                      },
                          // Headings
                          h1: ({ children }) => (
                            <h1 className="text-xl font-bold text-gray-900 mt-6 mb-3">
                              {children}
                            </h1>
                          ),
                          h2: ({ children }) => (
                            <h2 className="text-lg font-semibold text-gray-900 mt-5 mb-2">
                              {children}
                            </h2>
                          ),
                          h3: ({ children }) => (
                            <h3 className="text-md font-semibold text-gray-900 mt-4 mb-2">
                              {children}
                            </h3>
                          ),
                          // Paragraphs
                          p: ({ children }) => (
                            <p className="text-gray-700 leading-relaxed mb-3">
                              {children}
                            </p>
                          ),
                        }}
                      >
                        {message.content}
                        {message.isStreaming && message.cursor && (
                          <span className="animate-pulse text-blue-500">{message.cursor}</span>
                        )}
                      </ReactMarkdown>
                    ) : (
                      <p className="text-gray-700 leading-relaxed">
                        {message.content}
                        {message.isStreaming && message.cursor && (
                          <span className="animate-pulse text-blue-500">{message.cursor}</span>
                        )}
                      </p>
                    )}
                    
                    {/* Render Charts if available */}
                    {(message.chartData || message.statusChart || message.asciiChart) && (
                      <ChartContainer 
                        chartData={message.chartData}
                        statusChart={message.statusChart}
                        asciiChart={message.asciiChart}
                      />
                    )}
                  </div>
                </div>
              </div>
            ))}
            
            {isLoading && !messages.some(msg => msg.isStreaming && msg.content) && (
              <div className="flex gap-4 items-start">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                    <span className="text-sm text-gray-500">Thinking...</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </main>
        
        <div className="p-4 border-t bg-white">
          <form onSubmit={handleSubmit} className="flex gap-2 max-w-4xl mx-auto">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message here..."
              className="flex-1"
              disabled={isLoading}
            />
            <Button 
              type="submit" 
              className="bg-sage-500 hover:bg-sage-600"
              disabled={isLoading}
            >
              <SendIcon size={18} />
            </Button>
          </form>
        </div>
        
        <Footer />
      </div>
    </div>
  );
};

export default ChatPage;