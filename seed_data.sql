-- ====================================================================
-- Career Pilot Seed Data
-- Standard Skills, Careers, Career-Skills, Roadmaps, Demo Jobs, and Initial Users
-- ====================================================================

-- 1. Initial Users (Admin & Sample Student)
-- Passwords:
-- admin@careerpilot.local -> Admin@123
-- student@careerpilot.local -> Student@123
INSERT INTO users (id, full_name, email, password_hash, role, created_at) VALUES
(1, 'System Administrator', 'admin@careerpilot.local', 'scrypt:32768:8:1$FmhpFmoO5YBp7rIo$34792964196f57b932064ba2144bcfc8eef4150c1626683ea4ddb69bb9634816aa07d92eb2d06b20d8daa24c2dcbd0ae29b2b0e19a034c0e7d0dac037f850013', 'admin', NOW()),
(2, 'Alex Morgan', 'student@careerpilot.local', 'scrypt:32768:8:1$oHJLldpXqrcVbc3S$1288e1bfacf0206be8b4648ef03430c8e667853f7e178c0bd6cb9f4a87bfcf6c629c5e09b5b65ca4a5947118fa222c52498997ff1994302b3263279e9a0ac578', 'student', NOW())
ON DUPLICATE KEY UPDATE id=id;

-- 2. Initial Student Profile for Alex Morgan
INSERT INTO student_profiles (user_id, education_level, degree, specialization, graduation_year, experience_level, preferred_location, career_interests, career_goals) VALUES
(2, 'Undergraduate', 'B.Tech / B.E.', 'Computer Science & Engineering', 2026, 'Fresher (0-1 yrs)', 'Bangalore / Remote', 'Web Development, Python Development, Data Analytics', 'Aspiring software developer eager to build scalable web applications and real-time data pipelines.')
ON DUPLICATE KEY UPDATE user_id=user_id;

-- 3. Skills Master Data
INSERT INTO skills (id, skill_name, skill_category) VALUES
(1, 'Python', 'Programming Languages'),
(2, 'JavaScript', 'Programming Languages'),
(3, 'Java', 'Programming Languages'),
(4, 'C++', 'Programming Languages'),
(5, 'HTML5 & CSS3', 'Web Technologies'),
(6, 'React.js', 'Web Technologies'),
(7, 'Node.js', 'Web Technologies'),
(8, 'Flask / Django', 'Web Technologies'),
(9, 'SQL / MySQL', 'Databases'),
(10, 'MongoDB / NoSQL', 'Databases'),
(11, 'Database Administration', 'Databases'),
(12, 'Pandas & NumPy', 'Data & AI'),
(13, 'Machine Learning & Scikit-Learn', 'Data & AI'),
(14, 'Deep Learning (PyTorch/TensorFlow)', 'Data & AI'),
(15, 'Tableau / Power BI', 'Data & AI'),
(16, 'Data Visualization', 'Data & AI'),
(17, 'Git & Version Control', 'Development Tools'),
(18, 'Linux & Bash Scripting', 'Systems & Cloud'),
(19, 'Docker & Containers', 'Systems & Cloud'),
(20, 'Network Security & Firewalls', 'Cybersecurity'),
(21, 'Ethical Hacking & Pen Testing', 'Cybersecurity'),
(22, 'Cryptography & IAM', 'Cybersecurity'),
(23, 'Figma & Wireframing', 'Design & UX'),
(24, 'UI Prototyping & User Research', 'Design & UX'),
(25, 'SEO & SEM', 'Digital Marketing'),
(26, 'Google Analytics & Content Strategy', 'Digital Marketing'),
(27, 'Business Process Modeling & UML', 'Business Analysis'),
(28, 'Agile & Scrum Methodologies', 'Business Analysis'),
(29, 'Analytical Problem Solving', 'Soft Skills'),
(30, 'Communication & Presentation', 'Soft Skills')
ON DUPLICATE KEY UPDATE id=id;

-- 4. Initial User Skills for Alex Morgan
INSERT INTO user_skills (user_id, skill_id, proficiency_level) VALUES
(2, 1, 'Intermediate'),
(2, 2, 'Intermediate'),
(2, 5, 'Advanced'),
(2, 8, 'Intermediate'),
(2, 9, 'Intermediate'),
(2, 17, 'Intermediate'),
(2, 29, 'Advanced'),
(2, 30, 'Intermediate')
ON DUPLICATE KEY UPDATE user_id=user_id;

