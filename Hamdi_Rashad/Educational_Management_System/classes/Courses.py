import sys
import json
import os
from os import path
from RoleMixin import RoleMixin
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from education_data import *
class Course:
    def __init__(self, course_name, course_code, start_date, end_date, unregister_deadline):
        self.course_name = course_name
        self.course_code = course_code
        self.start_date = start_date
        self.end_date = end_date
        self.unregister_deadline = unregister_deadline

    @RoleMixin.role_check("doctor")
    def create_course(self):
        course_data = {
            "course_name": self.course_name,
            "course_code": self.course_code,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "unregister_deadline": self.unregister_deadline
        }


        courses_dir = "courses"
        os.makedirs(courses_dir, exist_ok=True)


        course_file = os.path.join(courses_dir, f"{self.course_code}.json")
        if os.path.exists(course_file):
            raise ValueError(f"Course with code {self.course_code} already exists.")

        try:
            with open(course_file, "w") as f:
                json.dump(course_data, f, indent=2)
            print(f"Course {self.course_code} created successfully.")
        except Exception as e:
            print(f"Error creating course: {e}")

    @staticmethod
    def get_course(course_code):
        courses_dir = "courses"
        course_file = os.path.join(courses_dir, f"{course_code}.json")

        if not os.path.exists(course_file):
            return None

        try:
            with open(course_file, "r") as f:
                course_data = json.load(f)
            return Course(**course_data)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error retrieving course: {e}")
            return None