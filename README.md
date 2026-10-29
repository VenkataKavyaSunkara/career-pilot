# Career Pilot Database Documentation

This folder contains the SQL schema definitions and initial demonstration datasets for the **Career Pilot – Career Guidance and Job Recommendation System**.

## Files Overview

1. `schema.sql`: Contains the complete DDL for all 15 relational tables with primary keys, foreign keys (`ON DELETE CASCADE`), indexes, and unique constraints.
2. `seed_data.sql`: Contains the baseline skills (30 skills across 9 categories), 10 core career profiles, skill associations with importance levels, detailed 3-stage learning roadmaps with projects and checklists, 10 demonstration job listings, and default test accounts.

## Tables (15 Tables)

- `users`: Core authentication table (passwords hashed using Werkzeug).
- `student_profiles`: Detailed academic and career preference records.
- `skills`: Master table of technical, domain, and soft skills.
- `user_skills`: Mapping of skills acquired by each student.
- `careers`: Catalog of supported career paths.
- `career_skills`: Career skill requirements mapped by importance (High, Medium, Low).
- `assessments`: History of completed career assessment question sets and JSON payloads.
- `career_recommendations`: Calculated recommendation match scores and justification summaries.
- `jobs`: Predefined demonstration job listings with employment type and location.
- `job_skills`: Required skill mapping for job listings.
- `saved_jobs`: Student job bookmarks.
- `roadmaps`: Career learning paths broken into Beginner, Intermediate, and Advanced stages.
- `user_roadmaps`: Saved user learning roadmaps and completion percentages.
- `roadmap_progress`: Individual checklist item completions for active roadmaps.
- `admin_audit_logs`: Administrative actions log for transparency.

## Default Credentials (Demo)

- **Admin Account**:
  - Email: `admin@careerpilot.local`
  - Password: `Admin@123`
  - Role: `admin`
- **Student Account**:
  - Email: `student@careerpilot.local`
  - Password: `Student@123`
  - Role: `student`

## How to Initialize in MySQL

### Option 1: Using the provided Python initialization script
```bash
python database/init_db.py
```

### Option 2: Using MySQL CLI or phpMyAdmin / MySQL Workbench
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS career_pilot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -p career_pilot < database/schema.sql
mysql -u root -p career_pilot < database/seed_data.sql
```
