from flask import Flask, request
from flask_cors import CORS
from services.activity_service import ActivityService
from services.student_service import StudentService


app = Flask(__name__)

'''
Some clients require this option to work (needed this for the svelte project I mentioned)
'''
CORS(app)

activity_service = ActivityService()
student_service = StudentService()

@app.route('/')
def index():
    return 'BCG-X Case Study'

'''
Returns list of possible acitivities
'''
@app.route('/get_activities', methods=['GET'])
def get_activities():
    return activity_service.get_activities_json()

'''
Receives:
    - Student ID
    - password
    - List of activities to enroll, in order of priority (important in case of conflicts)

Returns list of activitiy ids not enrolled due to conflict
'''
@app.route('/enroll_activity', methods=['POST'])
def enroll_activity():
    request_data = request.get_json()

    if "student_id" not in request_data.keys() or "password" not in request_data.keys() or "activity_ids" not in request_data.keys():
        return 'Request must contain fields "student_id", "password", "activity_ids"', 400

    if not student_service.authenticate(request_data["student_id"], request_data["password"]):
        return "Wrong password or ID", 401

    return student_service.enroll_activity(request_data["student_id"], request_data["activity_ids"])

'''
Receives:
    - Student ID
    - password

Returns 201 if user was successfully created, 500 if user already exists
'''
@app.route('/create_student', methods=['POST'])
def create_student():
    request_data = request.get_json()

    if "student_id" not in request_data.keys() or "password" not in request_data.keys():
        return 'Request must contain fields "student_id", "password"', 400

    return student_service.create_student(request_data["student_id"], request_data["password"])

'''
Receives:
    - Student ID
    - password

Returns list of activities if credentials match, 401 otherwise
'''
@app.route('/list_student_activities', methods=['GET'])
def list_student_activities():
    request_data = request.get_json()

    if "student_id" not in request_data.keys() or "password" not in request_data.keys():
        return 'Request must contain fields "student_id", "password"', 400

    if not student_service.authenticate(request_data["student_id"], request_data["password"]):
        return "Wrong password or ID", 401

    return student_service.list_student_activities(request_data["student_id"])

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")