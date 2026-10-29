from models.career_model import CareerModel
from models.skill_model import SkillModel
from models.roadmap_model import RoadmapModel

class SkillGapService:
    """
    Performs comprehensive skill gap analysis between a student's current inventory
    and the requirements of any target career path.
    """

    @classmethod
    def analyze(cls, user_id, career_id):
        """
        Analyzes skill gaps for a user against a target career.
        Returns:
            - career: Career profile
            - possessed_skills: Skills the student already has
            - missing_skills: Skills the student still needs, ranked by importance
            - coverage_percentage: Current readiness percentage
            - prioritized_learning: Priority action items
            - recommended_projects: Hands-on project suggestions
            - roadmap: Associated learning roadmap if available
        """
        career = CareerModel.get_by_id(career_id)
        if not career:
            return None

        career_skills = CareerModel.get_skills(career_id)
        user_skills = SkillModel.get_user_skills(user_id)

        user_skill_map = {s['id']: s for s in user_skills}

        possessed = []
        missing = []

        for cs in career_skills:
            if cs['id'] in user_skill_map:
                u_skill = user_skill_map[cs['id']]
                possessed.append({
                    'id': cs['id'],
                    'name': cs['skill_name'],
                    'category': cs['skill_category'],
                    'importance': cs['importance_level'],
                    'proficiency': u_skill.get('proficiency_level', 'Intermediate')
                })
            else:
                missing.append({
                    'id': cs['id'],
                    'name': cs['skill_name'],
                    'category': cs['skill_category'],
                    'importance': cs['importance_level']
                })

        # Sort missing by importance (High first)
        importance_rank = {'High': 1, 'Medium': 2, 'Low': 3}
        missing.sort(key=lambda x: importance_rank.get(x['importance'], 4))

        total_req = len(career_skills)
        coverage_pct = round((len(possessed) / total_req * 100), 1) if total_req > 0 else 100.0

        # Suggested projects and roadmap
        roadmap = RoadmapModel.get_by_career_id(career_id)
        recommended_projects = []
        if roadmap and 'parsed_content' in roadmap:
            recommended_projects = roadmap['parsed_content'].get('projects', [])

        return {
            'career': career,
            'possessed_skills': possessed,
            'missing_skills': missing,
            'total_required': total_req,
            'possessed_count': len(possessed),
            'missing_count': len(missing),
            'coverage_percentage': coverage_pct,
            'roadmap': roadmap,
            'recommended_projects': recommended_projects
        }