-- 5. Careers Master Data (10 Core Roles)
INSERT INTO careers (id, title, description, required_education, entry_level_roles, is_active) VALUES
(1, 'Data Analyst', 'Collects, cleans, and analyzes structured and unstructured datasets to derive actionable business insights and create data visualizations.', 'Bachelor''s in Computer Science, Statistics, Mathematics, or Data Science', 'Junior Data Analyst, Business Intelligence Associate, Reporting Analyst', 1),
(2, 'Python Developer', 'Designs, builds, and maintains backend services, automation scripts, and server-side web applications using Python and related ecosystems.', 'Bachelor''s in Computer Science, Information Technology, or Engineering', 'Junior Python Engineer, Backend Trainee, Automation Developer', 1),
(3, 'Software Developer', 'Architects, writes, and tests core software systems, algorithmic modules, and end-to-end desktop and enterprise applications.', 'Bachelor''s or Master''s degree in Computer Science, Software Engineering', 'Associate Software Engineer, Junior Software Engineer, Graduate Developer', 1),
(4, 'Web Developer', 'Creates responsive, interactive client-side interfaces and scalable server-side web architectures using modern web standards.', 'Bachelor''s degree or equivalent technical certification/diploma in Web Technologies', 'Junior Full Stack Developer, Frontend Developer, Web Specialist', 1),
(5, 'Business Analyst', 'Bridges the gap between business stakeholders and technical teams by analyzing requirements, workflows, and translating needs into specifications.', 'Bachelor''s in Business Administration, Information Systems, or Engineering', 'Associate Business Analyst, Systems Analyst, Requirements Coordinator', 1),
(6, 'UI/UX Designer', 'Designs user journeys, wireframes, high-fidelity prototypes, and design systems for intuitive digital experiences.', 'Bachelor''s in Design, Human-Computer Interaction, CS, or Fine Arts', 'Junior UI Designer, Product Design Intern, UX Researcher Assistant', 1),
(7, 'Cybersecurity Analyst', 'Protects organization networks, applications, and confidential assets from unauthorized breaches, threats, and vulnerabilities.', 'Bachelor''s in Cybersecurity, Computer Science, or Network Engineering', 'Junior Security Analyst, SOC Analyst L1, Information Security Associate', 1),
(8, 'Digital Marketing Specialist', 'Drives online brand visibility, traffic acquisition, search rankings, and campaign conversions through digital channels.', 'Bachelor''s degree in Marketing, Mass Media, Business, or Communications', 'Digital Marketing Executive, SEO Specialist, Social Media Analyst', 1),
(9, 'Database Administrator', 'Ensures high availability, security, query optimization, backup strategies, and integrity of critical database servers.', 'Bachelor''s degree in Computer Science, IT, or Computer Applications', 'Junior DBA, Database Support Engineer, Data Operations Analyst', 1),
(10, 'Machine Learning Engineer', 'Researches, constructs, trains, and deploys predictive machine learning models and neural networks into production pipelines.', 'Bachelor''s or Master''s degree in Computer Science, AI/ML, or Mathematics', 'Junior ML Engineer, AI Associate, Applied Data Scientist', 1)
ON DUPLICATE KEY UPDATE id=id;

-- 6. Career Skills Mapping (Importance: High, Medium, Low)
INSERT INTO career_skills (career_id, skill_id, importance_level) VALUES
-- Data Analyst
(1, 1, 'High'),   -- Python
(1, 9, 'High'),   -- SQL / MySQL
(1, 12, 'High'),  -- Pandas & NumPy
(1, 15, 'High'),  -- Tableau / Power BI
(1, 16, 'High'),  -- Data Visualization
(1, 29, 'High'),  -- Analytical Problem Solving
(1, 30, 'Medium'),-- Communication

-- Python Developer
(2, 1, 'High'),   -- Python
(2, 8, 'High'),   -- Flask / Django
(2, 9, 'High'),   -- SQL / MySQL
(2, 17, 'High'),  -- Git
(2, 18, 'Medium'),-- Linux
(2, 19, 'Medium'),-- Docker
(2, 29, 'High'),  -- Analytical Problem Solving

-- Software Developer
(3, 1, 'High'),   -- Python
(3, 3, 'High'),   -- Java
(3, 4, 'High'),   -- C++
(3, 9, 'High'),   -- SQL / MySQL
(3, 17, 'High'),  -- Git
(3, 28, 'Medium'),-- Agile
(3, 29, 'High'),  -- Analytical Problem Solving

