# 🚀 Spike AI BuildX Hackathon: Analytics & SEO Intelligence Backend

A robust **Python-based backend system** that unifies **GA4 analytics** and **technical SEO intelligence** into a single, intelligent API. Built with an agent-based architecture, it bridges the gap between natural language intent and deterministic data execution.

---

## 🧠 System Overview

This backend exposes a single endpoint `POST /query` that intelligently routes requests to specialized agents. By combining **LLM-assisted query planning** with **deterministic execution**, the system ensures 100% accuracy based on real datasets—eliminating the risk of LLM hallucinations.

### 🏗️ Architecture Flow

```mermaid
graph TD
    A[POST /query] --> B{Orchestrator}
    B -->|propertyId present| C[GA4 Analytics Agent]
    B -->|SEO Query| D[SEO Intelligence Suite]
    D --> E[Accessibility Agent - WCAG]
    D --> F[Response Codes Agent - Health]
    D --> G[Indexability Agent - Technical SEO]
    C & E & F & G --> H[Human-Readable Insights + Structured Data]
✨ Key Features
📊 Tier 1: GA4 Analytics Agent
Engine: Uses Google Analytics Data API.

Function: Converts natural language into structured GA4 query plans.

Metrics: Active users, sessions, events, and pageviews.

Reliability: Handles empty/low-traffic properties gracefully with clear error states.

🔍 Tier 2: SEO Intelligence (Screaming Frog Data)
Derived from real crawl data stored in Google Sheets:

Accessibility (WCAG) Agent: Detects WCAG 2.2 AA violations, computes compliance risk, and summarizes fixes.

Crawl Health Agent: Classifies URLs (200, 3xx, 4xx, 5xx), identifies robots.txt blocks, and evaluates technical risks.

Indexability Agent: Analyzes Meta Robots and X-Robots-Tag to compute indexability percentages and overall SEO health (Good/Average/Poor).

📡 API Usage
Endpoint: POST /query

1. GA4 Analytics
JSON

{
  "query": "Give me active users in the last 7 days",
  "propertyId": "YOUR_GA4_PROPERTY_ID"
}
2. SEO Health & Accessibility
JSON

{
  "query": "Are there any WCAG 2.2 accessibility issues on the site?"
}
// OR
{
  "query": "Analyze response codes and crawl health"
}
⚙️ Setup & Deployment (Evaluator Guide)
This project is optimized for automated evaluation and strictly follows the hackathon execution requirements.

✅ Prerequisites
Port: Application binds to 8080.

Credentials: A credentials.json (Google Service Account) must be placed in the root directory.

Structure: Ensure deploy.sh is in the root.

🚀 One-Step Deployment
Run the following command from the repository root:

Bash

bash deploy.sh
The script creates a .venv, installs dependencies, and starts the server at http://localhost:8080.

🧪 Validation & Testing
Standalone scripts are provided to validate individual agent logic (requires valid credentials):

test_ga4.py — GA4 API connectivity.

test_accessibility_agent.py — WCAG logic.

test_indexability_agent.py — SEO Health logic.

test_list_sheet.py — Google Sheets connectivity.

📄 Assumptions & Constraints
Data Integrity: Assumes Screaming Frog sheets follow the standard export structure (internal_all, accessibility_all, etc.).

Security: Credentials are handled via Service Account; no manual OAuth flow required.

LLM Role: The LLM is used strictly for intent classification and query mapping, not for data generation.

🎥 Demo Highlights
Unified Endpoint: One API for both Analytics and SEO.

Deterministic Accuracy: Every insight is backed by raw crawl or API data.

Orchestration: Seamless routing based on user intent.

👨‍💻 Author
Harshit Shrivastava Participant - Spike AI BuildX Hackathon
```
