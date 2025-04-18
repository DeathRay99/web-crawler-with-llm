"use client"

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { FileText, Loader } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function Sidebar() {
  const [pages, setPages] = useState([]);
  const [loading, setLoading] = useState(true);
//   const router = useRouter();
//   const currentPageId = router.query.id;

  useEffect(() => {
    async function fetchPages() {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/pages/list');
        
        if (response.ok) {
          const data = await response.json();
          setPages(data);
        }
      } catch (err) {
        console.error("Error fetching pages:", err);
      } finally {
        setLoading(false);
      }
    }

    fetchPages();
  }, []);

  return (
    <div className="w-64 bg-white border-r h-full overflow-y-auto">
      <div className="p-4">
        <h2 className="text-lg font-semibold mb-4">Recently Crawled Pages</h2>
        
        {loading ? (
          <div className="flex justify-center py-4">
            <Loader className="animate-spin text-blue-500" size={24} />
          </div>
        ) : (
          <ul className="space-y-2">
            {pages.length === 0 ? (
              <p className="text-gray-500 text-sm">No pages found</p>
            ) : (
              pages.map(page => (
                <li key={page.id}>
                  <Link href={`/crawledPage/${page.id}`}>
                    <div className="flex items-center p-2 rounded-md hover:bg-gray-100 text-gray-700">
                      <FileText size={16} className="mr-2 flex-shrink-0" />
                      <span className="text-sm truncate">{page.title}</span>
                    </div>
                  </Link>
                </li>
              ))
            )}
          </ul>
        )}
      </div>
    </div>
  );
}