import React from 'react'

function Insights({insights}) {
  return (
    <div className="bg-white shadow rounded-lg p-6 mb-6">
    <h2 className="text-xl font-semibold mb-4">Insights</h2>
    <ul className="space-y-3">
      {insights.map((insight, index) => (
        <li key={index} className="flex items-start">
          <div className="mr-2 text-indigo-600 font-bold">•</div>
          <p className="text-gray-700">{insight}</p>
        </li>
      ))}
    </ul>
  </div>
  )
}

export default Insights