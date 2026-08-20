# 🇮🇳 PlacementIndia Job Scraper — India's Top Job Board Data Extractor

[![Apify Badge](https://img.shields.io/badge/Apify-Actor-00D4FF?style=flat-square)](https://apify.com)
[![Python Badge](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green?style=flat-square)](https://opensource.org/licenses/Apache-2.0)

Extract structured job listings from **PlacementIndia.com** — India's leading job portal connecting 1 Crore+ job seekers with 6 Lakh+ verified employers. Perfect for job aggregators, recruitment platforms, market research, and **AI agents** powered by Claude, ChatGPT, and MCP protocols.

---

## 🎯 Features

✅ **Comprehensive Job Data** — Title, company, location, salary, experience, skills, job description  
✅ **Multi-Location Support** — Search jobs across all Indian cities (Delhi, Mumbai, Bangalore, etc.)  
✅ **Advanced Filtering** — By industry, job type, salary range, experience level  
✅ **No Login Required** — Scrape publicly available job listings without authentication  
✅ **Rate Limit Friendly** — Respects server resources with smart delays  
✅ **MCP Compatible** — Seamlessly integrates with Claude Desktop and AI automation workflows  
✅ **JSON Export** — Clean, structured output ready for databases and analytics  

---

## 📊 Output Format

Each job listing returns the following structured data:

| Field | Type | Description |
|-------|------|-------------|
| `jobTitle` | String | Job position title |
| `companyName` | String | Hiring company name |
| `location` | String | Job location (city, state) |
| `salary` | String | Salary range (if available) |
| `experience` | String | Required experience level |
| `skills` | Array | Required skills/technologies |
| `jobDescription` | String | Full job description |
| `jobUrl` | String | Direct link to job posting |
| `postedDate` | String | When the job was posted |
| `applicants` | String | Number of applicants (if shown) |
| `jobType` | String | Full-time, Part-time, Contract, etc. |

### Example Output

```json
{
  "jobTitle": "Senior Python Developer",
  "companyName": "Tech Solutions India Pvt Ltd",
  "location": "Bangalore, Karnataka",
  "salary": "₹8-12 LPA",
  "experience": "3-5 years",
  "skills": ["Python", "Django", "REST API", "PostgreSQL", "AWS"],
  "jobDescription": "We are looking for an experienced Python developer...",
  "jobUrl": "https://www.placementindia.com/job/python-developer-12345",
  "postedDate": "2 days ago",
  "applicants": "25 applicants",
  "jobType": "Full-time"
}
```

---

## 🚀 Quick Start

### Run on Apify Platform

```bash
apify call [your-username]/placementindia-scraper --input '{
  "searchKeyword": "python developer",
  "location": "Bangalore",
  "maxJobs": 50
}'
```

### Input Parameters

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `searchKeyword` | String | No | Job title or skill to search | `""` |
| `location` | String | No | City/state to filter jobs | `"All India"` |
| `maxJobs` | Integer | No | Maximum jobs to scrape | `100` |
| `experienceLevel` | String | No | Filter: Fresher, 1-3 years, 3-5 years, 5+ years | `"All"` |
| `industry` | String | No | Filter by industry (IT, Banking, Healthcare, etc.) | `"All"` |
| `jobType` | String | No | Full-time, Part-time, Contract, Internship | `"All"` |

---

## 🤖 AI Integration — Claude, ChatGPT & MCP

### Use with Claude Desktop (MCP Protocol)

Add this actor to your Claude Desktop `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": ["-y", "@apify/mcp-server"],
      "env": {
        "APIFY_API_TOKEN": "your_apify_token"
      }
    }
  }
}
```

**Example Claude Prompt:**
```
"Find me all Python developer jobs in Mumbai with 3+ years experience from PlacementIndia"
```

Claude will automatically:
1. Call this Apify Actor with the right parameters
2. Parse the job listings
3. Present you with a clean summary and actionable insights

---

### Use with ChatGPT (GPT Actions)

Configure this actor as a GPT Action in ChatGPT:

```yaml
openapi: 3.0.0
info:
  title: PlacementIndia Job Scraper
  version: 1.0.0
servers:
  - url: https://api.apify.com/v2
paths:
  /acts/[your-username]/placementindia-scraper/runs:
    post:
      operationId: scrapeJobs
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                searchKeyword:
                  type: string
                location:
                  type: string
                maxJobs:
                  type: integer
```

**Example ChatGPT Prompt:**
```
"Get the latest data science jobs in Pune with salaries above ₹10 LPA"
```

---

### Use with Make.com / Zapier

**Make.com:**
1. Add "Apify" module
2. Select "Run Actor"
3. Choose `placementindia-scraper`
4. Map input fields from previous steps
5. Use output in Google Sheets, Airtable, or email notifications

**Zapier:**
1. Search for "Apify" in Zapier
2. Trigger: Schedule (daily job alerts)
3. Action: Run Apify Actor → `placementindia-scraper`
4. Filter: Only jobs matching your criteria
5. Send to Slack, email, or CRM

---

## 💡 Use Cases

| Use Case | Description |
|----------|-------------|
| 🔍 **Job Aggregation** | Build a meta job board by combining data from multiple sources |
| 📊 **Market Research** | Analyze hiring trends, salary ranges, and skill demand in India |
| 🤖 **AI Resume Matching** | Feed job data to Claude/ChatGPT to match candidates with roles |
| 📧 **Job Alerts** | Auto-notify users when jobs matching their profile are posted |
| 🏢 **Recruitment Analytics** | Track competitor hiring, industry growth, and talent gaps |
| 📱 **Mobile Apps** | Power job search features in mobile applications |

---

## 🛠️ Technical Details

- **Language:** Python 3.11+
- **Libraries:** `requests`, `beautifulsoup4`, `apify-client`
- **Rate Limiting:** 1-2 second delay between requests
- **Error Handling:** Automatic retries on network failures
- **Data Validation:** Ensures all fields are properly formatted

---

## 📖 FAQ

**Q: Do I need a PlacementIndia account?**  
A: No, this scraper only accesses public job listings.

**Q: How often should I run this actor?**  
A: Daily for fresh job alerts, weekly for market research.

**Q: Can I scrape specific companies?**  
A: Yes, use the `searchKeyword` field with the company name.

**Q: Is this legal?**  
A: Yes, we only scrape publicly available data. Always review PlacementIndia's Terms of Service.

**Q: How do I handle large datasets?**  
A: Increase `maxJobs` or run multiple searches in parallel with different filters.

---

## 🔗 Related Actors

- [Naukri.com Scraper](https://apify.com/store) — India's largest job portal
- [LinkedIn Jobs Scraper](https://apify.com/store) — Professional networking jobs
- [Indeed India Scraper](https://apify.com/store) — Global job aggregator

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/placementindia-scraper/issues)
- **Documentation:** [Apify Docs](https://docs.apify.com)
- **Community:** [Apify Discord](https://discord.gg/apify)

---

## 📄 License

Apache 2.0 — Free for commercial and personal use.

---

**Built with ❤️ for India's job market | Optimized for Claude AI, ChatGPT, and MCP workflows**
