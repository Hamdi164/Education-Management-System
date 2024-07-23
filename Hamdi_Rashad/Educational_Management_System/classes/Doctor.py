from Courses import Course
from RoleMixin import  RoleMixin
import sys
import json
import os
from os import path
from RoleMixin import RoleMixin
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from education_data import *
from User import User
class Doctor(User):
    def __init__(self, user_id, username, password, email,role, courses=[]):
        super().__init__(user_id, username, password, email)
        self.courses = courses

    
    @RoleMixin.role_check("doctor")
    def edit_course(self, course_code, updates):
        courses_dir = "courses"
        course_file = os.path.join(courses_dir, f"{course_code}.json")

        if not os.path.exists(course_file):
            raise ValueError(f"Course with code {course_code} not found.")

        try:
            with open(course_file, "r+") as f:
                course_data = json.load(f)
                course_data.update(updates)
                f.seek(0)
                json.dump(course_data, f, indent=2)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error editing course: {e}")
            return False

        return True
 