from tkinter import *
import login
import file_handler


# should be called when the system needs to be reset.
def reset():
    # initialising all arrays if they dont already exist
    course_names = ['Chess Online Regular Course', 'Scratch Coding Regular Course', 'Lego Robotics Online Course']
    age_groups = ['4-6', '7-9', '10-13']

    # the business entities arrays that will store user-defined objects
    courses, schedules, students, registrations, terms = [], [], [], [], []

    # hash table that stores usernames (keys) and passwords (values)
    user_accounts = {}

    # 2-D array that stores all values
    all_entities_array = [course_names, age_groups, courses, schedules, students, registrations, terms, user_accounts]
    file_handler.binary_file_writer(all_entities_array)


root = Tk()
application = login.Login(root)
root.mainloop()