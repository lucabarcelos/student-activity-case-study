## Installation

1. Clone the repository:

```bash
git clone https://github.com/lucabarcelos/sudent-activity-case-study.git
cd sudent-activity-case-study
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python app.py
```

The API will be running at `http://localhost:5000`

---

##  Running Tests

Tests are written using `pytest`. To run the tests:

```bash
pytest
```

---

##  Curl tests used

* curl localhost:5000/get_activities
* curl -H 'Content-Type: application/json' \
      -d '{ "student_id":"student1","password":"teste", "activity_ids": [1,0,3]}' \
      -X POST \
      localhost:5000/enroll_activity
* curl -H 'Content-Type: application/json' \
      -d '{ "student_id":"student3","password":"teste3"}' \
      -X POST \
      localhost:5000/create_student
* curl -H 'Content-Type: application/json' \
      -d '{ "student_id":"student3","password":"teste3", "activity_ids": [2,3]}' \
      -X POST \
      localhost:5000/enroll_activity
* curl -H 'Content-Type: application/json' \
      -d '{ "student_id":"student3","password":"teste3"}' \
      -X GET \
      localhost:5000/list_student_activities

---

## Requirements

* Python 3.7+
* Flask
* Flask-CORS
* pytest (for testing)