-- Web Developer
(4, 2, 'High'),   -- JavaScript
(4, 5, 'High'),   -- HTML5 & CSS3
(4, 6, 'High'),   -- React.js
(4, 7, 'High'),   -- Node.js
(4, 8, 'Medium'), -- Flask / Django
(4, 9, 'High'),   -- SQL / MySQL
(4, 17, 'High'),  -- Git

-- Business Analyst
(5, 9, 'Medium'), -- SQL
(5, 15, 'Medium'),-- Tableau / Power BI
(5, 27, 'High'),  -- Business Process Modeling
(5, 28, 'High'),  -- Agile & Scrum
(5, 29, 'High'),  -- Analytical Problem Solving
(5, 30, 'High'),  -- Communication

-- UI/UX Designer
(6, 5, 'Medium'), -- HTML5 & CSS3
(6, 23, 'High'),  -- Figma
(6, 24, 'High'),  -- Prototyping & User Research
(6, 29, 'Medium'),-- Analytical Problem Solving
(6, 30, 'High'),  -- Communication

-- Cybersecurity Analyst
(7, 1, 'Medium'), -- Python
(7, 18, 'High'),  -- Linux & Bash
(7, 20, 'High'),  -- Network Security
(7, 21, 'High'),  -- Ethical Hacking
(7, 22, 'High'),  -- Cryptography & IAM
(7, 29, 'High'),  -- Analytical Problem Solving

-- Digital Marketing Specialist
(8, 25, 'High'),  -- SEO & SEM
(8, 26, 'High'),  -- Google Analytics & Content
(8, 30, 'High'),  -- Communication

-- Database Administrator
(9, 9, 'High'),   -- SQL / MySQL
(9, 10, 'Medium'),-- MongoDB / NoSQL
(9, 11, 'High'),  -- Database Administration
(9, 18, 'High'),  -- Linux & Bash
(9, 29, 'High'),  -- Analytical Problem Solving

-- Machine Learning Engineer
(10, 1, 'High'),  -- Python
(10, 9, 'Medium'),-- SQL
(10, 12, 'High'), -- Pandas & NumPy
(10, 13, 'High'), -- Machine Learning
(10, 14, 'High'), -- Deep Learning
(10, 19, 'Medium'),-- Docker
(10, 29, 'High')  -- Analytical Problem Solving
ON DUPLICATE KEY UPDATE career_id=career_id;

-- 7. Predefined Learning Roadmaps (JSON Content)
INSERT INTO roadmaps (career_id, title, description, roadmap_content) VALUES
(1, 'Data Analyst Learning Roadmap', 'Step-by-step master path to transition from spreadsheet novice to industry-ready data analyst.',
'{"stages": [{"name": "Beginner", "duration": "Weeks 1-4", "topics": ["Excel Advanced (VLOOKUP, Pivot, INDEX/MATCH)", "SQL Basics: SELECT, WHERE, GROUP BY, JOINS", "Statistical Fundamentals: Mean, Median, Variance, Distributions"]}, {"name": "Intermediate", "duration": "Weeks 5-8", "topics": ["Python for Data Analysis (Pandas, NumPy)", "Exploratory Data Analysis (EDA) Techniques", "Data Visualization with Matplotlib & Seaborn", "Interactive Dashboards with Power BI or Tableau"]}, {"name": "Advanced", "duration": "Weeks 9-12", "topics": ["Complex SQL Window Functions & CTEs", "Data Storytelling & Executive Reporting", "A/B Testing and Hypothesis Validation", "Basic Predictive Analytics & Time Series"]}], "projects": ["Sales Performance Executive Dashboard in Power BI", "E-commerce Customer Retention & Cohort Analysis using SQL & Python", "Global Healthcare Trends EDA with Kaggle Dataset"], "interview_topics": ["SQL Joins and Aggregation query challenges", "Explaining A/B testing statistical significance", "Walkthrough of an end-to-end data cleansing scenario", "Data visualization best practices for stakeholders"], "checklist": ["Master SQL Joins and Aggregations", "Build 2 Power BI / Tableau dashboards", "Complete 1 full end-to-end Python EDA on GitHub", "Practice 20 LeetCode / HackerRank SQL questions"]}'),

