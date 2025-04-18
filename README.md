# 🕷️ Web Crawler with LLM Analysis

A full-stack web application that performs intelligent web crawling and AI-powered content analysis using a Large Language Model (LLM).

## 📌 Overview

This project consists of a backend service for crawling web pages and performing LLM-driven analysis, and a frontend web interface for interacting with the crawler and visualizing the extracted insights.

The system allows users to input a website URL, crawl its pages, and receive structured insights such as:
* Summary of the content
* Sentiment analysis
* Categorization
* Extracted metadata & links

The LLM model (such as LLaMA2) is used locally via Ollama for powerful and privacy-respecting analysis.

## 🏗️ Project Structure

```
web-crawler-with-llm/
│
├── web-crawler-backend/   # FastAPI backend for crawling, analysis & database
├── web-crawler-frontend/  # Next.js frontend for user interaction
└── README.md              # You're here!
```

Each folder contains its own README with detailed setup instructions:
* 🔧 **Backend README**: [web-crawler-backend/README.md](https://github.com/DeathRay99/web-crawler-with-llm/blob/master/web-crawler-backend/README.md)
* 🎨 **Frontend README**: [web-crawler-frontend/README.md](https://github.com/DeathRay99/web-crawler-with-llm/blob/master/web-crawler-frontend/README.md)

## 🧠 Technologies Used

* **Backend**: FastAPI, PostgreSQL (NeonDB), asyncio, crawl4ai, Ollama, LLaMA2
* **Frontend**: React, Next.js
* **AI Analysis**: LLaMA2 via Ollama
* **Deployment Ready**: Can be deployed locally or on cloud with minor changes

## 🚀 Getting Started

1. Clone this repo:

```bash
git clone https://github.com/DeathRay99/web-crawler-with-llm.git
cd web-crawler-with-llm
```

2. Set up and run backend and frontend by following instructions in their respective folders:
   * [Backend Setup Guide](https://github.com/DeathRay99/web-crawler-with-llm/tree/master/web-crawler-backend)
   * [Frontend Setup Guide](https://github.com/DeathRay99/web-crawler-with-llm/tree/master/web-crawler-frontend)
