
import React from 'react';
import { Sidebar } from '@/components/Sidebar';
import { ArticleCard } from '@/components/ArticleCard';
import { SearchBar } from '@/components/SearchBar';
import { NewTab } from '@/components/NewTab';
import { SavedQueries } from '@/components/SavedQueries';
import { Logo } from '@/components/Logo';
import { Footer } from '@/components/Footer';

const Index = () => {
  const featuredArticles = [
    {
      title: 'How Data Fuels The Move To Smart Manufacturing',
      description: 'Digital transformation is critical to ensuring a positive outcome in manufacturing and design. Here are four ways data and AI get the job done.'
    },
    {
      title: 'How To Handle Breakdown During Production'
    },
    {
      title: 'Reduce Downtime For Meeting High Demand'
    },
    {
      title: 'Leading With Innovation In Smart Factories'
    }
  ];

  return (
    <div className="flex h-screen bg-white">
      <Sidebar />
      
      <div className="flex-1 flex flex-col overflow-auto">
        <header className="p-4 border-b flex justify-between items-center">
          <Logo />
        </header>
        
        <main className="flex flex-1">
          <div className="w-3/4 p-6 overflow-y-auto">
            <div className="mb-12 flex flex-col items-center justify-center py-12">
              <div className="text-6xl mb-6 text-sage-500 font-light">
                <span>(</span>
                <span className="text-sage-400">*</span>
                <span>)</span>
              </div>
              <h1 className="text-2xl font-medium text-gray-700 mb-8">Discover Infinite Wisdom</h1>
            </div>
            
            <div className="mb-10">
              <div className="grid grid-cols-2 gap-4">
                {featuredArticles.map((article, index) => (
                  <ArticleCard 
                    key={index}
                    title={article.title}
                    description={article.description}
                  />
                ))}
              </div>
            </div>
            
            <div className="mt-8 w-full max-w-xl mx-auto">
              <SearchBar />
            </div>
          </div>
          
          <div className="w-1/4 border-l p-4 bg-gray-50">
            <div className="space-y-6">
              <NewTab />
              <SavedQueries />
            </div>
          </div>
        </main>
        
        <Footer />
      </div>
    </div>
  );
};

export default Index;
