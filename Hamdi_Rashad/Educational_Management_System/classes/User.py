# from RoleMixin import RoleMixin
import sys
import os
import json
import bcrypt
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from education_data import *
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from classes.RoleMixin import RoleMixin
class User( RoleMixin):
    def __init__(self, user_id, username, password, email,role):
        self.user_id = user_id
        self.username = username
        self.password = password 
        self.email = email
        self.role = role
    import bcrypt
    import re
    @RoleMixin.role_check("admin")



    def create_user(user_id, username, password, email, role):
    

 
        user_data_dir = "users"
        user_file = os.path.join(user_data_dir, f"{user_id}.json")

        if os.path.exists(user_file):
              print(f"User with ID {user_id} already exists.")
              return False

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user_data = {
            "user_id": user_id,
            "username": username,
            "password": hashed_password.decode(),  
            "email": email,
            "role": role,
        }

        try:
          with open(user_file, "w") as f:
            json.dump(user_data, f, indent=2)
          return True
        except Exception as e:
          print(f"Error creating user: {e}")
          return False

    @RoleMixin.role_check("admin")
    def delete_user(user_id):
 
        print(f"Error deleting user: {e}")
        return False

    @RoleMixin.role_check("student")
    def register_for_course(self, course_code):



        user_data_dir = "users"
        courses_dir = "courses"

        user_file = os.path.join(user_data_dir, f"{self.user_id}.json")
        course_file = os.path.join(courses_dir, f"{course_code}.json")

  
        if not os.path.exists(course_file):
            print(f"Course {course_code} not found.")
            return False

 
        with open(user_file, "r") as f:
            user_data = json.load(f)
        if course_code in user_data.get("courses", []):
            print(f"You are already registered for course {course_code}.")
            return False

        user_data["courses"].append(course_code)
        with open(user_file, "w") as f:
            json.dump(user_data, f, indent=2)

 

        print(f"Successfully registered for course {course_code}.")
        return True
        
    @RoleMixin.role_check("student")
    def unregister_from_course(self, course_code):
 


        user_data_dir = "users"

        user_file = os.path.join(user_data_dir, f"{self.user_id}.json")

        try:
            with open(user_file, "r+") as f:
                user_data = json.load(f)
                if course_code in user_data["courses"]:
                    user_data["courses"].remove(course_code)
                    f.seek(0)
                    json.dump(user_data, f, indent=2)
                    return True
                else:
                    print(f"You are not registered for course {course_code}.")
                    return False
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error unregistering from course: {e}")
            return False

    @RoleMixin.role_check("student")
    def submit_assignment(self, assignment_id, submission):


    
        user_data_dir = "users"
        assignments_dir = "assignments"

        user_file = os.path.join(user_data_dir, f"{self.user_id}.json")
        assignment_file = os.path.join(assignments_dir, f"{assignment_id}.json")


        if not os.path.exists(assignment_file):
            print(f"Assignment {assignment_id} not found.")
            return False

 
        with open(user_file, "r") as f:
            user_data = json.load(f)
        if assignment_id not in user_data.get("assignments", {}):
            print(f"You are not enrolled in the course for assignment {assignment_id}.")
            return False

   
        submission_dir = os.path.join("submissions", str(self.user_id), str(assignment_id))
        os.makedirs(submission_dir, exist_ok=True)

        # Save submission (replace with appropriate file handling or storage)
        submission_file = os.path.join(submission_dir, f"submission_{time.time()}.txt")  # Example filename
        with open(submission_file, "w") as f:
            f.write(submission)  # Replace with actual submission saving logic

        print(f"Assignment {assignment_id} submitted successfully.")
        return True