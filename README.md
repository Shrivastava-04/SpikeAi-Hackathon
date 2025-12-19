# 🚀 Spike AI BuildX Hackathon

## Analytics & SEO Intelligence Backend

A **Python-based backend system** built for the **Spike AI BuildX Hackathon** that answers **GA4 analytics** and **technical SEO questions** through a **single unified API**.

The system uses an **agent-based architecture**, combining **deterministic execution** with **LLM-assisted query planning** to ensure **accuracy, safety, and explainability**.

---

## 🧠 What This Project Does

This backend exposes a single API endpoint:

```
POST /query
```

It intelligently routes natural language questions to:

- **GA4 Analytics Agent** (when `propertyId` is provided)
- **SEO Intelligence Agents** (using real Screaming Frog Google Sheets data)

✅ All answers are computed from **real datasets only**  
🚫 No hallucinated or fabricated insights

---

## ✨ Key Features

### 🔹 Tier 1 — GA4 Analytics Agent

- Uses **Google Analytics Data API**
- Converts natural language questions into **structured GA4 query plans**
- Supports metrics such as:
  - Active users
  - Sessions
  - Events
  - Pageviews
- Handles:
  - Empty GA4 responses
  - Low-traffic properties
- Returns:
  - Structured analytics output
  - Human-readable explanation

---

### 🔹 Tier 2 — SEO Intelligence (Screaming Frog Data)

SEO insights are derived from **real Screaming Frog crawl data** stored in **Google Sheets**.

#### ♿ Accessibility SEO Agent (WCAG)

- Reads the `accessibility_all` worksheet
- Detects **WCAG 2.2 AA violations**
- Computes:
  - Violation counts
  - Risk indicators
- Produces **human-readable accessibility summaries**

---

#### 🌐 Response Codes SEO Agent

- Reads the `response_codes_all` worksheet
- Classifies URLs into:
  - `200 OK`
  - `3xx Redirects`
  - `Blocked by robots.txt`
  - `4xx / 5xx` errors
- Evaluates:
  - Crawl health
  - Technical SEO risks

---

#### 🔍 Indexability SEO Agent

- Reads the `internal_all` worksheet
- Determines indexability using:
  - Status codes
  - Meta Robots
  - X-Robots-Tag
- Computes:
  - Percentage of indexable pages
  - Technical SEO health classification:
    - **Good / Average / Poor**
- Produces **derived SEO insights**, not raw counts

---

## 🏗️ System Architecture

```
POST /query
   |
   v
Orchestrator
   |
   |-- GA4 Analytics Agent (if propertyId exists)
   |
   |-- Accessibility SEO Agent (WCAG)
   |
   |-- Response Codes SEO Agent
   |
   |-- Indexability SEO Agent
```

---

## 📡 API Usage

### 📊 GA4 Analytics Query

```json
POST /query
{
  "query": "Give me active users in the last 7 days",
  "propertyId": "GA4_PROPERTY_ID"
}
```

---

### ♿ Accessibility SEO Query

```json
POST /query
{
  "query": "Are there any WCAG 2.2 accessibility issues on the site?"
}
```

---

### 🌐 Response Codes / Crawl Health Query

```json
POST /query
{
  "query": "Analyze response codes and crawl health"
}
```

---

### 🔍 Indexability SEO Query

```json
POST /query
{
  "query": "Calculate the percentage of indexable pages and assess SEO health"
}
```

---

## ⚙️ Setup Instructions (Evaluator Ready)

### ✅ Strict Execution Requirements

- Server binds **only to port 8080**
- `deploy.sh` exists at repository root
- `credentials.json` exists at repository root  
  _(Evaluators will replace this file during evaluation)_
- **`.env` file exist at repository root with environment variable as given below** -`LLM_API_KEY` -`LLM_BASE_URL` -`SEO_AGENT_SHEET_ID` -`GA4_PROPERTY_ID`

- Virtual environment created as `.venv`
- Startup completes within **7 minutes**
- No manual intervention required

---

### 🚀 One-Step Deployment

From repository root:

```bash
bash deploy.sh
```

The server will start on:

```
http://localhost:8080
```

---

## 🔐 Credentials Handling (Important)

- **environment variables must be there in `.env` file**
- **The environment variable names are listed below:** -`LLM_API_KEY` -`LLM_BASE_URL` -`SEO_AGENT_SHEET_ID` -`GA4_PROPERTY_ID`
- `credentials.json` **must be present at project root**
- It contains a **Google Service Account**
- Used for:
  - GA4 authentication
  - Google Sheets access
- **Evaluators will replace this file with their own credentials**

---

## 🧪 Testing & Validation

Standalone test scripts are included for development and validation:

- `test_ga4.py`
- `test_accessibility_agent.py`
- `test_response_codes_agent.py`
- `test_indexability_agent.py`
- `test_list_sheet.py`

These tests:

- Validate individual agents
- Are **not auto-executed**
- Require valid Google credentials

---

## 📄 Assumptions & Limitations

### Assumptions

- GA4 property contains valid traffic data
- Service account has access to GA4 and Google Sheets
- Screaming Frog sheet structure remains consistent

### Limitations

- SEO intent routing is rule-based (LLM optional – Tier-3)
- No write-back to GA4 or Google Sheets
- Focus is on **analysis and insights**, not automated fixes

---

## 🏁 Conclusion

This project demonstrates:

- Clean agent-based backend architecture
- Safe and controlled LLM usage
- Real GA4 analytics integration
- Practical technical SEO intelligence
- Production-aligned execution constraints

Built specifically to meet and exceed the **Spike AI BuildX Hackathon** requirements.

---

## 🙌 Author

**Harshit Shrivastava**  
Spike AI BuildX Hackathon Participant