(2, 'Python Developer Learning Roadmap', 'Comprehensive path for mastering Python, asynchronous programming, clean code, and API engineering.',
'{"stages": [{"name": "Beginner", "duration": "Weeks 1-4", "topics": ["Python Syntax, Data Structures (Lists, Dicts, Sets)", "OOP Principles (Classes, Inheritance, Polymorphism)", "File I/O, Exception Handling, Virtual Environments"]}, {"name": "Intermediate", "duration": "Weeks 5-8", "topics": ["Relational Databases & ORM (SQLAlchemy, Raw SQL)", "Building REST APIs with Flask / FastAPI", "Authentication & JWT / Session Security", "Unit Testing with PyTest & Mocking"]}, {"name": "Advanced", "duration": "Weeks 9-12", "topics": ["Concurrency with Asyncio, Threading, & Multiprocessing", "Dockerizing Python Microservices", "Redis Caching and Celery Task Queues", "CI/CD Workflows with GitHub Actions"]}], "projects": ["RESTful API for Task Management with Flask & MySQL", "Automated Web Scraper with Rate Limiting and Data Pipeline", "Real-Time Chat Microservice with WebSockets & Redis"], "interview_topics": ["Python GIL (Global Interpreter Lock) and how it affects concurrency", "Generators, Iterators, and Decorators in depth", "Database optimization and query indexing", "REST API architecture and status code design"], "checklist": ["Write unit tests with >80% coverage on a project", "Deploy a containerized Flask/FastAPI service", "Publish 2 well-documented repositories on GitHub", "Implement token-based authentication and rate limiting"]}'),

(3, 'Software Developer Learning Roadmap', 'Foundational and industry-level software engineering path covering algorithms, system design, and OOP.',
'{"stages": [{"name": "Beginner", "duration": "Weeks 1-4", "topics": ["Core Programming (Java/C++/Python) & Control Flow", "Data Structures: Arrays, Linked Lists, Stacks, Queues", "Git Branching, Commit Etiquette, and Pull Requests"]}, {"name": "Intermediate", "duration": "Weeks 5-8", "topics": ["Advanced Trees, Graphs, Sorting & Searching Algorithms", "Design Patterns (Factory, Singleton, Observer, Strategy)", "Database Modeling, Normalization, and ACID Properties", "Writing Clean, Modular, and Testable Code"]}, {"name": "Advanced", "duration": "Weeks 9-12", "topics": ["Basic Distributed Systems & Microservice Architecture", "Caching Strategies and Database Sharding Concepts", "API Gateway and Message Broker Integration (Kafka/RabbitMQ)", "System Design Interviews Preparation"]}], "projects": ["Inventory & Billing Desktop/Server Management System", "Multi-Threaded File Downloader / Cache Manager", "Distributed Rate Limiter Implementation in C++/Java"], "interview_topics": ["Time and Space Complexity Analysis (Big-O)", "Object-Oriented Design (SOLID Principles)", "Designing a scalable URL Shortener", "Deadlock conditions and thread synchronization"], "checklist": ["Solve 75+ LeetCode DSA questions", "Implement 5 core design patterns in code", "Build and architect a full-fledged client-server app", "Conduct 3 mock technical interviews"]}'),

(4, 'Web Developer Learning Roadmap', 'Full-stack web development blueprint mastering frontend reactivity, backend services, and modern standards.',
'{"stages": [{"name": "Beginner", "duration": "Weeks 1-4", "topics": ["Semantic HTML5, CSS3 Grid, Flexbox, & Responsive Layouts", "Modern JavaScript (ES6+): Promises, Fetch, DOM Events", "CSS Variables, Animations, and Accessibility (a11y)"]}, {"name": "Intermediate", "duration": "Weeks 5-8", "topics": ["React.js: Hooks, State Management, Router", "Backend REST APIs with Node.js/Express or Python Flask", "Relational & Document Databases (MySQL, MongoDB)", "Authentication: Sessions, Cookies, and OAuth 2.0"]}, {"name": "Advanced", "duration": "Weeks 9-12", "topics": ["Server-Side Rendering (Next.js) & Performance Tuning", "Web Security: XSS, CSRF, CORS, CSP Best Practices", "Containerization with Docker and Cloud Deployment (AWS/Vercel)", "End-to-End Testing with Playwright / Cypress"]}], "projects": ["Full-Stack Career & Job Portal with Responsive UI", "Collaborative Kanban Task Board with Drag-and-Drop", "Interactive E-Commerce Store with Cart & Payment Flow"], "interview_topics": ["JavaScript Event Loop, Closures, and Prototypal Inheritance", "React Virtual DOM and reconciliation engine", "State management tradeoffs (Redux vs Context vs Zustand)", "Web performance optimization (Lighthouse, Lazy Loading)"], "checklist": ["Create a modern responsive portfolio website", "Build 1 full-stack CRUD application with auth", "Achieve 90+ Lighthouse score on a deployed app", "Deploy a web app with automated CI/CD pipeline"]}'),

