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

It intelligently routes natural language queries to:

- **GA4 Analytics Agent** (when `propertyId` is provided)
- **SEO Intelligence Agents** (using real Screaming Frog Google Sheets data)

✅ All answers are generated from **real datasets** —  
🚫 No hallucinated or fabricated insights.

---

## ✨ Key Features

### 🔹 Tier 1 — GA4 Analytics Agent

- Uses **Google Analytics Data API**
- Converts natural language questions into **structured GA4 queries**
- Supports metrics like:
  - Active users
  - Sessions
  - Events
- Gracefully handles:
  - Empty datasets
  - Low-traffic properties

---

### 🔹 Tier 2 — SEO Intelligence (Screaming Frog Data)

#### ♿ Accessibility SEO Agent (WCAG)

- Reads the `accessibility_all` worksheet
- Detects **WCAG 2.2 AA violations**
- Reports:
  - Compliance risk
  - Violation percentages
- Produces **human-readable accessibility insights**

---

#### 🌐 Response Codes SEO Agent

- Reads the `response_codes_all` worksheet
- Classifies URLs into:
  - `200 OK`
  - `3xx Redirects`
  - Blocked by `robots.txt`
  - `4xx / 5xx` errors
- Evaluates:
  - Crawl health
  - Technical SEO risks

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

```

### Design Principles

- LLMs are used **only for query planning**
- LLMs **never execute analytics logic**
- All insights are computed **deterministically**
- Uses **real APIs and datasets only**
  - GA4
  - Google Sheets (Screaming Frog)

---

## 📡 API Usage

### 📊 GA4 Analytics Query

```json
POST /query
{
  "query": "Give me active users for the last 7 days",
  "propertyId": "YOUR_GA4_PROPERTY_ID"
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
  "query": "Are there any response code or crawl issues?"
}
```

---

## ⚙️ Setup Instructions

### 1️⃣ Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Add Google Credentials

Place `credentials.json` (Google Service Account) in the **project root**.

Enable the following APIs in **Google Cloud Console**:

- Google Analytics Data API
- Google Sheets API

⚠️ `credentials.json` is intentionally **not committed** for security reasons.

---

### 4️⃣ Run the Server

```bash
python -m uvicorn app.main:app --port 8080
```

Server runs at:

```
http://127.0.0.1:8080
```

---

## 🧪 Testing

This repository includes **standalone test scripts** for development and validation:

- `test_ga4.py`
- `test_accessibility_agent.py`
- `test_response_codes_agent.py`
- `test_list_sheet.py`

These tests:

- Validate individual agents
- Are **not executed automatically**
- Require **valid Google credentials** to run

---

## 🔐 Security & Best Practices

- No secrets or API keys are committed
- GA4 `propertyId` is supplied dynamically via API request
- `.gitignore` excludes:

  - Credentials
  - Virtual environments
  - Cache files

- Deterministic execution prevents hallucinated insights

---

## 🏁 Conclusion

This project demonstrates:

- Agent-based backend architecture
- Safe and controlled LLM usage
- Real-world GA4 analytics integration
- Practical SEO intelligence using Screaming Frog data
- Production-grade robustness and explainability

Built specifically to align with the **Spike AI BuildX Hackathon** problem statement.

---

## 🙌 Author

**Harshit Shrivastava**
Spike AI BuildX Hackathon Participant
