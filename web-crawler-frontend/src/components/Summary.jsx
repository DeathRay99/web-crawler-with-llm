import React from "react";

function Summary({summary}) {
  return (
    <div className="bg-white shadow rounded-lg p-6 mb-6">
      <h2 className="text-xl font-semibold mb-4">Summary</h2>
      <p className="text-gray-700">{summary}</p>
    </div>
  );
}

export default Summary;
