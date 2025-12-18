🧠 Spike AI BuildX Hackathon — Analytics & SEO Intelligence Backend
Overview

This project is a Python-based backend system built for the Spike AI BuildX Hackathon.
It provides a unified /query API that can answer GA4 analytics questions and technical SEO questions using real datasets.

The system is designed with agent-based architecture, deterministic data execution, and human-readable insights.

🚀 Features
Tier 1 — GA4 Analytics Agent

Fetches real Google Analytics 4 data

Supports metrics like active users, sessions, events

Uses Google Analytics Data API

Gracefully handles empty datasets

Tier 2 — SEO Agents (Screaming Frog Data)
Accessibility SEO Agent

Analyzes accessibility_all worksheet

Detects WCAG 2.2 AA violations

Reports percentage of URLs with accessibility risks

Provides compliance-focused explanations

Response Codes SEO Agent

Analyzes response_codes_all worksheet

Classifies URLs into:

200 OK

3xx Redirects

Blocked by robots.txt

4xx / 5xx errors

Evaluates crawl health and technical SEO risks

🏗️ Architecture
POST /query
|
v
Orchestrator
|
|-- GA4 Analytics Agent (if propertyId exists)
|
|-- SEO Accessibility Agent (WCAG)
|
|-- SEO Response Codes Agent

LLM is used only for GA4 query planning

SEO execution is fully deterministic

No hallucinated data

Real Google Sheets + GA4 APIs only

📡 API Usage
GA4 Query
POST /query
{
"query": "Give me active users last 7 days",
"propertyId": "YOUR_GA4_PROPERTY_ID"
}

SEO Accessibility Query
POST /query
{
"query": "Are there WCAG 2.2 accessibility issues on the site?"
}

SEO Response Codes Query
POST /query
{
"query": "Are there any response code or crawl issues?"
}

⚙️ Setup Instructions

1. Create virtual environment
   python -m venv .venv
   .venv\Scripts\activate # Windows

2. Install dependencies
   pip install -r requirements.txt

3. Add credentials

Place credentials.json (Google Service Account) in project root

Enable:

Google Analytics Data API

Google Sheets API

4. Run server
   python -m uvicorn app.main:app --port 8080

🔐 Security Notes

API keys and credentials are never committed

.gitignore excludes secrets

Deterministic execution prevents hallucination

🏁 Conclusion

This project demonstrates:

Real-world analytics integration

Agent-based AI architecture

Safe LLM usage

Practical SEO intelligence

Production-grade robustness
