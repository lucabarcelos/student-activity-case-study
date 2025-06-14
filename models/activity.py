from datetime import datetime, date

'''
I ended up not using this but it was an option for the JSON return depending on the app that would consume the API
'''
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


'''
Base Lecture class
Attributes:
    - ID
    - Title
    - Start date and time
    - End date and time
'''
class Lecture:
    def __init__(self, id, title, start_datetime, end_datetime):
        self.id = id
        self.title = title
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

    '''
    Determines if 2 activities overlap
    '''
    def has_conflict(self, activity):
        '''
        Two separate logics depending on wether we are comparing against a Lecture or a Course
            - Lecture vs Lecture: Check if there is overlap between their datetime ranges
            - Course vs Lecture: First check if lecture is in one of the weekdays when the course happens, and if the lecture is happening within the period of the course, then check for specific times within the day

            Difference between two dates is done b
        '''
        seconds_in_day = 24 * 60 * 60

        if isinstance(activity, Lecture):
            last_start = max(self.start_datetime, activity.start_datetime)
            first_end = min(self.end_datetime, activity.end_datetime)
            print("last start:", last_start)
            print("first end:", first_end)
            print("first_end-last_start:", ((first_end-last_start).days * seconds_in_day + (first_end-last_start).seconds))
            if ((first_end-last_start).days * seconds_in_day + (first_end-last_start).seconds) > 0:
                return True
            
        if isinstance(activity, Course):
            if self.start_datetime.weekday() in activity.times.keys() and self.start_datetime >= activity.start_datetime and self.end_datetime <= activity.end_datetime:
                activity_start_datetime = datetime(self.start_datetime.year, self.start_datetime.month, self.start_datetime.day, activity.times[self.start_datetime.weekday()][0].hour, activity.times[self.start_datetime.weekday()][0].minute)
                activity_end_datetime = datetime(self.start_datetime.year, self.start_datetime.month, self.start_datetime.day, activity.times[self.start_datetime.weekday()][1].hour, activity.times[self.start_datetime.weekday()][1].minute)
                last_start = max(self.start_datetime, activity_start_datetime)
                first_end = min(self.end_datetime, activity_end_datetime)

                if ((first_end-last_start).days * seconds_in_day + (first_end-last_start).seconds) > 0:
                    return True
            
        return False
    
    '''
    Needed for returning object in JSON format
    '''
    def toJSON(self):
        json_activity = {
            "id": self.id,
            "title": self.title,
            "start_datetime": str(self.start_datetime),
            "end_datetime": str(self.end_datetime)
        }

        return json_activity


'''
Base Course class
Attributes:
     - ID
     - Title
     - Start Date
     - End Date
     - Weekdays and times of each class
'''
class Course:
    def __init__(self, id, title, start_datetime, end_datetime, times):
        self.id = id
        self.title = title
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.times = times

    '''
    Determines if 2 activities overlap
    '''
    def has_conflict(self, activity):
        '''
        Two separate logics depending on wether we are comparing against a Lecture or a Course
            - Course vs Lecture: First check if lecture is in one of the weekdays when the course happens, and if the lecture is happening within the period of the course, then check for specific times within the day
            - Course vs Course: First check which weekdays overlap between courses and if their periods overlap, if so, check times within each overlapping day
        '''
        seconds_in_day = 24 * 60 * 60

        if isinstance(activity, Lecture):
            if activity.start_datetime.weekday() in self.times.keys() and activity.start_datetime >= self.start_datetime and activity.end_datetime <= self.end_datetime:
                self_start_datetime = datetime(activity.start_datetime.year, activity.start_datetime.month, activity.start_datetime.day, self.times[activity.start_datetime.weekday()][0].hour, self.times[activity.start_datetime.weekday()][0].minute)
                self_end_datetime = datetime(activity.start_datetime.year, activity.start_datetime.month, activity.start_datetime.day, self.times[activity.start_datetime.weekday()][1].hour, self.times[activity.start_datetime.weekday()][1].minute)
                last_start = max(activity.start_datetime, self_start_datetime)
                first_end = min(activity.end_datetime, self_end_datetime)

                if ((first_end-last_start).days * seconds_in_day + (first_end-last_start).seconds) > 0:
                    return True
            
        if isinstance(activity, Course):
            overlapping_days = list(set(list(self.times.keys())).intersection(list(activity.times.keys())))
            last_start = max(self.start_datetime, activity.start_datetime)
            first_end = min(self.end_datetime, activity.end_datetime)
            if overlapping_days and ((first_end-last_start).days * seconds_in_day + (first_end-last_start).seconds) > 0:
                for day in overlapping_days:
                    last_time_start = max(self.times[day][0], activity.times[day][0])
                    first_time_end = min(self.times[day][1], activity.times[day][1])
                    if ((first_time_end-last_time_start).days * seconds_in_day + (first_time_end-last_time_start).seconds) > 0:
                        return True
            
        return False
    
    '''
    Needed for returning object in JSON format
    '''
    def toJSON(self):
        weekdays_times = {}

        for (day, times) in self.times.items():
            weekdays_times[day] = {
                "start": str(times[0]),
                "end": str(times[1])
            }

        json_activity = {
            "id": self.id,
            "title": self.title,
            "start_datetime": str(self.start_datetime),
            "end_datetime": str(self.end_datetime),
            "weekdays_times": weekdays_times
        }

        return json_activity
    

Activity = Lecture | Course