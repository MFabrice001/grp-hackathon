# 🇷🇼 Rwanda GRB Resource Discovery Platform
**Team Name:** [Insert Your Team Name Here]
**Repository:** `team-[name]-gdrh-2026`

## 🎯 Project Objective
To bridge the data visibility gap for Civil Society Organizations (CSOs) in Rwanda by providing a centralized, searchable, and AI-powered catalog of Gender Responsive Budgeting (GRB) resources, datasets, and surveys.

## 👤 User Persona
**CSO Policy Advocate:** Working at the district level (e.g., Musanze). They need localized, intersectional data (Urban vs. Rural, Male vs. Female) to write evidence-based policy briefs but struggle to navigate fragmented NISR and MIGEPROF databases.

## 🔄 Key Workflows
1. **Discover:** Users search the catalog (Tab 1) by keyword, year, or organization.
2. **Analyze:** Users visualize intersectional resource allocation via the Analytics Dashboard (Tab 2).
3. **Advocate:** Users generate an automated, AI-driven Policy Brief based on specific district and sector parameters (Tab 3).

## 🛠️ Setup Steps & Run Command
1. Clone this repository.
2. Create a virtual environment: `python3 -m venv venv` and activate it.
3. Install dependencies: `pip install -r requirements.txt`
4. Add your `.env` file with `GROQ_API_KEY=your_key_here`.
5. **Run Command:** `streamlit run app.py`

## ⚠️ Limitations
* The AI Assistant relies on the Groq free tier API limits.
* Datasets mapped in `studies.csv` currently link out to external portals; direct microdata downloads are restricted by NISR policies.
* Charts require datasets to have specific column names (Gender, Location).

## 🚀 Next Steps
* Integrate directly with the existing Gender Data Lab API.
* Expand the AI to automatically scrape and summarize PDF reports.

## 🔗 Data Provenance & Usage
| Resource | Source URL | Access Time | Status | Notes / Restrictions |
| :--- | :--- | :--- | :--- | :--- |
| NISR Microdata Catalog | `https://microdata.statistics.gov.rw/` | March 20, 2026 | Open / Restricted | Some DTA files require specific institution login requests. |
| FAST Project Context | Internal GIZ/FAST Briefing | March 20, 2026 | Open | Used for scoping Intersectionality metrics. |

---
*Submitted for the FAST GRB Resource Discovery Challenge - 2026*