from models.student import Student
from services.activity_service import ActivityService
import hashlib

'''
Add some initial students, chose a dict for easier access later (not having for loops)
'''
students = {}
students["student1"] = Student("student1", "698dc19d489c4e4db73e28a713eab07b")
students["student2"] = Student("student2", "38851536d87701d2191990e24a7f8d4e")

'''
Get all activities and store in dict to pass onto student.enroll_activity method
'''
activity_service = ActivityService()
activities = {}

for activity in activity_service.get_activities():
    activities[activity.id] = activity


'''
Base student service class
'''
class StudentService:
    def authenticate(self, student_id, password):
        return students[student_id].authenticate(hashlib.md5(password.encode()).hexdigest())
    
    def enroll_activity(self, student_id, activity_list):
        activities_to_enroll = [activities[activity_id] for activity_id in activity_list]
        return students[student_id].enroll_activity(activities_to_enroll), 200
    
    def create_student(self, student_id, password):
        if student_id in students.keys():
            return "Student ID already present", 500
        
        students[student_id] = Student(student_id, hashlib.md5(password.encode()).hexdigest())

        return "Student created", 201
    
    def list_student_activities(self, student_id):
        return students[student_id].list_student_activities()