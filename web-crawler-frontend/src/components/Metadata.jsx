import React from "react";

function Metadata({metadata}) {
  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-4">Metadata</h2>
      <dl className="space-y-2">
        {Object.entries(metadata).map(([key, value]) => (
          <div key={key}>
            <dt className="text-sm font-medium text-gray-500">{key}</dt>
            <dd className="text-gray-700 break-words">{value || "-"}</dd>
          </div>
        ))}
      </dl>
    </div>
  );
}

export default Metadata;
