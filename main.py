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

    # the header string that will always be written to the csv file
    course_string = 'ID,Course Name,Course Level,Age Group,Sessions,Course Fee,Registered'
    schedule_string = 'ID,Day,Start Time,End Time,Registered'
    student_string = 'ID,Student Name,Date of Birth,Parent Name,Parent Email,Phone Number,Registered'
    term_string = 'Registration ID,Term ID,Course Name,Student Name,Sessions,Course Fee,Start Date,End Date,' \
                            'Discount Type,Discount Amount,Payment Method,Amount Paid,Payment Date,Account Name,Status'
    

    # 2-D array that stores all values
    all_entities_array = [course_names, age_groups, courses, schedules, students, registrations, terms, user_accounts]
    file_handler.binary_file_writer(all_entities_array)

    # writing the final string onto the csv files
    file_handler.text_file_writer(course_string, 'courses')
    file_handler.text_file_writer(schedule_string, 'schedules')
    file_handler.text_file_writer(student_string, 'students')
    file_handler.text_file_writer(term_string, 'terms')


root = Tk()
application = login.Login(root)
root.mainloop()