# Web Crawler & LLM Analyzer

A web crawler with LLM-based analysis capabilities.

## Overview

This application uses a web crawler to fetch web pages and stores the crawled data in a database. It also utilizes a Large Language Model (LLM) to analyze the crawled pages and extract insights.

## Features

* Web crawling using `crawl4ai`
* Database storage using NeonDB PostgreSQL
* LLM analysis using Ollama
* Insights extraction and storage
* Backend API using FastAPI

## Requirements

* Python 3.8+
* FastAPI
* asyncpg
* pydantic
* nltk
* rich

## Steps to Run

1. Clone the repository: `git clone https://github.com/DeathRay99/web-crawler-with-llm.git`

2. Install ollama locally. You can download the latest version from the [Ollama Website](https://ollama.ai/). After downloading, open a terminal and run the command: `ollama run llama2`. This will download the LLaMA2 model (approximately 5GB) and start serving it. We need LLaMA2 because we are using it for LLM analysis.

3. Navigate to the root directory (web-crawler-backend) and create a virtual environment:
   On Windows: `python -m venv venv`
   On Linux/Mac: `python3 -m venv venv`
   Then, activate the virtual environment:
   On Windows: `venv\Scripts\activate`
   On Linux/Mac: `source venv/bin/activate`

4. Install dependencies: `pip install -r requirements.txt`

5. Sign up on NeonDB, create a new project, and copy the connection string on which should be in the following format: `postgresql://<username>:<password>@<project_id>.postgres.neon.tech/<database>?sslmode=require`. Set this connection string as an environment variable in the .env file, e.g. `DATABASE_URL=postgresql://<username>:<password>@<project_id>.postgres.neon.tech/<database>?sslmode=require`

6. Run the application: `uvicorn app.main:app --host 127.0.0.1 --port 8000 --loop asyncio`

## API Endpoints

* `/api/crawl`: Trigger a crawl job and after crawling does the llm analysis (summary, sentiment, category, insights) then stores final result to db.
* `/api/page/{page_id}`: Get a single crawled page by ID.
* `/api/pages/list`: Get a list of all crawled pages (just ID and title).

