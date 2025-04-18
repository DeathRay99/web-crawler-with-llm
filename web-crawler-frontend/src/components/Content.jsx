import React from "react";
import ReactMarkdown from "react-markdown";

function Content({content}) {
  return (
    <div className="bg-white shadow rounded-lg p-6 mb-6">
      <h2 className="text-xl font-semibold mb-4">Content</h2>
      <div className="prose max-w-none">
        <ReactMarkdown>{content}</ReactMarkdown>
      </div>
    </div>
  );
}

export default Content;
