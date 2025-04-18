# Web Crawler Frontend

This is the frontend repository for the Web Crawler application, built using Next.js and React. It's a web application that allows users to crawl, analyze, and extract insights from any website. The application is designed to be user-friendly and provide a seamless experience for users.

The application takes in a website domain as input and crawls the website, extracting content in the form of text, images, and other data. The extracted content is then analyzed using a large language model (LLM) to extract insights such as sentiment, categories, and more. The results are then presented to the user in a comprehensive and easy-to-understand format.

## Table of Contents

* [Getting Started](#getting-started)
* [Features](#features)
* [API Documentation](#api-documentation)

## Getting Started

To run the application, follow these steps:

1. Clone the repository: `git clone https://github.com/DeathRay99/web-crawler-with-llm.git`
2. Navigate to root directory for frontend (web-crawler-frontend) & Install dependencies: `npm install` or `yarn install`
3. Start the development server: `npm run dev` or `yarn dev`

## Features

* Provide a user-friendly input field for users to enter website domains they wish to crawl
* Display real-time updates on the status of the crawling process to keep users informed
* Allow users to view detailed information and insights about the pages that have been crawled previously
* Display detailed information about each crawled page, including the page title, content, internal and external links discovered, timestamp of the crawl, metadata, and AI-powered analysis such as sentiment, summary, insights, and category.

## API Documentation

The API documentation can be found in the [API repository](https://github.com/DeathRay99/web-crawler-with-llm/tree/master/web-crawler-backend).

