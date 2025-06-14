from datetime import datetime, time
from models.activity import Lecture, Course

'''
Add some initital activities, chose dict for easier access later (and for cases when we skip an ID)
'''
activities = {}
activities[0] = Course(0, "Chemistry", datetime(2025, 3, 24, 0, 0), datetime(2025, 7, 1, 0, 0), {0: (time(14, 0), time(15, 0)), 1: (time(17, 0), time(20, 0))})
activities[1] = Lecture(1, "Intr. to Quantum Physics", datetime(2025, 3, 25, 16, 0), datetime(2025, 3, 25, 19, 0))
activities[2] = Lecture(2, "Astronomy 101", datetime(2025, 3, 16, 14, 0), datetime(2025, 3, 16, 18, 0))
activities[3] = Course(3, "Philosophy", datetime(2025, 2, 12, 0, 0), datetime(2025, 12, 10, 0, 0), {0: (time(14, 0), time(17, 0)), 3: (time(13, 0), time(18, 0))})


'''
Base activity service class
'''
class ActivityService:
    def get_activities(self):
        return list(activities.values())
    
    def get_activities_json(self):
        return [activity.toJSON() for activity in activities.values()]