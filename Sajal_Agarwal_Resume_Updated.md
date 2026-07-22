# SAJAL AGARWAL

Toronto, Ontario, Canada | sajal001@gmail.com | +1-437-218-0034
[linkedin.com/in/agarwalsajal](https://linkedin.com/in/agarwalsajal) | Portfolio: [sajalagarwal-ca.github.io/portfolio.github.io](https://sajalagarwal-ca.github.io/portfolio.github.io/)

---

## PROFESSIONAL SUMMARY

Results-driven Senior Data Scientist and Generative AI Engineer with 15+ years of experience in machine learning, statistical modeling, advanced analytics, and cloud data engineering. Proven track record deploying production ML models for **credit risk, insurance pricing, fraud detection, and cloud cost optimization**, including a flagship anomaly detection system that delivered **$12.8M CAD in annual savings** at Manulife. Deep expertise in Python, PostgreSQL, Microsoft Azure (ADF, Databricks, Azure OpenAI), and GenAI frameworks including LangChain, FAISS, RAG pipelines, and GPT-4. Experienced in translating complex model outputs into strategic business decisions for C-suite stakeholders. Actively maintains a public AI/ML project portfolio on GitHub.

---

## TECHNICAL SKILLS

| Area | Platforms / Tools |
| --- | --- |
| **Reporting & BI Tools** | Power BI, Tableau, Grafana, Qlik Sense, Advanced Excel, SSRS, MS Access, Cognos TM1 |
| **Cloud Platform** | Microsoft Azure (Azure Data Factory, Databricks, Azure OpenAI, Azure Functions) |
| **Databases** | PostgreSQL, MS SQL Server, MySQL, IBM Cognos TM1 |
| **Programming Tools** | Python, FastAPI, Streamlit, Flask, Visual Studio, Azure Data Studio, Databricks |
| **Languages** | Python, R, SQL |
| **ML / AI Frameworks** | Scikit-learn, XGBoost, Random Forest, Prophet, SMOTE, LangChain, FAISS, RAG Pipelines, GPT-4, HuggingFace |
| **Domains** | BFSI, Insurance, Healthcare, Retail, CPG, FMCG, Aviation |
| **Methodology / Tools** | Agile, Jira |

---

## PROFESSIONAL EXPERIENCE

### Data Scientist | Client: Manulife
**Tata Consultancy Services — Associate Consultant, Analytics & Insights**  *Jul 2020 – Present | Toronto, ON*

- **Delivered $12.8M CAD in annual savings** by designing and deploying a production ML-based outlier detection model that flagged underutilized Azure resources and excess cloud charges.
- Designed and deployed **end-to-end ML pipelines** for credit risk, insurance pricing, fraud detection, and cloud cost optimization, providing technical leadership across the full model lifecycle (development, validation, deployment, monitoring).
- Built **BI dashboards** in Grafana and Power BI on top of complex PostgreSQL queries to deliver reporting and analytics on Microsoft Azure daily consumption data.
- Automated Azure billing reporting via **Python scripts and Azure Functions**; implemented ETL pipelines in **Azure Data Factory** for daily data refreshes and database updates.
- Designed scalable, maintainable applications using **Python, FastAPI, Streamlit, and Flask on Databricks** for data processing and analytics.
- Applied feature engineering and data transformation using **Pandas, NumPy, and Seaborn** within Databricks notebooks for complex analytical workflows.
- Monitored model performance through KPI dashboards and presented actionable insights and recommendations to senior leadership.

#### Primary Projects at Manulife

**1. Cloud Cost Anomaly Detection & Optimization (Azure + Facebook Prophet)** — *Flagship project*
- Designed and deployed an **ML-based anomaly detection system on Azure** to identify abnormal cloud spending patterns at the cost-center level, delivering **$12.8M CAD in annual savings** at Manulife.
- Built a daily time-series forecasting model using **Facebook Prophet** to predict Azure charges and detect deviations from expected spend.
- Implemented automated email alerts to cost-center owners with resource-level breakdowns when actuals exceeded forecasted thresholds, enabling proactive remediation and improved cloud cost governance.
- GitHub: [github.com/Sajalagarwal-ca/Time-Series-Forecasting-via-meta-prophet-model](https://github.com/Sajalagarwal-ca/Time-Series-Forecasting-via-meta-prophet-model)

**2. Credit Risk Modeling — PD, LGD & Expected Credit Loss (XGBoost + Streamlit)**
- Built a **dual-output credit risk model using XGBoost** to simultaneously estimate **Probability of Default (PD)** and **Loss Given Default (LGD)**, and computed **Expected Credit Loss (ECL = PD × LGD × EAD)** at the borrower level.
- Engineered features from borrower credit, income, repayment history, and loan portfolio attributes; validated model with discrimination (AUC, KS) and calibration metrics suitable for IFRS 9 / Basel-aligned risk reporting.
- Deployed as an interactive **Streamlit application** enabling risk officers to score loans on-demand and explore ECL drivers.
- GitHub: [github.com/Sajalagarwal-ca/credit_risk_modeling](https://github.com/Sajalagarwal-ca/credit_risk_modeling) | Live Demo: [creditriskmodeling-dbvgyaavxuqjfbjtztxep5.streamlit.app](https://creditriskmodeling-dbvgyaavxuqjfbjtztxep5.streamlit.app/)

**3. Fraudulent Loan Application Detection (Random Forest + SMOTE)**
- Developed an **ML-based fraud detection system** for loan applications using borrower credit, income, and loan features; handled severe class imbalance with **SMOTE oversampling**.
- Achieved an **F1-score above 0.75** with a **Random Forest classifier** after hyperparameter tuning via GridSearchCV; identified **FICO score, debt-to-income ratio, and loan purpose** as top fraud indicators.
- Proposed ensemble model enhancements (Random Forest + Gradient Boosting) and a real-time inference architecture for production deployment.
- GitHub: [github.com/Sajalagarwal-ca/Fraudulent-Loan-Application-Detection-Project](https://github.com/Sajalagarwal-ca/Fraudulent-Loan-Application-Detection-Project)

**4. Health Care Insurance Premium Calculator (XGBoost + scikit-learn + Streamlit)**
- Built a robust ML system using **XGBoost and scikit-learn** to predict health insurance premiums based on age, medical history, lifestyle factors, and demographics.
- Performed end-to-end feature engineering, model selection, and hyperparameter tuning; evaluated with RMSE / MAE / R² and SHAP-based feature importance to ensure pricing explainability.
- Deployed as an **interactive Streamlit web application** allowing underwriters and customers to generate instant premium quotes.
- GitHub: [github.com/Sajalagarwal-ca/healthcare_premium_prediction](https://github.com/Sajalagarwal-ca/healthcare_premium_prediction) | Live Demo: [healthcarepremiumprediction-ufs9ahmsfgntfmn6lqrkvf.streamlit.app](https://healthcarepremiumprediction-ufs9ahmsfgntfmn6lqrkvf.streamlit.app/)

#### Generative AI Projects

**1. AI Travel Assistant (LangChain + Azure OpenAI + Streamlit)**
- Designed a conversational travel assistant providing itinerary planning and flight/hotel suggestions based on natural language prompts.
- Implemented LangChain for LLM orchestration with Azure OpenAI GPT models; integrated Google Places API for real-time data and PostgreSQL for user session history.

**2. Natural Language to SQL Query Engine (LangChain + PostgreSQL)**
- Built a natural language interface over PostgreSQL using LangChain's `create_sql_agent` with OpenAI GPT models, SQLAlchemy connections, and conversational memory for multi-turn sessions.
- Deployed a Streamlit front-end on Databricks for scalable NL-to-SQL inference with dynamic query generation and result visualization.
- GitHub: [github.com/Sajalagarwal-ca/langchain_query_NL_PostgreSQL_DB](https://github.com/Sajalagarwal-ca/langchain_query_NL_PostgreSQL_DB)

**3. Personal RAG Document Assistant (Streamlit + OpenAI + FAISS)**
- Built a local RAG pipeline ingesting multi-format documents (PDF, Word, Excel, CSV, TXT); chunked and embedded content via HuggingFace `all-MiniLM-L6-v2` with a FAISS vector store for fast semantic retrieval.
- Integrated OpenAI `gpt-4o-mini` for grounded answers with source file, page, chunk ID, and snippet references.
- GitHub: [github.com/Sajalagarwal-ca/RAG-Document-reader](https://github.com/Sajalagarwal-ca/RAG-Document-reader)

**4. Insurance Fraud Investigation Assistant (RAG-Based Claims Chatbot)**
- Developed a GenAI solution using **Azure OpenAI GPT-4** to summarize long insurance claim documents and surface anomalies based on historical fraud patterns.
- Combined structured (claims, transaction logs) and unstructured (text, emails, scanned PDFs) data using LangChain and FAISS embeddings.
- Built a Power BI dashboard to visualize detected anomalies and generate audit-ready fraud investigation summaries.

---

### Data Scientist | Client: Tata Steel
**Tata Consultancy Services — Assistant Consultant, Analytics & Insights**  *Jun 2019 – Jul 2020 | Kolkata, India*

- Identified patterns and applied statistical models to optimize operational efficiency of the mild steel door production process, improving production yield outcomes.
- Developed supervised and unsupervised ML models (regression, clustering, PCA) to analyze and diagnose production process deviations.
- Designed forecasting and classification models using multivariate regression, logistic regression, decision trees, and time-series analysis.
- Experimented with model pruning and quantization techniques to optimize real-time predictive maintenance models for edge deployment.
- Developed and maintained KPI dashboards for cross-functional teams, ensuring data analysis processes aligned with industry standards.

---

### Manager — Analytics
**GMR — Delhi International Airport Ltd.**  *Jul 2018 – Jun 2019 | New Delhi, India*

- Consolidated Management Reports for all airport terminals for Non-Aero Commercial reporting to CCO/CEO on Qlik Sense and Power BI.
- Designed data-driven campaigns and promotions generating **INR 2 Million in incremental revenue** across retail and F&B segments.

---

### Deputy Manager — Analytics
**WNS Global Services**  *Dec 2017 – Jul 2018 | Gurugram, India*

- Collaborated with clients and stakeholders across UK and USA in Healthcare and FMCG analytics verticals.
- Led a team of 5 analysts for financial and commercial reporting based on IMS/Nielsen/IRI published data on Power BI.
- Conducted sales and competitive landscape analysis to identify high-growth consumer healthcare product segments across SE Asia.
- Tracked and reported KPIs (Gross Sales, COGS, Net Sales, Operating Profit, Net Profit) from public financial data for FMCG companies.
- Generated market insights through secondary research covering consumer behavior, digital pricing, and market growth for the Indian FMCG industry.

---

## EDUCATION

| Qualification | Institution | Year | Grade |
| --- | --- | --- | --- |
| Bachelor of Engineering | Jaypee Institute of Information Technology, Noida | 2009 | 6.8 / 10 |
| MBA | Jaypee Business School | 2010 | 7.3 / 10 |
| Certificate – R Programming | Indian Institute of Technology, Chennai | 2017 | 75% |
| Diploma in Statistics | Indira Gandhi National Open University | 2018 | 73% |

---

## CERTIFICATIONS

- Microsoft Certified: Power BI Data Analyst Associate — Microsoft (2023)
- Data Science Using Python — Udemy (2021)
- Python for Data Science — Udemy (2020)