(5, 'Business Analyst Learning Roadmap', 'Strategy and technical blueprint for bridging commercial goals and software engineering deliverables.',
'{"stages": [{"name": "Beginner", "duration": "Weeks 1-4", "topics": ["SDLC Methodologies: Waterfall vs Agile vs Kanban", "Stakeholder Communication & Interviewing Techniques", "Writing Business Requirement Documents (BRD) & FRD"]}, {"name": "Intermediate", "duration": "Weeks 5-8", "topics": ["User Stories and Acceptance Criteria (Gherkin/INVEST)", "Process Mapping: BPMN 2.0 and UML Use Case Diagrams", "SQL for Data Exploration and Fact-Checking", "JIRA & Confluence for Backlog Grooming"]}, {"name": "Advanced", "duration": "Weeks 9-12", "topics": ["Financial Modeling & ROI Cost-Benefit Analysis", "Data Analytics & Dashboarding with Power BI", "Change Management and UAT (User Acceptance Testing)", "Enterprise Architecture Basics"]}], "projects": ["Banking Customer Onboarding Process Redesign BRD", "HealthTech Telemedicine Feature Specification & Wireframes", "E-Commerce Return Workflow Optimization Analysis"], "interview_topics": ["Handling conflicting requirements from multiple stakeholders", "Writing measurable and testable acceptance criteria", "Root cause analysis methodologies (5 Whys, Fishbone)", "Prioritization frameworks (MoSCoW, RICE, WSJF)"], "checklist": ["Complete a comprehensive BRD with UML diagrams", "Draft 15 detailed user stories with acceptance criteria", "Build an executive KPI tracker dashboard", "Lead a simulated sprint planning session"]}'),

(6, 'UI/UX Designer Learning Roadmap', 'Product design roadmap covering user research, usability heuristics, interaction design, and design systems.',
'{"stages": [{"name": "Beginner", "duration": "Weeks 1-4", "topics": ["Design Fundamentals: Typography, Color Theory, Spacing", "Figma Fundamentals: Frames, Auto Layout, Components", "Heuristic Evaluation (Nielsen Norman 10 Usability Principles)"]}, {"name": "Intermediate", "duration": "Weeks 5-8", "topics": ["User Research Methods: User Personas, Journey Maps", "Wireframing: Low-Fidelity to High-Fidelity Transitions", "Interactive Prototyping and Micro-Interactions in Figma", "Usability Testing and Feedback Synthesis"]}, {"name": "Advanced", "duration": "Weeks 9-12", "topics": ["Building Scalable Design Systems & Token Architecture", "Accessibility Standards (WCAG 2.1 AA Compliance)", "Developer Handoff Best Practices & CSS Inspecting", "Product Metrics: Conversion Rate, Churn, SUS Score"]}], "projects": ["Fintech Mobile Wallet App Redesign & Case Study", "SaaS Dashboard Design System with 30+ Reusable Components", "Accessible Healthcare Appointment Booking Experience"], "interview_topics": ["Defending design choices using research data", "Trade-offs between visual aesthetics and business goals", "Design system governance and versioning", "Walkthrough of your design process on a portfolio case study"], "checklist": ["Publish 2 in-depth case studies on Behance/Portfolio", "Master Figma Auto Layout and Component Variants", "Run usability tests with 5 real users on a prototype", "Document full design system tokens and component specs"]}'),

(7, 'Cybersecurity Analyst Learning Roadmap', 'Defensive security, incident response, network auditing, and vulnerability assessment roadmap.',
'{"stages": [{"name": "Beginner", "duration": "Weeks 1-4", "topics": ["Networking Fundamentals: OSI Model, TCP/IP, DNS, Subnets", "Linux CLI Operations & Administration Essentials", "Information Security Principles: CIA Triad & Risk Basics"]}, {"name": "Intermediate", "duration": "Weeks 5-8", "topics": ["Security Monitoring: SIEM Tools (Splunk, Elastic)", "Network Packet Analysis with Wireshark & Tcpdump", "Vulnerability Scanning with Nmap, Nessus, OpenVAS", "Identity and Access Management (IAM) & Active Directory"]}, {"name": "Advanced", "duration": "Weeks 9-12", "topics": ["Incident Response Frameworks (NIST & SANS)", "Malware Analysis Fundamentals & Sandboxing", "Web Application Security (OWASP Top 10)", "Cloud Security (AWS Security Hub & Azure Defender)"]}], "projects": ["Home SOC Lab Setup with Splunk and Sysmon Telemetry", "OWASP Juice Shop Vulnerability Assessment & Remediation Report", "Automated Bash/Python Incident Response Script"], "interview_topics": ["Step-by-step investigation of a suspected phishing breach", "Explaining TCP 3-way handshake and SYN flood attacks", "How to isolate an infected endpoint on a corporate subnet", "Remediation tactics for SQL Injection and Broken Object Auth"], "checklist": ["Build a virtualized home cybersecurity lab", "Achieve 20+ challenge solves on TryHackMe / HackTheBox", "Author an official Vulnerability Assessment Report", "Complete Security+ or equivalent foundational mock exams"]}'),

