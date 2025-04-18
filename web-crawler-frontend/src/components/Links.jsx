import React from 'react'
import {
    ExternalLink,
    Share2,
  } from "lucide-react";

function Links({links}) {
  return (
    <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Links</h2>

              {links.internal && links.internal.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-lg font-medium mb-2">Internal Links</h3>
                  <ul className="space-y-2">
                    {links.internal.map((link, index) => (
                      <li
                        key={`internal-${index}`}
                        className="flex items-start"
                      >
                        <div className="mr-2 mt-1 text-blue-600">
                          <Share2 size={14} />
                        </div>
                        <div>
                          <a
                            href={link.href}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:underline"
                          >
                            {link.text || link.href}
                          </a>
                          {link.base_domain && (
                            <span className="text-gray-500 text-sm ml-2">
                              ({link.base_domain})
                            </span>
                          )}
                        </div>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {links.external && links.external.length > 0 && (
                <div>
                  <h3 className="text-lg font-medium mb-2">External Links</h3>
                  <ul className="space-y-2">
                    {links.external.map((link, index) => (
                      <li
                        key={`external-${index}`}
                        className="flex items-start"
                      >
                        <div className="mr-2 mt-1 text-green-600">
                          <ExternalLink size={14} />
                        </div>
                        <div>
                          <a
                            href={link.href}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-green-600 hover:underline"
                          >
                            {link.text || link.href}
                          </a>
                          {link.base_domain && (
                            <span className="text-gray-500 text-sm ml-2">
                              ({link.base_domain})
                            </span>
                          )}
                        </div>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
  )
}

export default Links