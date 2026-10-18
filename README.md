# 🧠 CueCard Custom Intelligence Harvester

> **Automated Multi-Source Content Research & Market Intelligence Pipeline**

`cuecard_custom_harvester.py` is an enterprise-grade Python automation engine designed to extract, synthesize, and structure real-time digital trends into client-ready Excel databases. By tapping directly into Wikipedia, DuckDuckGo, YouTube auto-suggest matrices, Reddit community threads, and Google News RSS feeds, this script replaces manual content research with automated execution.

---

## ⚡ End-to-End Workflow Process

1. **Target Ingestion:** Reads target seed topics and handles from an automated text queuing file (`keywords_input.txt`).
2. **Multi-Source Scraping & API Extraction:**
   * **Context Abstracts:** Pulls clean summaries via Wikipedia REST APIs & DuckDuckGo fallback.
   * **Search Intent:** Harvesters capture live search auto-suggest keywords from YouTube.
   * **Social Video Discovery:** Extracts live YouTube video links, Instagram Reels, and Facebook Watch feeds via targeted RSS/XML proxies.
   * **Community & News Pulse:** Gathers active Reddit discussion threads and breaking news headlines.
   * **Audience Hooks:** Generates high-click comparison prompts (`vs`) and common audience inquiries (`why/how`).
3. **Structured Excel Generation:**
   * Utilizes `pandas` and `openpyxl` to build beautifully styled spreadsheets.
   * Features custom dark header formatting, zebra striping, dynamic column auto-resizing, and clickable hyperlink formulas.
4. **Historical Database Sync:**
   * Automatically updates a two-sheet workbook (`Latest Data` and `Historic Data`).
   * Eliminates duplicate records and sorts entries chronologically by timestamp.
5. **Auto-Reset:** Clears input queues post-run to maintain continuous batch processing.

---

## 🎯 Target Clients & Problems Solved

This automation script is engineered specifically to address operational bottlenecks for:

### 1. Media Houses & Pop-Culture News Networks
* **Problem:** Journalists spend 15+ hours weekly manually tracking breaking news across Reddit, Google News, and social media.
* **Solution:** Automates breaking news and community sentiment harvesting into a central dashboard updated in seconds.

### 2. YouTube & Short-Form Content Creators (Shorts / Reels / TikTok)
* **Problem:** Finding viral hooks, comparison angles ("X vs Y"), and audience questions takes longer than recording content.
* **Solution:** Delivers ready-to-script comparison hooks, live competitor video links, and audience inquiry prompts automatically.

### 3. Digital Marketing & SEO Agencies
* **Problem:** Conducting keyword research and indexing live social mentions across multiple platforms is tedious and error-prone.
* **Solution:** Generates structured client reports complete with formatted Excel styling and actionable intent metrics.

---

## 🛠️ Customization & Client Services Offered

We offer fully customized Python automation and data pipeline setups tailored to your agency or business workflow:

* **Custom Platform Connectors:** Integration with additional platforms (LinkedIn, Twitter/X, Quora, Pinterest, Amazon, eBay).
* **Automated Scheduling:** Cloud deployment (AWS / GitHub Actions / Cron) to run pipeline reports daily or hourly automatically to email/Slack.
* **Custom Output Schemas:** Custom branding, color schemes, PDF exports, or direct database connections (PostgreSQL, Airtable, Notion, Google Sheets API).
* **AI Integration:** OpenAI / Gemini API integration for automated script generation, viral title scoring, and text summarization directly inside the spreadsheet.

---

## 🚀 How to Run Locally

### Prerequisites
```bash
pip install pandas requests openpyxl