(8, 'Digital Marketing Specialist Learning Roadmap', 'Full-funnel digital marketing curriculum covering SEO, programmatic search, content growth, and analytics.',
'{"stages": [{"name": "Beginner", "duration": "Weeks 1-4", "topics": ["Marketing Funnel: Top of Funnel to Retention", "Keyword Research Tools (Ahrefs, SEMrush, Google Trends)", "On-Page SEO: Title Tags, Meta, Schema, Heading Structure"]}, {"name": "Intermediate", "duration": "Weeks 5-8", "topics": ["Technical SEO: Site Speed, Crawlability, Sitemaps", "Google Ads (PPC): Search Campaigns, Ad Copies, Bidding", "Google Analytics 4 (GA4) Custom Events & Conversions", "Content Strategy and Inbound Editorial Calendar"]}, {"name": "Advanced", "duration": "Weeks 9-12", "topics": ["Email Marketing Automation & Lead Nurturing Flows", "Conversion Rate Optimization (CRO) & Heatmap Analysis", "Social Media Advertising (Meta Ads Manager, LinkedIn Ads)", "Marketing Attribution Modeling & CAC/LTV Ratios"]}], "projects": ["Live Website SEO Audit & 90-Day Traffic Growth Strategy", "Search Engine PPC Campaign Mockup with ROI Forecast", "Complete 5-Stage Email Nurturing Funnel with Copywriting"], "interview_topics": ["Diagnosing an unexpected 30% drop in organic traffic", "Structuring a high-converting PPC campaign from scratch", "Interpreting GA4 user engagement metrics", "Balancing brand marketing with direct response acquisition"], "checklist": ["Conduct a full technical SEO audit for an active website", "Write and optimize 3 long-form rankable articles", "Earn Google Analytics 4 Certification", "Create a comprehensive multi-channel digital campaign plan"]}'),

(9, 'Database Administrator Learning Roadmap', 'Enterprise DBA track covering high availability, indexing, performance tuning, replication, and disaster recovery.',
'{"stages": [{"name": "Beginner", "duration": "Weeks 1-4", "topics": ["Relational Database Theory, Normalization (1NF to BCNF)", "Advanced SQL: Window Functions, CTEs, Subqueries", "Storage Engines: InnoDB Architecture & Buffer Pool"]}, {"name": "Intermediate", "duration": "Weeks 5-8", "topics": ["Index Architecture: B-Trees, Hash, Composite Indexes", "Query Profiling with EXPLAIN and Slow Query Logs", "Database Backups: Logical (mysqldump) vs Physical (Percona)", "User Privilege Management and Database Auditing"]}, {"name": "Advanced", "duration": "Weeks 9-12", "topics": ["High Availability: Master-Slave Replication, Clustering", "Connection Pooling, MaxScale, and ProxySQL", "Database Partitioning, Sharding, and Archiving Strategies", "NoSQL Scaling Patterns with MongoDB / Redis"]}], "projects": ["Automated Automated MySQL Backup & Restore Verification Script", "Slow Query Optimization Case Study on 1M+ Records Dataset", "Master-Replica MySQL Replication Setup on Ubuntu VM"], "interview_topics": ["Resolving deadlocks in high-throughput transactions", "Index selection for multi-column filtering queries", "Disaster recovery RTO (Recovery Time Objective) vs RPO", "Database tuning parameters in my.cnf / postgresql.conf"], "checklist": ["Set up automated backup scripts with cron and notification", "Optimize 5 complex slow queries using EXPLAIN plans", "Configure and test failover on a replica node", "Write runbooks for disaster recovery and schema migrations"]}'),

