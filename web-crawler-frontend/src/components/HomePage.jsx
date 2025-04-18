import React from 'react';
import { Globe, Search, Brain, FileText } from 'lucide-react';
import DomainInputForm from './DomainInputForm';

function HomePage() {
  return (
    <div className="max-w-4xl mx-auto py-4 px-4">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-blue-600 mb-4">Welcome to Web Crawler</h1>
        <p className="text-xl text-gray-600">Crawl, analyze, and extract insights from any website</p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-8 mb-12">
        <h2 className="text-2xl font-semibold mb-6">How It Works</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="flex flex-col items-center text-center">
            <div className="bg-blue-100 p-4 rounded-full mb-4">
              <Globe className="h-8 w-8 text-blue-600" />
            </div>
            <h3 className="font-medium mb-2">Enter Domain</h3>
            <p className="text-gray-600 text-sm">Input any website domain you want to analyze</p>
          </div>
          
          <div className="flex flex-col items-center text-center">
            <div className="bg-green-100 p-4 rounded-full mb-4">
              <Search className="h-8 w-8 text-green-600" />
            </div>
            <h3 className="font-medium mb-2">Crawl Pages</h3>
            <p className="text-gray-600 text-sm">Our system crawls and extracts content from the website</p>
          </div>
          
          <div className="flex flex-col items-center text-center">
            <div className="bg-purple-100 p-4 rounded-full mb-4">
              <Brain className="h-8 w-8 text-purple-600" />
            </div>
            <h3 className="font-medium mb-2">AI Analysis</h3>
            <p className="text-gray-600 text-sm">LLM analyzes content for sentiment, categories and insights</p>
          </div>
          
          <div className="flex flex-col items-center text-center">
            <div className="bg-amber-100 p-4 rounded-full mb-4">
              <FileText className="h-8 w-8 text-amber-600" />
            </div>
            <h3 className="font-medium mb-2">View Results</h3>
            <p className="text-gray-600 text-sm">Browse comprehensive analysis and extracted insights</p>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-2xl font-semibold mb-6">Start Crawling</h2>
        <p className="mb-6 text-gray-600">Enter a domain to begin crawling and analysis:</p>
        
        <DomainInputForm/>
        
        <p className="mt-4 text-sm text-gray-500">
          Note: Crawling and analysis may take a few minutes depending on the size of the website.
        </p>
      </div>
    </div>
  );
}

export default HomePage;