'''
Base Student class
'''
class Student:
    def __init__(self, student_id, password):
        self.student_id = student_id
        self.password = password
        self.enrolled_activities = {}

    '''
    Password comes pre-hashed from service
    '''
    def authenticate(self, password):
        return self.password == password
    

    def enroll_activity(self, new_acitivities):
        '''
        Check for time conflicts with other enrolled activities, returns a tuple (Bool, []) indicating if all activities were enrolled, and if not, which ones weren't
        '''
        conflicted = []

        for new_activity in new_acitivities:
            '''
            If activity is already enrolled
            '''
            if new_activity.id in self.enrolled_activities.keys():
                conflicted.append(new_activity.id)
                continue

            for activity in self.enrolled_activities.values():
                if activity.has_conflict(new_activity):
                    conflicted.append(new_activity.id)
                    break
            
            if new_activity.id not in conflicted:
                self.enrolled_activities[new_activity.id] = new_activity
        
        return conflicted
    
    def list_student_activities(self):
        return [activity.toJSON() for activity in self.enrolled_activities.values()]