(10, 'Machine Learning Engineer Learning Roadmap', 'From statistical learning to production MLOps, deep learning architectures, and scalable inference.',
'{"stages": [{"name": "Beginner", "duration": "Weeks 1-4", "topics": ["Linear Algebra, Calculus, Probability & Statistics for ML", "Python Libraries: NumPy, Pandas, Matplotlib", "Data Preprocessing: Imputation, One-Hot Encoding, Scaling"]}, {"name": "Intermediate", "duration": "Weeks 5-8", "topics": ["Supervised Learning: Linear/Logistic Regression, Trees, SVM", "Unsupervised Learning: K-Means, PCA, Hierarchical Clustering", "Ensemble Methods: Random Forest, XGBoost, LightGBM", "Model Evaluation: ROC-AUC, Precision-Recall, Cross-Validation"]}, {"name": "Advanced", "duration": "Weeks 9-12", "topics": ["Deep Learning with PyTorch: CNNs, RNNs, Transformers", "MLOps: MLflow Tracking, Model Versioning, DVC", "Packaging Models with FastAPI & Docker Containers", "Monitoring Model Drift in Production"]}], "projects": ["End-to-End Loan Default Prediction with XGBoost & Explainability (SHAP)", "Image Classification Service with PyTorch, FastAPI & Docker", "Customer Sentiment Analysis Pipeline with HuggingFace Transformers"], "interview_topics": ["Bias-Variance tradeoff and regularization techniques", "Under the hood of Gradient Descent and Adam optimizers", "Handling severe class imbalance in classification", "Deploying and scaling low-latency inference endpoints"], "checklist": ["Build and publish 3 end-to-end ML projects on GitHub", "Implement a machine learning algorithm from scratch in NumPy", "Deploy a trained model as an accessible REST API", "Track experiments using MLflow or Weights & Biases"]}');

-- 8. Demonstration Job Listings (Clear Demonstration Data Notice)
-- Note: As per project guidelines, these are curated demonstration listings.
INSERT INTO jobs (id, title, company_name, description, required_education, experience_level, location, employment_type, application_url, posted_at, is_active) VALUES
(1, 'Junior Data Analyst', 'Apex Analytics Solutions', 'Seeking an analytical mind to extract, transform, and visualize enterprise datasets. You will write SQL queries, generate dashboards in Power BI, and collaborate with business teams. [Demonstration Listing]', 'Bachelor''s in CS, IT, Statistics, or Math', 'Fresher (0-1 yrs)', 'Bangalore / Hybrid', 'Full-time', 'https://example.com/demo-careers/apex-data-analyst', NOW() - INTERVAL 2 DAY, 1),
(2, 'Associate Python Developer', 'NextWave Software Labs', 'Join our backend engineering crew building robust microservices, database connectors, and automation tools using Python, Flask, and MySQL. [Demonstration Listing]', 'Bachelor''s in Computer Science or related degree', 'Fresher (0-1 yrs)', 'Hyderabad / Remote', 'Full-time', 'https://example.com/demo-careers/nextwave-python-dev', NOW() - INTERVAL 3 DAY, 1),
(3, 'Junior Software Engineer', 'Cognitive Cloud Systems', 'Develop clean, scalable code in Java/Python. Participate in agile ceremonies, write automated unit tests, and resolve algorithmic tickets in an enterprise codebase. [Demonstration Listing]', 'B.Tech / B.E. / MCA in Computer Science', 'Fresher (0-1 yrs)', 'Pune / On-site', 'Full-time', 'https://example.com/demo-careers/cognitive-cloud-se', NOW() - INTERVAL 1 DAY, 1),
(4, 'Frontend / Web Developer Trainee', 'PixelCraft Digital', 'Help craft fluid web user interfaces using modern HTML5, CSS3, JavaScript, and React. Work alongside UI designers to transform prototypes into pixel-perfect pages. [Demonstration Listing]', 'Bachelor''s degree or Diploma in Computer Applications', 'Fresher (0-1 yrs)', 'Chennai / Remote', 'Full-time', 'https://example.com/demo-careers/pixelcraft-web-trainee', NOW() - INTERVAL 4 DAY, 1),
(5, 'Junior Business Analyst', 'FinCorp Global Advisory', 'Analyze functional requirements, interact with business sponsors, author user stories with acceptance criteria, and create workflow diagrams. [Demonstration Listing]', 'Bachelor''s in Business, IT, or Engineering', '1-2 years', 'Mumbai / Hybrid', 'Full-time', 'https://example.com/demo-careers/fincorp-ba', NOW() - INTERVAL 5 DAY, 1),
(6, 'Junior UI/UX Designer', 'Vanguard Studio', 'Create intuitive user experiences, wireframes, and design system components in Figma. Conduct usability testing sessions with target users. [Demonstration Listing]', 'Degree in Design, HCI, or portfolio equivalent', 'Fresher (0-1 yrs)', 'Bangalore / Remote', 'Full-time', 'https://example.com/demo-careers/vanguard-uiux', NOW() - INTERVAL 2 DAY, 1),
(7, 'SOC Security Analyst (Tier 1)', 'CyberShield Infosec', 'Monitor incoming SIEM alerts, examine suspicious network packets, perform initial triage on potential incidents, and document vulnerability reports. [Demonstration Listing]', 'Bachelor''s in Cybersecurity or Computer Science', 'Fresher (0-1 yrs)', 'Delhi NCR / On-site', 'Full-time', 'https://example.com/demo-careers/cybershield-soc', NOW() - INTERVAL 3 DAY, 1),
(8, 'Junior Machine Learning Engineer', 'NeuralMatrix AI', 'Assist in data preprocessing, feature engineering, model training with Scikit-learn and PyTorch, and packaging endpoints into Docker containers. [Demonstration Listing]', 'Bachelor''s or Master''s in CS, AI, or Mathematics', 'Fresher (0-1 yrs)', 'Bangalore / Hybrid', 'Full-time', 'https://example.com/demo-careers/neuralmatrix-ml', NOW() - INTERVAL 1 DAY, 1),
(9, 'Junior Database Administrator', 'DataVault Enterprise', 'Assist in database server monitoring, indexing review, routine backups, performance tuning, and schema migration tasks on MySQL servers. [Demonstration Listing]', 'Bachelor''s in Computer Science, IT, or BCA', 'Fresher (0-1 yrs)', 'Noida / On-site', 'Full-time', 'https://example.com/demo-careers/datavault-dba', NOW() - INTERVAL 6 DAY, 1),
(10, 'Digital Marketing Executive', 'OmniReach Growth Agency', 'Manage organic search optimization (SEO), coordinate on-page content, analyze website metrics via GA4, and assist in paid search campaigns. [Demonstration Listing]', 'Bachelor''s in Marketing, Media, or Commerce', 'Fresher (0-1 yrs)', 'Remote', 'Full-time', 'https://example.com/demo-careers/omnireach-marketing', NOW() - INTERVAL 7 DAY, 1)
ON DUPLICATE KEY UPDATE id=id;

