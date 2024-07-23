from User import User 
from Courses import Course
import sys
import os
import json
import bcrypt
from os import path
from Doctor import Doctor
from AdminUser import AdminUser
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from education_data import *
import re
import os
import json

def login():

  username = input("Username: ")
  password = input("Password: ")


  user_data_dir = "users"
  user_file = os.path.join(user_data_dir, f"{username}.json")

  if not os.path.exists(user_file):
    print("User not found.")
    return None

  try:
    with open(user_file, "r") as f:
      user_data = json.load(f)

    if user_data["password"] == password:
    
      user_id = user_data["user_id"]
      role = user_data["role"]
      email = user_data["email"]
    
      
      if role == "student":
        user = User(user_id, username, password, email, []) 
      elif role == "doctor":
        user = Doctor(user_id, username, password, email)
      elif role == "admin":
        user = admin_user(user_id, username, password, email)
      else:
        print(f"Invalid user role: {role}")
        return None
      return user
    else:
      print("Invalid username or password.")
      return None
  except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error logging in: {e}")
    return None


def signup():

  username = input("Username: ")
  password = input("Password: ")
  password2 = input("Confirm password: ")
  email = input("Email: ")
  email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]{2,}$"
  if not bool(re.match(email_regex, email)):
    raise ValueError("Invalid email address")

  role = input("Role (student, doctor, admin): ")
  user_id = input("user_id (unique identifier): ")


  user_data_dir = "users"
  user_file = os.path.join(user_data_dir, f"{user_id}.json")

  if os.path.exists(user_file):
    print("User with ID already exists.")
    return None

  if password != password2:
    print("Passwords do not match.")
    return None

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

    if role == "student":

      user = Student(user_id, username, password, email, [])

    elif role == "doctor":
      user = Doctor(user_id, username, password, email)
    elif role == "admin":
      user = admin_user(user_id, username, password, email)
    else:
      print(f"Invalid user role: {role}")
      return None
    return user
  except Exception as e:
    print(f"Error creating user: {e}")
    return None

def main():
    """Prompts user for login/signup or exit."""
    while True:
        print("\nWelcome to the Education System!")
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            user = login()
            if user:
                
                menu = main_menu(user)  
                menu.run()  
                break  
            else:
                print("Login failed.")
        elif choice == '2':
            new_user = signup()
            if new_user:
                print(f"User '{new_user.username}' created successfully.")
                break
            else:
                print("Error creating user.")
                break
        elif choice == '3':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
def main_menu(user):
    """Presents menu options based on user role and returns the appropriate menu class."""
    try:
      conn = get_connection()
      if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM Users WHERE userid = ?", (user_id,))
        user_data = cursor.fetchone()
    except Exception as err:
      conn.rollback()  
    finally:
      conn.close() 
    if isinstance(user, User):
        print("\nStudent Menu:")
        print("1. Register for Course")
        print("2. Unregister from Course")
        print("3. View Registered Courses")
        print("4. View Assignments and Grades")
        print("5. Submit Assignment")
        return StudentMenu(user)  
    elif isinstance(user, Doctor):
        print("\nDoctor Menu:")
        print("1. Create Course")
        print("2. View Courses")
        print("3. Edit Course")
        return DoctorMenu(user)  
    elif isinstance(user, AdminUser):
        print("\nAdmin Menu:")
        print("1. Create User")
        print("2. Delete User")
        return AdminMenu(user)  
    else:
        print("Invalid user role.")
        return None  

class StudentMenu:
    def __init__(self, user):
        self.user = user

    def run(self):

      while True:
          choice = input("Enter your choice (1-5) or 'q' to quit: ")
          if choice == 'q':
              break
          elif choice == '1':
              course_name=input("input course name ")
              course_code=input("input course code ")
              start_date=input("input start date ")
              end_date=input("input end date ")
              unregister_deadline=input("input unregister deadline ")
              course=Course(course_name,course_code,start_date,end_date,unregister_deadline)
              self.register_for_course(course)
          elif choice == '2':
              course=input("please enter the course ")
              self.unregister_from_course(course)
          elif choice == '3':
              self.get_all_courses()
          elif choice == '4':

              self.get_assignments_and_grades()
          elif choice == '5':
              assignment=input("please enter the assignment ")
              solution=input("please enter the solution")            
              self.submit_assignment(assignment,solution)
          else:
              print("Invalid choice.")
class DoctorMenu:
    def __init__(self, user):
        self.user = user

    def run(self):
        """Provides options for doctor functionalities."""
        while True:
            choice = input("Enter your choice (1-3) or 'q' to quit: ")
            if choice == 'q':
                break
            elif choice == '1':
                course_name=input("please enter the course name")
                course_code=input("pleas enter the course code ")
                start_date=input("enter the start data")
                end_date=input("enter the end date")
                unregister_deadline=input("enter unregister deadline")
                self.create_course( course_name, course_code, start_date, end_date, unregister_deadline)
            elif choice == '2':
                self.view_courses()
            elif choice == '3':
                course_code=input("please enter the course code")
                self.edit_course(course_code)
            else:
                print("Invalid choice.")

class AdminMenu:
    def __init__(self, user):
        self.user = user

    def run(self):
        """Provides options for admin functionalities."""
        while True:
            choice = input("Enter your choice (1-2) or 'q' to quit: ")
            if choice == 'q':
                break
            elif choice == '1':
                user_id=input("enter user id ")
                user_name=input("enter user name ")
                password=input("enter the password")
                email=input("enter the email")
                role=input("enter the role")
                self.create_user(user_id, username, password, email,role)
            elif choice == '2':
                user_id=input("enter user id ")
                self.delete_user(self,user_id)
            else:
                print("Invalid choice.")
if __name__ == "__main__":
    main()