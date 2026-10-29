from models.career_model import CareerModel
from models.skill_model import SkillModel
from models.profile_model import ProfileModel

class CareerRecommendationService:
    """
    Transparent, Rule-Based Career Recommendation Engine.
    Combines:
    1. Skill Match Score (40% weight): Checks overlap between student skills and career required skills, weighted by importance.
    2. Assessment Responses (35% weight): Evaluates student's technical interests, problem-solving, activities, and domain affinity.
    3. Profile & Academic Alignment (25% weight): Compares student degree, career interests, and goals with career attributes.
    """

    # Domain affinity weight matrix mapping questionnaire choices to career IDs
    DOMAIN_AFFINITY_MAP = {
        'data_analytics': {1: 1.0, 10: 0.7, 5: 0.6, 9: 0.5},
        'python_programming': {2: 1.0, 10: 0.8, 1: 0.7, 3: 0.6},
        'software_engineering': {3: 1.0, 2: 0.8, 4: 0.7, 10: 0.6},
        'web_development': {4: 1.0, 6: 0.6, 2: 0.5, 3: 0.5},
        'business_systems': {5: 1.0, 1: 0.6, 8: 0.5},
        'ui_ux_design': {6: 1.0, 4: 0.6, 8: 0.5},
        'cybersecurity': {7: 1.0, 9: 0.6, 3: 0.5},
        'digital_marketing': {8: 1.0, 6: 0.5, 5: 0.4},
        'database_admin': {9: 1.0, 1: 0.7, 2: 0.5, 7: 0.5},
        'machine_learning': {10: 1.0, 1: 0.8, 2: 0.7, 3: 0.6}
    }

    @classmethod
    def evaluate(cls, user_id, assessment_responses=None):
        """
        Runs recommendation calculation for a user.
        Returns a list of scored career recommendations sorted from highest to lowest match score.
        """
        careers = CareerModel.get_all(active_only=True)
        user_skills = SkillModel.get_user_skills(user_id)
        user_skill_ids = {s['id']: s.get('proficiency_level', 'Intermediate') for s in user_skills}
        profile = ProfileModel.get_by_user_id(user_id) or {}

        recommendations = []

        for career in careers:
            career_id = career['id']
            career_skills = CareerModel.get_skills(career_id)

            # ---------------------------------------------------------
            # 1. Skill Match Component (Max 40 Points)
            # ---------------------------------------------------------
            skill_score = 0.0
            reasons = []
            matched_skills = []
            missing_skills = []

            importance_weights = {'High': 3.0, 'Medium': 2.0, 'Low': 1.0}
            total_possible_skill_pts = 0.0
            earned_skill_pts = 0.0

            for cs in career_skills:
                weight = importance_weights.get(cs['importance_level'], 2.0)
                total_possible_skill_pts += weight

                if cs['id'] in user_skill_ids:
                    # User possesses this skill
                    proficiency = user_skill_ids[cs['id']]
                    prof_multiplier = 1.0 if proficiency == 'Advanced' else (0.85 if proficiency == 'Intermediate' else 0.6)
                    earned_skill_pts += weight * prof_multiplier
                    matched_skills.append(cs['skill_name'])
                else:
                    missing_skills.append({
                        'id': cs['id'],
                        'name': cs['skill_name'],
                        'importance': cs['importance_level']
                    })

            if total_possible_skill_pts > 0:
                skill_ratio = earned_skill_pts / total_possible_skill_pts
                skill_score = skill_ratio * 40.0
            else:
                skill_score = 20.0 # Neutral baseline if no skills registered

            if matched_skills:
                reasons.append(f"You already possess {len(matched_skills)} key skills: {', '.join(matched_skills[:3])}.")

            # ---------------------------------------------------------
            # 2. Assessment Responses Component (Max 35 Points)
            # ---------------------------------------------------------
            assessment_score = 15.0 # Baseline if assessment not taken
            if assessment_responses:
                raw_score = 0.0
                max_raw = 0.0

                # Check preferred domain
                preferred_domain = assessment_responses.get('preferred_domain')
                if preferred_domain in cls.DOMAIN_AFFINITY_MAP:
                    affinity = cls.DOMAIN_AFFINITY_MAP[preferred_domain].get(career_id, 0.2)
                    raw_score += affinity * 15.0
                    if affinity >= 0.8:
                        reasons.append(f"Direct alignment with your selected interest in {preferred_domain.replace('_', ' ').title()}.")
                else:
                    raw_score += 7.0
                max_raw += 15.0

                # Check preferred work activity
                activity = assessment_responses.get('work_activity')
                activity_score = cls._score_activity(activity, career_id)
                raw_score += activity_score * 10.0
                max_raw += 10.0

                # Check analytical / problem solving affinity
                analytical = assessment_responses.get('analytical_preference', 'moderate')
                if analytical == 'high' and career_id in (1, 3, 7, 9, 10):
                    raw_score += 10.0
                elif analytical == 'creative' and career_id in (4, 6, 8):
                    raw_score += 10.0
                else:
                    raw_score += 6.0
                max_raw += 10.0

                assessment_score = (raw_score / max_raw) * 35.0

            # ---------------------------------------------------------
            # 3. Profile & Academic Alignment Component (Max 25 Points)
            # ---------------------------------------------------------
            profile_score = 10.0 # Baseline
            profile_factors = 0.0
            max_profile_factors = 25.0

            # Degree relevance
            degree_text = (profile.get('degree') or '') + ' ' + (profile.get('specialization') or '')
            degree_text_lower = degree_text.lower()
            if any(k in degree_text_lower for k in ['computer', 'cs', 'it', 'software', 'data', 'information']):
                profile_factors += 12.0
            elif any(k in degree_text_lower for k in ['business', 'management', 'bba', 'mba', 'commerce']):
                if career_id in (1, 5, 8):
                    profile_factors += 12.0
                else:
                    profile_factors += 6.0
            elif any(k in degree_text_lower for k in ['design', 'arts', 'media']):
                if career_id in (6, 8):
                    profile_factors += 12.0
                else:
                    profile_factors += 5.0
            else:
                profile_factors += 7.0

            # Career interests keyword match
            interests_text = (profile.get('career_interests') or '').lower()
            if career['title'].lower() in interests_text:
                profile_factors += 13.0
                reasons.append(f"Explicitly matches your stated interest in '{career['title']}'.")
            elif any(word in interests_text for word in career['title'].lower().split()):
                profile_factors += 8.0
            else:
                profile_factors += 4.0

            profile_score = (profile_factors / max_profile_factors) * 25.0

            # ---------------------------------------------------------
            # Final Aggregated Match Score (Clamped to 0 - 100)
            # ---------------------------------------------------------
            final_score = round(min(100.0, max(15.0, skill_score + assessment_score + profile_score)), 1)

            if not reasons:
                reasons.append("Good foundational opportunity based on current technology trends.")

            recommendations.append({
                'career_id': career_id,
                'career_title': career['title'],
                'career_description': career['description'],
                'required_education': career['required_education'],
                'entry_level_roles': career['entry_level_roles'],
                'match_score': final_score,
                'skill_match_score': round(skill_score, 1),
                'assessment_score': round(assessment_score, 1),
                'profile_score': round(profile_score, 1),
                'matched_skills': matched_skills,
                'missing_skills': missing_skills,
                'recommendation_reason': ' | '.join(reasons)
            })

        # Sort recommendations descending by match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations

    @staticmethod
    def _score_activity(activity, career_id):
        """Scores preferred day-to-day activity against career role."""
        if not activity:
            return 0.5
        activity_map = {
            'coding_logic': [2, 3, 4, 10],
            'data_number_crunching': [1, 9, 10, 5],
            'designing_user_interfaces': [6, 4, 8],
            'security_investigation': [7, 9],
            'business_communication': [5, 8, 1],
            'marketing_strategy': [8, 5, 6]
        }
        target_ids = activity_map.get(activity, [])
        if career_id in target_ids:
            return 1.0
        return 0.4
