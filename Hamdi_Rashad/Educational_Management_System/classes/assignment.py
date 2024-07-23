import sys
import json
import os
from os import path
from RoleMixin import RoleMixin
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from education_data import *
class Assignment:
    def __init__(self,name, assignment_id, course_id, due_date):
        self.name=name
        self.assignment_id = assignment_id
        self.due_date = due_date
        self.course_id = course_id

    @RoleMixin.role_check("doctor")
    def set_assignment(self, name, assignment_id, course_id, due_date):
        assignment_data = {
            "name": name,
            "assignment_id": assignment_id,
            "course_id": course_id,
            "due_date": due_date
        }

  
        assignment_dir = "assignments"
        os.makedirs(assignment_dir, exist_ok=True)


        assignment_file = os.path.join(assignment_dir, f"{assignment_id}.json")

        try:
            with open(assignment_file, "w") as f:
                json.dump(assignment_data, f, indent=2)
            print(f"Assignment {assignment_id} created successfully.")
        except Exception as e:
            print(f"Error creating assignment: {e}")

    @RoleMixin.role_check("doctor")
    def view_assignments(self, course_code=None):
        assignments_dir = "assignments"
        assignments = []

        if not os.path.exists(assignments_dir):
            print("No assignments found.")
            return

        for filename in os.listdir(assignments_dir):
            file_path = os.path.join(assignments_dir, filename)
            try:
                with open(file_path, "r") as f:
                    assignment_data = json.load(f)
                    if course_code is None or assignment_data["course_id"] == course_code:
                        assignments.append(assignment_data)
            except (FileNotFoundError, json.JSONDecodeError):
                print(f"Error reading assignment file: {file_path}")

        if not assignments:
            print("No assignments found for the specified course.")
            return

        print("Assignments:")
        for assignment in assignments:
            print(f"ID: {assignment['assignment_id']}, Name: {assignment['name']}, Course: {assignment['course_id']}, Due Date: {assignment['due_date']}")