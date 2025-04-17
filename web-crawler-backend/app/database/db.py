import os
from datetime import datetime
from typing import Dict, List, Optional
import json
import asyncpg
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv()

class CrawledPage(BaseModel):
    """Model for a crawled web page"""
    id: Optional[int] = None
    url: str
    title: str
    metadata: Dict
    content: str
    links: Dict
    crawled_at: datetime
    
    # LLM analysis results
    summary: Optional[str] = None
    category: Optional[str] = None
    sentiment: Optional[str] = None
    insights: Optional[str] = None

class Database:
    """Database handler for NeonDB PostgreSQL"""
    def __init__(self):
        self.conn_pool = None
        self.db_url = os.getenv("DATABASE_URL")
    
    async def connect(self):
        """Connect to the database and create a connection pool"""
        try:
            self.conn_pool = await asyncpg.create_pool(
                dsn=self.db_url,
                ssl="require" if "sslmode=require" in self.db_url else None
            )
            
            # Create tables if they don't exist
            await self._create_tables()
        except Exception as e:
            print(f"Database connection error: {e}")
            raise
        
    async def _create_tables(self):
        """Create necessary database tables"""
        async with self.conn_pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS crawled_pages (
                    id SERIAL PRIMARY KEY,
                    url TEXT NOT NULL UNIQUE,
                    title TEXT NOT NULL,
                    metadata JSONB,
                    content TEXT,
                    links JSONB,
                    crawled_at TIMESTAMP,
                    summary TEXT,
                    category TEXT,
                    sentiment TEXT,
                    insights TEXT
                )
            ''')
    
    async def ensure_connection(self):
        """Ensure database connection is established"""
        if self.conn_pool is None:
            await self.connect()
    
    async def store_crawled_data(self, pages: List[Dict]) -> List[int]:
        """Store crawled pages in the database"""
        await self.ensure_connection()
        page_ids = []
        
        async with self.conn_pool.acquire() as conn:
            for page in pages:
                # Check if page already exists
                existing = await conn.fetchval(
                    'SELECT id FROM crawled_pages WHERE url = $1',
                    page['url']
                )
                
                if existing:
                    page_ids.append(existing)
                    continue
                
                # Convert ISO datetime string to datetime object if needed
                crawled_at = page['crawled_at']
                if isinstance(crawled_at, str):
                    crawled_at = datetime.fromisoformat(crawled_at)

                 # ✅ Convert dict/list to JSON string
                metadata_json = json.dumps(page['metadata'])
                links_json = json.dumps(page['links'])

                # Insert new page
                page_id = await conn.fetchval('''
                    INSERT INTO crawled_pages (url, title, metadata, content, links, crawled_at)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    RETURNING id
                ''', 
                page['url'], 
                page['title'], 
                metadata_json, 
                page['content'], 
                links_json, 
                crawled_at
                )
                
                page_ids.append(page_id)
        
        return page_ids
    
    async def update_with_analysis(self, page_id: int, analysis: Dict) -> bool:
        """Update page with LLM analysis results"""
        await self.ensure_connection()
        insights = analysis.get('insights', [])
        if isinstance(insights, list):
            insights = json.dumps(insights)

        async with self.conn_pool.acquire() as conn:
            await conn.execute('''
                UPDATE crawled_pages
                SET summary = $1, category = $2, sentiment = $3, insights = $4
                WHERE id = $5
            ''',
            analysis.get('summary', ''),
            analysis.get('category', ''),
            analysis.get('sentiment', ''),
            insights,
            page_id
            )
        return True
    
    async def get_page(self, page_id: int) -> Optional[CrawledPage]:
        """Get a single page by ID"""
        await self.ensure_connection()
        async with self.conn_pool.acquire() as conn:
            row = await conn.fetchrow(
                'SELECT * FROM crawled_pages WHERE id = $1',
                page_id
            )
            
            if row:
                return CrawledPage(
                    id=row['id'],
                    url=row['url'],
                    title=row['title'],
                    metadata=json.loads(row['metadata']) if isinstance(row['metadata'], str) else row['metadata'],
                    content=row['content'],
                    links=json.loads(row['links']) if isinstance(row['links'], str) else row['links'],
                    crawled_at=row['crawled_at'],
                    summary=row['summary'],
                    category=row['category'],
                    sentiment=row['sentiment'],
                    insights=row['insights']
                )
            return None
            
    async def get_pages(self, limit: int = 20, offset: int = 0) -> List[CrawledPage]:
        """Get multiple pages with pagination"""
        await self.ensure_connection()
        results = []
        async with self.conn_pool.acquire() as conn:
            rows = await conn.fetch(
                'SELECT * FROM crawled_pages ORDER BY crawled_at DESC LIMIT $1 OFFSET $2',
                limit, offset
            )
            
            for row in rows:
                results.append(CrawledPage(
                    id=row['id'],
                    url=row['url'],
                    title=row['title'],
                    metadata=row['metadata'],
                    content=row['content'],
                    links=row['links'],
                    crawled_at=row['crawled_at'],
                    summary=row['summary'],
                    category=row['category'],
                    sentiment=row['sentiment'],
                    insights=row['insights']
                ))
                
        return results