from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from app.database.db import Database, CrawledPage
from app.llm.analyzer import OllamaAnalyzer
from uuid import uuid4
import subprocess
import json
import os
import sys

router = APIRouter()
db = Database()
analyzer = OllamaAnalyzer()


# Dependency to ensure DB connection
async def get_db():
    await db.ensure_connection()
    return db


# Request and Response Models
class CrawlRequest(BaseModel):
    query: str
    query_type: str = "domain"


class CrawlResponse(BaseModel):
    job_id: str
    message: str
    page_count: int = 0


class PageListItem(BaseModel):
    id: int
    title: str

class PageResponse(BaseModel):
    pages: List[CrawledPage]
    total: int

class CrawlerTestResponse(BaseModel):
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None


@router.post("/crawl", response_model=CrawlResponse)
async def start_crawl(request: CrawlRequest, database: Database = Depends(get_db)):
    job_id = str(uuid4())

    try:
        if request.query_type == "domain":
            crawler_response = await run_crawler_subprocess(request.query)

            if not crawler_response.success or not crawler_response.data:
                raise ValueError(f"Crawler failed: {crawler_response.error}")

            results = crawler_response.data
        else:
            print(f"Keyword crawling not implemented for: {request.query}")
            results = []

        page_ids = await database.store_crawled_data(results)

        for page_id in page_ids:
            page = await database.get_page(page_id)
            if page and page.content:
                analysis = analyzer.analyze_text(page.content, page.title, page.url)
                await database.update_with_analysis(page_id, analysis)

        return CrawlResponse(
            job_id=job_id,
            message=f"Crawling completed for {request.query_type}: {request.query}",
            page_count=len(page_ids)
        )

    except Exception as e:
        print(f"Error in crawl operation: {e}")
        return CrawlResponse(
            job_id=job_id,
            message=f"Error during crawl: {str(e)}",
            page_count=0
        )
    


# @router.get("/test-crawler/{domain}", response_model=CrawlerTestResponse)
async def run_crawler_subprocess(domain: str):
    """
    Run the crawler subprocess (in the crawler/ directory) as a standalone process.
    This function will run the crawler as a subprocess and wait for it to finish.
    It will return the JSON output of the crawler as a CrawlerTestResponse object.
    """
    try:
        # 1. Find the crawler script location
        crawler_script_path = os.path.join(os.path.dirname(__file__), "..", "crawler", "crawler.py")
        abs_path = os.path.abspath(crawler_script_path)
        
        # 2. Set up environment variables
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["CRAWL4AI_VERBOSE"] = "false"  # Suppress debug output
        
        # 3. Run the crawler subprocess
        result = subprocess.run(
            [sys.executable, abs_path, domain],
            capture_output=True,
            text=True,
            timeout=30,
            encoding="utf-8",
            env=env
        )

        # 4. Log output for debugging (if needed)
        if result.stderr:
            print(f"Crawler stderr: {result.stderr[:100]}...")
            
        # 5. Check if the crawler process succeeded
        if result.returncode != 0:
            return CrawlerTestResponse(
                success=False, 
                error=f"Crawler process failed with code {result.returncode}"
            )

        # 6. Extract and parse JSON from the output
        return extract_json_from_output(result.stdout)

    except subprocess.TimeoutExpired:
        return CrawlerTestResponse(success=False, error="Crawler timed out after 30 seconds")
    except Exception as e:
        return CrawlerTestResponse(success=False, error=f"Unexpected error: {str(e)}")

def extract_json_from_output(output: str) -> CrawlerTestResponse:
    """Extract JSON from possibly mixed output string"""
    try:
        json_start = output.find('{')
        if json_start >= 0:
            json_content = output[json_start:]
            data = json.loads(json_content)
            return CrawlerTestResponse(
                success=data.get("success", False),
                data=data.get("data"),
                error=data.get("error")
            )
    except Exception:
        pass  # Ignore if JSON parsing fails
    
    # No valid JSON found
    return CrawlerTestResponse(
        success=False, 
        error=f"Could not extract valid JSON from output: {output[:50]}..."
    )


@router.get("/pages", response_model=PageResponse)
async def get_pages(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    database: Database = Depends(get_db)
):
    pages = await db.get_pages(limit, offset)
    total = len(pages) + offset  # simplified
    return PageResponse(pages=pages, total=total)


@router.get("/page/{page_id}", response_model=CrawledPage)
async def get_page(page_id: int, database: Database = Depends(get_db)):
    page = await db.get_page(page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page

@router.get("/pages/list", response_model=List[PageListItem])
async def list_pages(database: Database = Depends(get_db)):
    """
    Get a list of all pages (just ID and title).
    """
    try:
        pages = await db.get_pages(limit=100)
        result = []
        for page in pages:
            item = PageListItem(id=page.id, title=page.title)
            result.append(item)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching pages list: {str(e)}")