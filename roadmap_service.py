from models.roadmap_model import RoadmapModel
from models.career_model import CareerModel

class RoadmapService:
    """
    Manages structured learning roadmaps, stage progressions, and user checklist state.
    """

    @classmethod
    def get_roadmap_details(cls, roadmap_id, user_id=None):
        """
        Fetches detailed roadmap data and merges user's checklist progress if user is authenticated.
        """
        roadmap = RoadmapModel.get_by_id(roadmap_id)
        if not roadmap:
            return None

        completed_steps = set()
        progress_percentage = 0.0
        status = 'Not Enrolled'

        if user_id:
            completed_steps = RoadmapModel.get_completed_steps(user_id, roadmap_id)
            user_roadmaps = RoadmapModel.get_user_saved_roadmaps(user_id)
            for ur in user_roadmaps:
                if ur['roadmap_id'] == roadmap_id:
                    progress_percentage = float(ur['progress_percentage'])
                    status = ur['status']
                    break

        parsed = roadmap.get('parsed_content', {})

        return {
            'roadmap': roadmap,
            'stages': parsed.get('stages', []),
            'projects': parsed.get('projects', []),
            'interview_topics': parsed.get('interview_topics', []),
            'checklist': parsed.get('checklist', []),
            'completed_steps': completed_steps,
            'progress_percentage': progress_percentage,
            'status': status
        }
