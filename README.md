# 🚀 Career Pilot - Career Guidance & Job Recommendation System

An AI-powered career guidance platform that helps students discover their ideal career path through skill assessment, personalized roadmaps, and job recommendations.

Live Demo: _Add your Render link after deployment_

### ✨ Features
- **Smart Assessment:** 5-stage career assessment to understand user interests
- **Career Recommendation Engine:** Python-based logic to match skills with careers
- **Job Matching:** Personalized job recommendations based on user profile
- **Skill Gap Analysis:** Shows what skills you have vs what job needs
- **Learning Roadmap:** 3-stage roadmap with projects & checklists
- **Admin Dashboard:** Manage careers, jobs, and users

### 🛠️ Tech Stack
- **Backend:** Python, Flask, Jinja2
- **Database:** MySQL - 15 relational tables
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Auth:** Werkzeug Security (Hashed Passwords)

### 🗄️ Database Structure (15 Tables)
- `users`: Core authentication
- `student_profiles`: Academic & career preferences
- `skills`: Master table of technical/domain/soft skills
- `user_skills`, `careers`, `career_skills`, `assessments`, `career_recommendations`, `jobs`, `job_skills` etc.

### ⚙️ How to Run Locally
1. Clone the repo
   `git clone https://github.com/VenkataKavyaSunkara/career-pilot.git`
2. Install dependencies
   `pip install -r requirements.txt`
3. Setup DB
   - Import `schema.sql`
   - Import `seed_data.sql`
4. Run
   `python app.py`

### 👩‍💻 Author
Venkata Kavya Sunkara
