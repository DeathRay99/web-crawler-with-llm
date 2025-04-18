"use client";
import { useState, useEffect } from "react";
import {
  Eye,
  ExternalLink,
  Calendar,
  Share2,
  Tag,
  Home,
  MessageSquare,
} from "lucide-react";
import { useParams } from "next/navigation";
import Summary from "@/components/Summary";
import Insights from "@/components/Insights";
import Metadata from "@/components/Metadata";
import Links from "@/components/Links";
import Content from "@/components/Content";
import Link from "next/link";

export default function PageDetails() {
  const params = useParams();
  const id = params?.id;
  const [page, setPage] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!id) return;

    async function fetchPageData() {
      try {
        setLoading(true);
        const response = await fetch(`http://127.0.0.1:8000/api/page/${id}`);

        if (!response.ok) {
          throw new Error(`Error: ${response.status}`);
        }

        const data = await response.json();
        setPage(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchPageData();
  }, [id]);

  if (loading)
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-xl">Loading...</div>
      </div>
    );
  if (error)
    return (
      <div className="bg-red-50 p-4 rounded-md text-red-700 text-center">
        {error}
      </div>
    );
  if (!page) return null;

  // Parse insights from string to array if needed
  const insights =
    typeof page.insights === "string"
      ? JSON.parse(page.insights)
      : page.insights;

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <div className="fixed top-6 right-40 z-50">
        <Link
          href="/"
          className="group relative text-gray-600 hover:text-black"
        >
          <Home size={24} />
          <span className="absolute left-full ml-2 bottom-1/2 translate-y-1/2 hidden group-hover:inline-block text-xs bg-black text-white px-2 py-1 rounded shadow">
            Go to Home
          </span>
        </Link>
      </div>
      {/* Header section */}
      <div className="mb-8">
        <div className="flex items-center gap-2 text-sm text-gray-500 mb-2">
          <Calendar size={16} />
          <span>Crawled at: {new Date(page.crawled_at).toLocaleString()}</span>
        </div>

        <h1 className="text-3xl font-bold mb-2">{page.title}</h1>

        <div className="flex items-center gap-2 mb-4">
          <a
            href={page.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800 flex items-center gap-1"
          >
            {page.url}
            <ExternalLink size={16} />
          </a>
        </div>

        <div className="flex flex-wrap gap-4 text-sm">
          <div className="flex items-center gap-1 bg-gray-100 px-3 py-1 rounded-full">
            <Eye size={16} />
            <span>ID: {page.id}</span>
          </div>

          {page.category && (
            <div className="flex items-center gap-1 bg-blue-100 px-3 py-1 rounded-full">
              <Tag size={16} />
              <span>{page.category}</span>
            </div>
          )}

          {page.sentiment && (
            <div className="flex items-center gap-1 bg-green-100 px-3 py-1 rounded-full">
              <MessageSquare size={16} />
              <span>Sentiment: {page.sentiment}</span>
            </div>
          )}
        </div>
      </div>

      {/* Main content */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-2">
          {/* Content section */}
          <Content content={page.content} />

          {/* Links section   */}
          {page.links && <Links links={page.links} />}
        </div>

        <div className="md:col-span-1">
          {/* Summary section */}
          <Summary summary={page.summary} />

          {/* Insights section */}
          {insights && insights.length > 0 && <Insights insights={insights} />}

          {/* Metadata section */}
          {page.metadata && <Metadata metadata={page.metadata} />}
        </div>
      </div>
    </div>
  );
}
