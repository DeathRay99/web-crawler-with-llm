import asyncio
from typing import Dict, List
from datetime import datetime
import sys
import json
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig

class WebCrawler:
    def __init__(self):
        # No stored configuration or state that could cause issues between requests
        pass
        
    async def crawl_by_domain(self, domain: str) -> List[Dict]:
        """Simple domain crawl - just crawls the main page of the domain"""
        # Format domain for URL if needed
        if not domain.startswith("http"):
            domain = f"https://{domain}"
        
        # Create fresh configuration for each request
        browser_config = BrowserConfig(
            headless=True,
            use_persistent_context=False,
            verbose=False  
        )
        
        # Create the crawler with fresh configuration
        async with AsyncWebCrawler(config=browser_config) as crawler:
            try:
                # Crawl the main domain page
                result = await crawler.arun(
                    url=domain,
                    config=CrawlerRunConfig()
                )
                
                if result.success:
                    # Extract data using the metadata property
                    extracted_data = {
                        "url": domain,
                        "title": result.metadata.get("title", "No title available"),
                        "metadata": {
                            "description": result.metadata.get("description", ""),
                            "author": result.metadata.get("author", ""),
                            "keywords": result.metadata.get("keywords", ""),
                            "og:title": result.metadata.get("og:title", ""),
                            "og:description": result.metadata.get("og:description", ""),
                            "og:image": result.metadata.get("og:image", "")
                        },
                        "content": result.markdown,
                        "status_code": result.status_code,
                        "links": result.links,
                        "crawled_at": datetime.now().isoformat()
                    }
                    return [extracted_data]
                else:
                    print(f"Failed to crawl {domain}: Status code {result.status_code}")
                    return []
            except Exception as e:
                print(f"Error crawling {domain}: {str(e)}")
                return []

# subprocess-based usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python crawler.py <domain>\n")
        json_response = json.dumps({"success": False, "error": "Invalid arguments"})
        sys.stdout.write(json_response)
        sys.exit(1)

    domain = sys.argv[1]

    async def run():
        try:
            crawler = WebCrawler()
            result = await crawler.crawl_by_domain(domain)
            if result:
                # Use json.dumps once with the entire response
                json_response = json.dumps({"success": True, "data": result})
                sys.stdout.write(json_response)
            else:
                json_response = json.dumps({"success": False, "error": "No data returned from crawler."})
                sys.stdout.write(json_response)
        except Exception as e:
            # Catch any exceptions and return as JSON error
            json_response = json.dumps({"success": False, "error": f"Exception: {str(e)}"})
            sys.stdout.write(json_response)

    asyncio.run(run())
