from models.job_model import JobModel
from models.skill_model import SkillModel
from models.profile_model import ProfileModel

class JobRecommendationService:
    """
    Transparent, Rule-Based Job Recommendation Engine.
    Matches demonstration jobs against student profile and skills:
    1. Skill Overlap (50%): Ratio of job's required skills present in student's profile.
    2. Role & Title Affinity (25%): Keyword matching between job title and student's career interests / goals.
    3. Location Preference (15%): Compatibility between job location and student's preferred location.
    4. Experience Level (10%): Match between candidate experience and job experience requirements.
    """

    @classmethod
    def recommend_for_user(cls, user_id, limit=10):
        """
        Calculates relevance scores for all active demonstration jobs for a student.
        Returns a sorted list of jobs with match details.
        """
        all_jobs = JobModel.get_all(active_only=True, limit=100)
        user_skills = SkillModel.get_user_skills(user_id)
        user_skill_ids = set(s['id'] for s in user_skills)
        user_skill_names = set(s['skill_name'].lower() for s in user_skills)
        profile = ProfileModel.get_by_user_id(user_id) or {}
        saved_jobs = JobModel.get_saved_by_user(user_id)
        saved_job_ids = set(j['id'] for j in saved_jobs)

        user_pref_location = (profile.get('preferred_location') or '').lower()
        user_interests = (profile.get('career_interests') or '').lower()
        user_exp = (profile.get('experience_level') or 'Fresher (0-1 yrs)').lower()

        scored_jobs = []

        for job in all_jobs:
            job_id = job['id']
            job_skills = JobModel.get_skills(job_id)
            total_req_skills = len(job_skills)

            # 1. Skill Overlap (Max 50 pts)
            matched_skills = []
            missing_skills = []
            for js in job_skills:
                if js['id'] in user_skill_ids:
                    matched_skills.append(js['skill_name'])
                else:
                    missing_skills.append(js['skill_name'])

            if total_req_skills > 0:
                skill_score = (len(matched_skills) / total_req_skills) * 50.0
            else:
                skill_score = 25.0

            # 2. Role & Title Affinity (Max 25 pts)
            role_score = 5.0
            job_title_lower = job['title'].lower()
            if job_title_lower in user_interests:
                role_score = 25.0
            elif any(word in user_interests for word in job_title_lower.split() if len(word) > 3):
                role_score = 18.0
            else:
                role_score = 10.0

            # 3. Location Match (Max 15 pts)
            location_score = 5.0
            job_loc_lower = job['location'].lower()
            if 'remote' in job_loc_lower and ('remote' in user_pref_location or 'flexible' in user_pref_location):
                location_score = 15.0
            elif any(city in job_loc_lower for city in user_pref_location.split('/') if len(city.strip()) > 3):
                location_score = 15.0
            elif 'remote' in job_loc_lower:
                location_score = 12.0
            else:
                location_score = 6.0

            # 4. Experience Match (Max 10 pts)
            exp_score = 5.0
            job_exp_lower = job['experience_level'].lower()
            if ('fresher' in user_exp and 'fresher' in job_exp_lower) or ('0-1' in user_exp and '0-1' in job_exp_lower):
                exp_score = 10.0
            elif user_exp in job_exp_lower or job_exp_lower in user_exp:
                exp_score = 10.0
            else:
                exp_score = 5.0

            # Final Score Calculation
            total_score = round(min(100.0, max(10.0, skill_score + role_score + location_score + exp_score)), 1)

            # Build transparent justification
            reasons = []
            if matched_skills:
                reasons.append(f"Matched {len(matched_skills)} of {total_req_skills} required skills: {', '.join(matched_skills[:3])}")
            if location_score >= 12.0:
                reasons.append("Location matches your preference")
            if role_score >= 18.0:
                reasons.append("Directly aligns with your career interests")

            scored_jobs.append({
                **job,
                'relevance_score': total_score,
                'matched_skills': matched_skills,
                'missing_skills': missing_skills,
                'match_reasons': ' • '.join(reasons) if reasons else "Compatible entry-level opportunity",
                'is_saved': job_id in saved_job_ids
            })

        # Sort descending by relevance score
        scored_jobs.sort(key=lambda x: x['relevance_score'], reverse=True)
        return scored_jobs[:limit]
