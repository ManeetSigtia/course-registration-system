from tkinter import Label, Button, Frame, PhotoImage
import os

import style
from widgets import Widgets
from file_handler import binary_file_reader, text_file_writer


class ReportFrame(Widgets):
    # inheriting from the Widgets class
    def __init__(self, root):
        # creating a frame in which all widgets will be added
        self.__frame = Frame(root, width=style.frame_width, height=style.frame_height)

        # image that will be used for the search button
        self.search_image = PhotoImage(file=os.path.join(os.path.dirname(__file__), "images", "search_1.png"))

        # array containing the different options to view the details
        self.select_search_options_array = ['Student', 'Schedule', 'Course']

        # array containing the days of the week
        self.days_array = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        # initialising string that will be used in the making of the pop-up window
        self.save_window_title = 'Save Details?'
        self.save_window_label = 'Are you sure you want to file details?'

        self.success_window_title = 'Successful submission'
        self.success_window_text = 'The details have been successfully saved.'

        # calling the read function from file handler
        self.all_entities_array = binary_file_reader()
        self.course_names_array = self.all_entities_array[0]

        # preseting dropdown search criteria. This can be later changed by the user.
        self.select_search_dropdown_content = 'Student'

        # calling this function to place all created widgets on screen
        self.__frame_elements()

    # public function used to retrieve the private attribute 'frame'
    def get_frame(self):
        return self.__frame

    # function contaning everything to do with making the screen
    def __frame_elements(self):
        # creating a label for the report frame
        Label(self.__frame, text='Search by: ', font=(style.main_font, 14), fg=style.orange).place(x=200, y=20)

        # creating dropdowns so that the user has limited input for certain fields
        self.course_search_dropdown = self.make_dropdown(self.__frame, values=['None'] + self.course_names_array,
                                                         font=(style.main_font, 11), initial='', x=350, y=25, width=20)
        self.schedule_search_dropdown = self.make_dropdown(self.__frame, values=['None'] + self.days_array,
                                                           font=(style.main_font, 11), initial='', x=350, y=25, width=20)
        self.select_search_dropdown = self.make_dropdown(self.__frame, values=self.select_search_options_array,
                                                         font=(style.main_font, 11), initial='Student', x=600, y=25,
                                                         width=20)
        self.select_search_dropdown.bind("<<ComboboxSelected>>", self.__identify_search_criteria)

        # creating an entrybox so that the user can enter a student name as a search criteria
        self.student_search_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 11), x=350, y=25, width=25,
                                                          borderwidth=3)

        # arrays containing the title of the columns for each of the course, schedule, and student tables
        self.student_table_columns = ["", "ID", "Student Name", "Date of Birth", "Parent Name", "Parent Email",
                                      "Phone Number", "Registered"]
        self.schedule_table_columns = ["", "ID", "Day", "Start Time", "End Time", "Registered"]
        self.course_table_columns = ["", "ID", "Course Name", "Course Level", "Age Group", "Sessions", "Course Fee",
                                     "Registered"]

        # arrays containing the width of each column for each of the course, schedule, and student tables
        self.student_table_columns_width = [0, 150, 160, 150, 160, 200, 140, 130]
        self.schedule_table_columns_width = [0, 200, 250, 200, 200, 240]
        self.course_table_columns_width = [0, 150, 360, 130, 120, 100, 130, 100]

        # making table that will be used to show the individual details
        self.report_table = self.make_table(self.__frame, 200, 100, self.student_table_columns_width,
                                            self.student_table_columns, height=13)
        self.striped_rows(self.report_table)

        # making a button to allow user to search and display details on the table
        self.search_button = Button(self.__frame, image=self.search_image, width=20, command=self.__insert_data,
                                    state='normal')
        self.search_button.place(x=800, y=22)

        # making a button to allow users to export reports to a text file
        self.save_text_button = self.make_button(self.__frame, text="Save", font=(style.main_font, 15), width=7,
                                                 command=lambda: self.make_confirm_window(self.save_window_title,
                                                                                          self.save_window_label,
                                                                                          self.__save_in_textfile),
                                                 state='normal', x=725, y=500)

    # function to create table based on search criteria
    def __identify_search_criteria(self, event):
        # if the user wants to see student details
        if self.select_search_dropdown.get() == 'Student':
            self.__destroy_search_fields()

            # making an entrybox so that users can search for a student
            self.student_search_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 11), x=350, y=25,
                                                              width=25, borderwidth=3)

            # remaking a table to display student details
            self.report_table.destroy()
            self.report_table = self.make_table(self.__frame, 200, 100, self.student_table_columns_width,
                                                self.student_table_columns, height=13)
            self.striped_rows(self.report_table)

        # if the user wants to see schedule details
        elif self.select_search_dropdown.get() == 'Schedule':
            self.__destroy_search_fields()

            # making a dropdwon so that users can search for a schedule
            self.schedule_search_dropdown = self.make_dropdown(self.__frame, values=['None'] + self.days_array,
                                                               font=(style.main_font, 11), initial='',
                                                               x=350, y=25, width=20)

            # remaking a table to display schedule details
            self.report_table.destroy()
            self.report_table = self.make_table(self.__frame, 200, 100, self.schedule_table_columns_width,
                                                self.schedule_table_columns, height=13)
            self.striped_rows(self.report_table)

        # if the user wants to see course details
        elif self.select_search_dropdown.get() == 'Course':
            self.__destroy_search_fields()

            # making a dropdwon so that users can search for a course
            self.course_search_dropdown = self.make_dropdown(self.__frame, values=['None'] + self.course_names_array,
                                                             font=(style.main_font, 11), initial='',
                                                             x=350, y=25, width=20)

            # remaking a table to display course details
            self.report_table.destroy()
            self.report_table = self.make_table(self.__frame, 200, 100, self.course_table_columns_width,
                                                self.course_table_columns, height=13)
            self.striped_rows(self.report_table)

    # function to generate reports in text files
    def __save_in_textfile(self):
        # the header string that will always be written to the file no matter how many lines are present in the table
        self.course_string = 'ID,Course Name,Course Level,Age Group,Sessions,Course Fee,Registered'
        self.schedule_string = 'ID,Day,Start Time,End Time,Registered'
        self.student_string = 'ID,Student Name,Date of Birth,Parent Name,Parent Email,Phone Number,Registered'

        # the string to which all the details will be concatenated
        self.final_string = ''

        # looping through the values of the table, and converting them into 1 string
        for table_row_number in self.report_table.get_children():
            self.current_row_contents = self.report_table.item(table_row_number, 'values')

            # joining each different field in the array 'current_row_contents' into a string for one row
            self.row_string = ','.join(self.current_row_contents)

            # adding each record on a new line
            self.final_string += '\n' + self.row_string

        if self.select_search_dropdown_content == 'Course':
            # updating the course string with the relevant course details
            self.course_string += self.final_string

            # writing the final string onto the course text file
            text_file_writer(self.course_string, 'courses')

        if self.select_search_dropdown_content == 'Schedule':
            # updating the schedule string with the relevant schedule details
            self.schedule_string += self.final_string

            # writing the final string onto the schedule text file
            text_file_writer(self.schedule_string, 'schedules')
        else:
            # updating the student string with the relevant student details
            self.student_string += self.final_string

            # writing the final string onto the student text file
            text_file_writer(self.student_string, 'students')

        # notifying user that the details have been saved successfully onto the text file
        self.make_notification_window(self.success_window_title, self.success_window_text)

    # function to delete search criteria widgets
    def __destroy_search_fields(self):
        self.schedule_search_dropdown.destroy()
        self.course_search_dropdown.destroy()
        self.student_search_entrybox.destroy()

    # function to insert appropriate data into table
    def __insert_data(self):
        self.table_row_counter = 0

        # calling the read function from file handler
        self.all_entities_array = binary_file_reader()

        # array that stores registered objects
        self.registered_objects_array = self.all_entities_array[5]

        # fetching the search criteria provided by the user
        self.select_search_dropdown_content = self.select_search_dropdown.get()
        if self.select_search_dropdown_content == 'Course':
            # deleting all the records present in the table
            for record in self.report_table.get_children():
                self.report_table.delete(record)

            # array that stores course objects
            self.course_objects_array = self.all_entities_array[2]

            # fetching search criteria that will filter specific courses based on course names
            self.course_search_dropdown_content = self.course_search_dropdown.get()
            if self.course_search_dropdown_content == 'None':
                self.course_search_dropdown_content = ''

            # looping through the course array to determine which courses match the criteria
            for course in self.course_objects_array:
                self.registered = 0

                # determining which courses match
                if self.course_search_dropdown_content in course.name:
                    for registration in self.registered_objects_array:
                        # determining how many times the chosen course has been determined
                        if course.course_id == registration.course_id:
                            self.registered += 1

                    # finalising the details that would be shown on the table
                    self.row_of_terms = (course.course_id, course.name, course.level, course.age, course.duration,
                                         course.fee, self.registered)

                    # determining the colour of the row
                    if self.table_row_counter % 2 == 0:
                        self.report_table.insert(parent='', index='end', iid=self.table_row_counter, text='',
                                                 values=self.row_of_terms, tags=('even',))
                    else:
                        self.report_table.insert(parent='', index='end', iid=self.table_row_counter, text='',
                                                 values=self.row_of_terms, tags=('odd',))
                    self.table_row_counter += 1

        elif self.select_search_dropdown_content == 'Schedule':
            # deleting all the records present in the table
            for record in self.report_table.get_children():
                self.report_table.delete(record)

            # array that stores schedule objects
            self.schedule_objects_array = self.all_entities_array[3]

            # fetching search criteria that will filter specific schedules based on day of the week
            self.schedule_search_dropdown_content = self.schedule_search_dropdown.get()
            if self.schedule_search_dropdown_content == 'None':
                self.schedule_search_dropdown_content = ''

            # looping through the schedule array to determine which schedules match the criteria
            for schedule in self.schedule_objects_array:
                self.registered = 0

                # determining which schedules match
                if self.schedule_search_dropdown_content in schedule.day:
                    for registrations in self.registered_objects_array:
                        # determining how many times the chosen schedule has been determined
                        if schedule.schedule_id == registrations.schedule_id:
                            self.registered += 1

                    # finalising the details that would be shown on the table
                    self.row_of_terms = (schedule.schedule_id, schedule.day, schedule.start_time,
                                         schedule.end_time, self.registered)

                    # determining the colour of the row
                    if self.table_row_counter % 2 == 0:
                        self.report_table.insert(parent='', index='end', iid=self.table_row_counter, text='',
                                                 values=self.row_of_terms, tags=('even',))
                    else:
                        self.report_table.insert(parent='', index='end', iid=self.table_row_counter, text='',
                                                 values=self.row_of_terms, tags=('odd',))
                    self.table_row_counter += 1

        elif self.select_search_dropdown_content == 'Student':
            # deleting all the records present in the table
            for record in self.report_table.get_children():
                self.report_table.delete(record)

            # array that stores student objects
            self.student_objects_array = self.all_entities_array[4]

            # fetching search criteria that will filter specific students based on student names
            self.student_search_entrybox_content = self.student_search_entrybox.get()

            # looping through the students array to determine which students match the criteria
            for student in self.student_objects_array:
                self.registered = 0

                # determining which students match
                if self.student_search_entrybox_content.lower() in student.student_name.lower():
                    for registrations in self.registered_objects_array:
                        # determining how many times the chosen student has been determined
                        if student.student_id == registrations.student_id:
                            self.registered += 1

                    # finalising the details that would be shown on the table
                    self.row_of_terms = (student.student_id, student.student_name, student.date_of_birth,
                                         student.parent_name, student.email, student.phone, self.registered)

                    # determining the colour of the row
                    if self.table_row_counter % 2 == 0:
                        self.report_table.insert(parent='', index='end', iid=self.table_row_counter, text='',
                                                 values=self.row_of_terms, tags=('even',))
                    else:
                        self.report_table.insert(parent='', index='end', iid=self.table_row_counter, text='',
                                                 values=self.row_of_terms, tags=('odd',))
                    self.table_row_counter += 1