-- 9. Job Required Skills Mapping
INSERT INTO job_skills (job_id, skill_id) VALUES
-- Job 1 (Junior Data Analyst): Python, SQL, Tableau, Pandas, Data Visualization
(1, 1), (1, 9), (1, 12), (1, 15), (1, 16),
-- Job 2 (Associate Python Dev): Python, Flask/Django, SQL, Git, Linux
(2, 1), (2, 8), (2, 9), (2, 17), (2, 18),
-- Job 3 (Junior Software Engineer): Python, Java, SQL, Git, Analytical Problem Solving
(3, 1), (3, 3), (3, 9), (3, 17), (3, 29),
-- Job 4 (Frontend / Web Trainee): JavaScript, HTML5 & CSS3, React.js, Git
(4, 2), (4, 5), (4, 6), (4, 17),
-- Job 5 (Junior Business Analyst): SQL, Tableau, Business Process, Agile, Communication
(5, 9), (5, 15), (5, 27), (5, 28), (5, 30),
-- Job 6 (Junior UI/UX Designer): HTML5 & CSS3, Figma, Prototyping, Communication
(6, 5), (6, 23), (6, 24), (6, 30),
-- Job 7 (SOC Security Analyst): Python, Linux, Network Security, Ethical Hacking
(7, 1), (7, 18), (7, 20), (7, 21),
-- Job 8 (Junior ML Engineer): Python, Pandas, Machine Learning, Deep Learning, Docker
(8, 1), (8, 12), (8, 13), (8, 14), (8, 19),
-- Job 9 (Junior DBA): SQL, Database Administration, Linux, Analytical Problem Solving
(9, 9), (9, 11), (9, 18), (9, 29),
-- Job 10 (Digital Marketing Executive): SEO & SEM, Google Analytics, Communication
(10, 25), (10, 26), (10, 30)
ON DUPLICATE KEY UPDATE job_id=job_id;
