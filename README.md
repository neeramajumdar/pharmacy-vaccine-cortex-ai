# pharmacy-vaccine-cortex-ai
An end-to-end data engineering and conversational AI pipeline built to analyze customer experience (CX) operational bottlenecks during COVID-19 vaccine distribution.
# 🏥 Retail Pharmacy Vaccine CX Analytics & Snowflake Cortex AI Pipeline

An end-to-end data engineering and conversational AI pipeline built to analyze customer experience (CX) operational bottlenecks during COVID-19 vaccine distribution. 

This project demonstrates how combining **Snowflake SQL transformations**, **dbt Semantic Modeling**, and **Snowflake Cortex Analyst AI** turns unstructured and structured survey data into self-service conversational analytics for non-technical business leaders.

---

## 🎯 Business Problem & Context
During high-volume COVID-19 vaccine rollouts, retail pharmacy operations experienced significant appointment no-shows, leading to vaccine spoilage and missed access opportunities. 

Marketing and operational leadership issued customer experience surveys, but lacked rapid, ad-hoc reporting capabilities. This pipeline was built to:
1. Identify the root causes of vaccine appointment no-shows.
2. Evaluate preferred customer remedies to drive attendance.
3. Provide operational CX managers with a **Self-Service Natural Language Query (Text-to-SQL)** interface via Snowflake Cortex AI.

---

## 🏗️ Technical Architecture & Pipeline Flow

┌───────────────────────────┐      ┌───────────────────────────┐
│  Python Data Generator    │ ───> │  Snowflake Internal Stage │
│  (1k Synthetic Records)   │      │  (CSV Data Ingestion)     │
└───────────────────────────┘      └─────────────┬─────────────┘
│
▼
┌───────────────────────────┐      ┌───────────────────────────┐
│ dbt / YAML Semantic Layer │ <─── │ Snowflake SQL Modeling    │
│ (Metrics, Synonyms, Joins)│      │ (Staging Views & Facts)   │
└─────────────┬─────────────┘      └───────────────────────────┘
│
▼
┌───────────────────────────┐      ┌───────────────────────────┐
│ Snowflake Cortex Analyst  │ ───> │ Interactive Streamlit UI  │
│ (Constrained Text-to-SQL) │      │ (Self-Service Dashboard)  │
└───────────────────────────┘      └───────────────────────────┘


1. **Synthetic Data Generation:** Python script simulating patient appointments, reminder delivery flags, channel types, and unstructured survey comments.
2. **Data Modeling:** Snowflake SQL staging views (`stg_vaccine_appointments`) and dimensional fact models (`fct_vaccine_enriched`).
3. **Semantic Governance:** dbt `semantic_models.yml` defining business metrics (e.g., `noshow_rate`, `popup_adoption_rate`), dimensions, and entity keys.
4. **AI & Self-Service Interface:** Snowflake Cortex Analyst translating natural language questions into accurate SQL executed via a Streamlit web interface.

---

## 🔑 Key Strategic Insights Uncovered
* **28% of No-Shows Were Avoidable:** The primary root cause of missed appointments was a total lack of automated reminder notifications (SMS/Email/Phone).
* **High-Impact Operations Pivots:** Top customer remedies identified were automated multi-channel reminder opt-ins and **localized community pop-up clinics** near high-risk stores.

---

## 📂 Repository Structure

```text
├── data/
│   └── raw_pharmacy_vaccine_data.csv    # Generated synthetic dataset
├── sql/
│   ├── 01_snowsight_setup.sql            # DB, Schema, Stage, & Copy Into commands
│   ├── 02_staging_views.sql             # SQL transformation & cleaning logic
│   └── 03_fact_cortex_enrichment.sql    # Native Snowflake Cortex LLM functions
├── dbt/
│   └── models/
│       └── semantic_models.yml          # YAML Semantic Layer blueprint
├── app/
│   ├── cortex_analyst_engine.py         # Text-to-SQL API wrapper
│   └── app_pharmacy.py                  # Streamlit self-service UI
├── generate_data.py                     # Python synthetic data script
├── README.md                            # Project documentation
└── requirements.txt                     # Python dependencies
🛠️ How to Run This Project Locally
Prerequisites
Python 3.9+

Snowflake Account with Cortex AI enabled

Streamlit & Snowflake Connector

Quickstart
Clone the repository:

Bash
git clone [https://github.com/your-username/pharmacy-vaccine-cortex-ai.git](https://github.com/your-username/pharmacy-vaccine-cortex-ai.git)
cd pharmacy-vaccine-cortex-ai
Install dependencies:

Bash
pip install -r requirements.txt
Generate synthetic dataset:

Bash
python generate_data.py
Execute SQL scripts in Snowsight: Run sql/01_snowsight_setup.sql through sql/03_fact_cortex_enrichment.sql in order.

Launch the Streamlit app:

Bash
streamlit run app/app_pharmacy.py

---

### 💻 Step-by-Step: How to Add Your Files to GitHub

<Sequence>

  <Step subtitle="Installs Git software if not already present on your system" title="Step 1: Install Git & Create GitHub Account">
1. Download and install Git from [git-scm.com](https://git-scm.com/).
2. Create a free account on [GitHub.com](https://github.com) if you do not have one.
  </Step>

  <Step subtitle="Sets up the online storage repository on GitHub" title="Step 2: Create a New Repository on GitHub">
1. Log into GitHub and click the **`+`** icon in the top-right corner $\rightarrow$ select **New repository**.
2. **Repository name:** `pharmacy-vaccine-cortex-ai`
3. **Description:** `Retail Pharmacy Vaccine CX Analytics using Snowflake Cortex AI & dbt Semantic Models.`
4. Set visibility to **Public** *(recruiters need to see it without logging in)*.
5. Uncheck "Add a README file" *(since you will push your own)*.
6. Click **Create repository**.
  </Step>

  <Step subtitle="Organizes project scripts and documents into clean folders" title="Step 3: Organize Your Local Folder Structure">
On your computer inside `C:\Users\neera\support_ticket_pipeline` (or your local project folder), organize your files like this:

* Create a file named `README.md` and paste the template above into it.
* Put your Python generator file in the root folder (`generate_data.py`).
* Create a folder named `sql/` and save your Snowsight `.sql` scripts there.
* Create a folder named `dbt/` and save your `semantic_models.yml` file there.
* Create a file named `requirements.txt` containing:
  ```text
  pandas
  streamlit
  google-genai
  duckdb
PowerShell
# 1. Initialize local git repository
git init

# 2. Add all files to staging
git add .

# 3. Create your first commit
git commit -m "Initial commit: Added Snowflake Cortex AI pharmacy pipeline code and README"

# 4. Set the main branch
git branch -M main

# 5. Link local folder to your GitHub repository (replace URL with your repository link)
git remote add origin https://github.com/your-username/pharmacy-vaccine-cortex-ai.git

# 6. Upload files to GitHub
git push -u origin main
