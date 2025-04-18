"use client"
import React, { useState } from 'react';
import { Loader, AlertCircle, CheckCircle } from 'lucide-react';

function DomainInputForm() {
  const [domain, setDomain] = useState('');
  const [loading, setLoading] = useState(false);
  const [alert, setAlert] = useState({ show: false, type: '', message: '' });

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!domain) {
      setAlert({
        show: true,
        type: 'error',
        message: 'Please enter a domain to crawl'
      });
      return;
    }

    // Format the domain if needed
    let formattedDomain = domain;
    if (!domain.startsWith('http://') && !domain.startsWith('https://')) {
      formattedDomain = `https://${domain}`;
    }

    setLoading(true);
    setAlert({ show: false, type: '', message: '' });

    try {
      const response = await fetch('http://127.0.0.1:8000/api/crawl', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: formattedDomain,
          query_type: 'domain'
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setAlert({
          show: true,
          type: 'success',
          message: `Crawling completed! ${data.page_count} pages processed. You can now view the results.`
        });
        setDomain('');
        window.location.reload();
      } else {
        throw new Error(data.message || 'Something went wrong');
      }
    } catch (error) {
      setAlert({
        show: true,
        type: 'error',
        message: error.message
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="flex flex-col md:flex-row gap-4">
        <input 
          type="text" 
          value={domain}
          onChange={(e) => setDomain(e.target.value)}
          placeholder="e.g., example.com" 
          className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={loading}
        />
        <button 
          type="submit" 
          className={`px-6 py-2 rounded-md transition-colors flex items-center justify-center ${
            loading 
              ? 'bg-blue-400 cursor-not-allowed' 
              : 'bg-blue-600 hover:bg-blue-700 text-white'
          }`}
          disabled={loading}
        >
          {loading ? (
            <>
              <Loader className="animate-spin mr-2" size={18} />
              Crawling...
            </>
          ) : (
            'Start Crawling'
          )}
        </button>
      </form>

      {alert.show && (
        <div className={`p-4 rounded-md flex items-start ${
          alert.type === 'error' ? 'bg-red-50 text-red-700 border border-red-200' : 
          'bg-green-50 text-green-700 border border-green-200'
        }`}>
          <div className="flex-shrink-0 mr-2 mt-0.5">
            {alert.type === 'error' ? (
              <AlertCircle size={18} />
            ) : (
              <CheckCircle size={18} />
            )}
          </div>
          <div>
            <p>{alert.message}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default DomainInputForm;