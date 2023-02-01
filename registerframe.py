from tkinter import *
from widgets import Widgets
import style
import file_handler
from verify import Validation
import datetime
from datetime import datetime, timedelta
from termframe import NewTerm


class NewRegister:
    # class to register students using data from courses, schedules and students class
    def __init__(self, course_id, schedule_id, student_id, start_date, future_dates, registration_id):
        self.course_id = course_id
        self.student_id = student_id
        self.schedule_id = schedule_id
        self.start_date = start_date
        self.future_dates = future_dates
        self.registration_id = registration_id


class RegisterFrame(Widgets, Validation):
    # inheriting from the Widgets and the Check class
    def __init__(self, root):
        super().__init__()
        # creating a frame in which all widgets will be added
        self.__frame = Frame(root, width=style.frame_width, height=style.frame_height)

        # images that will be used for the search and refresh buttons
        self.refresh_image = PhotoImage(file=r"refresh_1.png")
        self.search_image = PhotoImage(file=r"search_1.png")

        # lists used to make dropdown menus when data is being input:
        # list containing date of datys from 0 to 30
        self.days_array = [str(x).zfill(2) for x in range(1, 32)]

        # list containing name of months
        self.months_array = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        # list containing years from 2000 to 2050
        self.years_array = [x for x in range(2000, 2050)]

        # list containing possible discount types offered to customer
        self.discount_types_array = ["None", "Early Bird", "Packaged", "Referral", "Sibling"]

        # list containing possible payment methods
        self.payment_methods_array = ["Bank Transfer", "PayLah", "PayNow"]

        # list containing possible payment status options
        self.statuses_array = ["NT Pending", "Paid", "In-Progress", "Closed"]

        # initialising strings that will later be used in the making of pop-up windows
        self.incorrect_window_title = 'Incorrect Data'
        self.incorrect_window_label = 'Please enter correct data'

        self.unfilled_window_title = 'Empty Fields'
        self.unfilled_window_text = 'Please fill all required fields'

        self.clear_window_title = 'Clear Details?'
        self.clear_window_label = 'Are you sure you want to clear details?'

        self.submit_window_title = 'Save Details?'
        self.submit_window_label = 'Are you sure you want to submit details?'

        self.success_register_window_title = 'Successful submission'
        self.success_register_window_text = 'The registration has been successfully saved.'

        self.success_term_window_title = 'Successful submission'
        self.success_term_window_text = 'The term details have been successfully saved.'

        # calling this function to place all created widgets on screen
        self.frame_elements()

    # public function used to retrieve the private attribute 'frame'
    def get_frame(self):
        return self.__frame

    # function contaning everything to do with making the screen
    def frame_elements(self):
        # there are 2 parts to the screen, the left hand side deals with the registration of students
        # the right hand side deals with the term information that the user has an option to enter

        # the following widgets will be used to register a student (left side of frame)
        # creating labels for the frame
        Label(self.__frame, text='Register', font=(style.main_font, 35), fg='black').place(x=0, y=0)
        Label(self.__frame, text='Courses*', font=(style.main_font, 20), fg=style.orange).place(x=0, y=70)
        Label(self.__frame, text='Students*', font=(style.main_font, 20), fg=style.orange).place(y=140)
        Label(self.__frame, text='Schedules*', font=(style.main_font, 20), fg=style.orange).place(y=350)
        Label(self.__frame, text='Start Date*', font=(style.main_font, 20), fg=style.orange).place(y=420)

        # calling this function to initialise the course dropdown
        self.__refresh_courses()

        # calling this function to initialise the schedule dropdown
        self.__refresh_schedules()

        # creating dropdowns so that the user has limited input for certain fields
        self.start_day_dropdown = self.make_dropdown(self.__frame, values=self.days_array, font=(style.main_font, 17),
                                                     initial='DD', x=130, y=420, width=4)
        self.start_month_dropdown = self.make_dropdown(self.__frame, values=self.months_array, font=(style.main_font, 17),
                                                       initial='MM', x=280, y=420, width=4)
        self.start_year_dropdown = self.make_dropdown(self.__frame, values=self.years_array, font=(style.main_font, 17),
                                                      initial='YYYY', x=420, y=420, width=7)

        # creating entryboxes so that user can input data
        self.student_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 15), x=130, y=140, width=39)

        # creating a listbox to dsiplay student names from which users choose a particular student
        self.student_listbox = self.make_listbox(self.__frame, font=(style.main_font, 15), height=4, width=39,
                                                 borderwidth=5, x=130, y=210)
        self.student_listbox.bind('<<ListboxSelect>>', self.__student_criteria_filler)

        # making buttons to refresh course and schedule fields to display newly entered data
        self.refresh_course_button = Button(self.__frame, image=self.refresh_image, width=30, height=30,
                                            command=self.__refresh_courses, state='normal')
        self.refresh_schedule_button = Button(self.__frame, image=self.refresh_image, width=30, height=30,
                                              command=self.__refresh_schedules, state='normal')

        # making a button to allow user to search for a particular student based on name
        self.search_student_button = Button(self.__frame, image=self.search_image, width=30, height=30,
                                            command=self.__search_students, state='normal')

        # placing the buttons created above on screen
        self.refresh_course_button.place(x=540, y=70)
        self.search_student_button.place(x=540, y=140)
        self.refresh_schedule_button.place(x=540, y=350)

        # making a button to clear all fields on the registration side of the screen
        # without saving so user can reset and reenter data
        self.clear_register_button = self.make_button(self.__frame, text="Clear", font=(style.main_font, 16), width=7,
                                                      command=lambda: self.make_confirm_window(
                                                          self.clear_window_title,
                                                          self.clear_window_label,
                                                          self.__clear_registered),
                                                      state='normal', x=160, y=490)

        # making a submit button to save details after certain validation checks
        self.submit_register_button = self.make_button(self.__frame, text="Submit", font=(style.main_font, 16), width=7,
                                                       command=lambda: self.make_confirm_window(
                                                           self.submit_window_title,
                                                           self.submit_window_label,
                                                           self.__save_registered),
                                                       state='normal', x=260, y=490)

        # there are 2 parts to the screen, the left hand side deals with the registration of students
        # the right hand side deals with the term information that the user has an option to enter

        # the following widgets will be used to deal with the terms for that registration (right side of frame)
        Label(self.__frame, text='Term Details', font=(style.main_font, 35), fg='black').place(x=650, y=0)

        # creating entryboxes so that user can input data
        # the following entryboxes will be immutable, and will fill automatically once a new registration has been made
        # the user can not change the values of these fields other than the end date entrybox
        self.ID_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 12), x=650, y=180, width=16,
                                              borderwidth=2)
        self.course_term_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 12), x=770, y=180, width=16,
                                                       borderwidth=2)
        self.student_term_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 12), x=890, y=180, width=16,
                                                        borderwidth=2)
        self.session_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 12), x=1010, y=180, width=16,
                                                   borderwidth=2)
        self.term_fee_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 12), x=1130, y=180, width=16,
                                                    borderwidth=2)
        self.start_date_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 12), x=1250, y=180, width=16,
                                                      borderwidth=2)
        self.end_date_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 12), x=1370, y=180, width=16,
                                                    borderwidth=2)
        # disabling the following enty box to avoid user from details after they have made a new registration
        self.__term_entrybox_status('disabled')

        # the pivot position based on which the label y values will change
        self.title_y_position = 150

        # creating labels for the higher side of the term section of the registration frame
        Label(self.__frame, text='Term ID', font=(style.main_font, 12), fg=style.orange).place(x=650, y=self.title_y_position)
        Label(self.__frame, text='Course Name', font=(style.main_font, 12), fg=style.orange).place(x=770, y=self.title_y_position)
        Label(self.__frame, text='Student Name', font=(style.main_font, 12), fg=style.orange).place(x=890, y=self.title_y_position)
        Label(self.__frame, text='Sessions', font=(style.main_font, 12), fg=style.orange).place(x=1010, y=self.title_y_position)
        Label(self.__frame, text='Course Fee', font=(style.main_font, 12), fg=style.orange).place(x=1130, y=self.title_y_position)
        Label(self.__frame, text='Start Date', font=(style.main_font, 12), fg=style.orange).place(x=1250, y=self.title_y_position - 20)
        Label(self.__frame, text='DD/MM/YYYY', font=(style.main_font, 12), fg=style.orange).place(x=1250, y=self.title_y_position)
        Label(self.__frame, text='End Date*', font=(style.main_font, 12), fg=style.orange).place(x=1370, y=self.title_y_position - 20)
        Label(self.__frame, text='DD/MM/YYYY', font=(style.main_font, 12), fg=style.orange).place(x=1370, y=self.title_y_position)

        # creating labels for the lower side of the term section of the registration frame
        Label(self.__frame, text='Discount Type', font=(style.main_font, 12), fg=style.orange).place(x=650, y=self.title_y_position + 170)
        Label(self.__frame, text='Discount Amount', font=(style.main_font, 12), fg=style.orange).place(x=780, y=self.title_y_position + 170)
        Label(self.__frame, text='Payment Method', font=(style.main_font, 12), fg=style.orange).place(x=900, y=self.title_y_position + 170)
        Label(self.__frame, text='Amount Paid', font=(style.main_font, 12), fg=style.orange).place(x=1030, y=self.title_y_position + 170)
        Label(self.__frame, text='Payment Date', font=(style.main_font, 12), fg=style.orange).place(x=1135, y=self.title_y_position + 150)
        Label(self.__frame, text='DD/MM/YYYY', font=(style.main_font, 12), fg=style.orange).place(x=1135, y=self.title_y_position + 170)
        Label(self.__frame, text='Account Name', font=(style.main_font, 12), fg=style.orange).place(x=1260, y=self.title_y_position + 170)
        Label(self.__frame, text='Status', font=(style.main_font, 12), fg=style.orange).place(x=1375, y=self.title_y_position + 170)

        # creating dropdowns so that the user has limited input for certain fields
        self.discount_type_dropdown = self.make_dropdown(self.__frame, values=self.discount_types_array,
                                                         initial=self.discount_types_array[0],
                                                         font=(style.main_font, 12), x=650, y=350, width=13)
        self.payment_method_dropdown = self.make_dropdown(self.__frame, values=self.payment_methods_array,
                                                          initial=self.payment_methods_array[0],
                                                          font=(style.main_font, 12), x=905, y=350, width=13)
        self.status_dropdown = self.make_dropdown(self.__frame, values=self.statuses_array, initial=self.statuses_array[0],
                                                  font=(style.main_font, 12), x=1370, y=350, width=13)

        # creating entryboxes so that user can input data
        self.discount_amount_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 12), x=775, y=350,
                                                           width=15, borderwidth=2)
        self.amount_paid_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 12), x=1030, y=350, width=13,
                                                       borderwidth=2)
        self.payment_date_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 12), x=1133, y=350, width=16,
                                                        borderwidth=2)
        self.account_name_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 12), x=1260, y=350, width=13,
                                                        borderwidth=2)

        # making a button to clear all fields on term side of the screen
        # without saving so user can reset and reenter data
        self.clear_term_button = self.make_button(self.__frame, text="Clear", font=(style.main_font, 16), width=7,
                                                  command=lambda: self.make_confirm_window(
                                                      self.clear_window_title,
                                                      self.clear_window_label,
                                                      self.__clear_terms),
                                                  state='disabled', x=950, y=490)

        # making a submit button to save details after certain validation checks
        self.submit_term_button = self.make_button(self.__frame, text="Submit", font=(style.main_font, 16), width=7,
                                                   command=lambda: self.make_confirm_window(
                                                       self.submit_window_title,
                                                       self.submit_window_label,
                                                       self.__term_editor),
                                                   state='disabled', x=1050, y=490)

        # changing the colour of these buttons to dark blue, indicating that they are disabled
        self.clear_term_button.config(bg=style.dark_blue)
        self.submit_term_button.config(bg=style.dark_blue)

        # black line that divides the registration area from the term area for aesthetic purposes
        self.divider = Frame(self.__frame, bg='black', width=5, height=550)
        self.divider.place(x=600, y=0)

    # function to display selected student in the entry box in the registration section
    def __student_criteria_filler(self, event):
        self.student_entrybox.delete(0, END)
        self.student_entrybox.insert(0, self.student_listbox.get(ANCHOR))

    # function to update available and new courses displayed in the dropdown
    def __refresh_courses(self):
        # reading the file to get the updated version of the course objects
        self.all_entities_array = file_handler.binary_file_reader()

        # list that will be used to display options in the course dropdown
        self.course_array = []
        # looping through the course objects array
        for course_details in self.all_entities_array[2]:
            # adding details of different courses so it is easier to distinguish them
            self.course_array.append((course_details.name, course_details.level, course_details.age))

        if not len(self.course_array) == 0:
            # if there are courses that have been created, then display them
            self.course_dropdown = self.make_dropdown(self.__frame, values=self.course_array, font=(style.main_font, 15),
                                                      initial='', x=130, y=70, width=38)
        else:
            # otherwise, display an empty dropdown. No registration can take place in this case
            self.course_dropdown = self.make_dropdown(self.__frame, values=[''], font=(style.main_font, 15),
                                                      initial='', x=130, y=70, width=38)

    # function to determine students based on the searched name
    def __search_students(self):
        # if students exist, this boolean is true, else false
        self.boolean_students_found = False

        # reading the file to get the updated version of the student objects
        self.all_entities_array = file_handler.binary_file_reader()

        # getting the search criteria and removing whitespaces before and after string
        self.student_search_criteria = self.student_entrybox.get().strip()
        # clearing previous names and making space for new names in the area where the user chooses the required student
        self.student_listbox.delete(0, END)
        #  looping through the students objects array
        self.student_object_array = self.all_entities_array[4]
        for student in self.student_object_array:
            # if the name input by user matches name present in file
            if self.student_search_criteria.lower() in student.student_name.lower():
                # displaying the name
                self.student_listbox.insert(END, student.student_name)
                # setting a boolean that, if is true, shows that there is as least one name present
                self.boolean_students_found = True

    # function to update available and new schedules displayed in the dropdown
    def __refresh_schedules(self):
        # reading the file to get the updated version of the schedule objects
        self.all_entities_array = file_handler.binary_file_reader()

        # list that will be used to display options in the schedule dropdown
        self.schedule_objects_array = []
        #  looping through the schedule objects array
        for schedule_details in self.all_entities_array[3]:
            # adding details of different schedules so it is easier to distinguish them
            self.schedule_objects_array.append((schedule_details.day, schedule_details.start_time, schedule_details.end_time))

        if not len(self.schedule_objects_array) == 0:
            # if there are schedules that have been created, then display them
            self.schedule_dropdown = self.make_dropdown(self.__frame, values=self.schedule_objects_array,
                                                        font=(style.main_font, 17),
                                                        initial='', x=130, y=350, width=32)
        else:
            # otherwise, display an empty dropdown
            self.schedule_dropdown = self.make_dropdown(self.__frame, values=[''], font=(style.main_font, 17), initial='',
                                                        x=130, y=350, width=32)

    # function to create registration objcct and save it
    def __save_registered(self):
        # fetching details that have been entered by the user
        self.course_dropdown_content = self.course_dropdown.get()
        self.student_entrybox_content = self.student_entrybox.get()
        self.schedule_dropdown_content = self.schedule_dropdown.get()
        self.start_day_dropdown_content = self.start_day_dropdown.get()
        self.start_month_dropdown_content = self.start_month_dropdown.get()
        self.start_year_dropdown_content = self.start_year_dropdown.get()

        # checking for unfilled details - if they exist, then display an error window
        if not self.course_dropdown_content \
                or not self.student_entrybox_content \
                or not self.schedule_dropdown_content \
                or self.start_day_dropdown_content == 'DD' \
                or self.start_month_dropdown_content == 'MM' \
                or self.start_year_dropdown_content == 'YYYY':

            # error window if all fields aren't filled
            self.make_notification_window(self.unfilled_window_title, self.unfilled_window_text)

        # if all details filled:
        else:
            # checking for validity of start date
            # confirming that the start date entered matches the day of the week entered when making a schedule

            # the following indices will allow date time module to verify the date
            self.start_day_index = int(self.start_day_dropdown_content)
            self.start_month_index = 1 + self.months_array.index(self.start_month_dropdown_content)
            self.start_year_index = int(self.start_year_dropdown_content)

            # checking the validity of the start date field
            self.validate_date(self.start_year_index, self.start_month_index, self.start_day_index)

            # checking if the date entered matches the day of the week entered in for the chosen schedule
            # from the selected schedule, the registration id and day of the week must be determined
            self.schedule_objects_array = self.all_entities_array[3]

            for schedule_object in self.schedule_objects_array:
                # finding the required object by matching the object day, start and end time and the criteria
                # creating a string that to bring it into the same format as the strings it is being checked against
                schedule_object_details = schedule_object.day + ' ' + \
                                          schedule_object.start_time + ' ' + \
                                          schedule_object.end_time
                if schedule_object_details == self.schedule_dropdown_content:
                    # needed to verify if the date matches the day of the week
                    self.day_of_week = schedule_object.day

                    # will be needed later to create a term
                    self.selected_schedule_id = schedule_object.schedule_id

            # validating day of week based on the date entered
            self.validate_date_of_week(self.day_of_week, self.start_year_index, self.start_month_index,
                                       self.start_day_index)

            # checking whether all validations have been passed
            if not self.boolean_date_verifier or not self.boolean_day_of_week_verifier:
                self.make_notification_window(self.incorrect_window_title, self.incorrect_window_label)

            else:
                # all validation checks passed
                # calling the read function from file handler
                self.all_entities_array = file_handler.binary_file_reader()

                # calling function to combine the date of birth in DD/MM/YYYY format
                self.__identify_object_details()

                # generate ID using the course, schedule and student fields
                # each field makes up a part and constitutes 2 digits
                self.new_registered_id = self.selected_course_id + self.selected_schedule_id + self.selected_student_id

                # making a registration object
                self.created_registration_object = NewRegister(self.selected_course_id, self.selected_schedule_id,
                                                               self.selected_student_id, self.class_start_date,
                                                               self.future_dates_array, self.new_registered_id)

                # after details have been saved, the fields can be cleared for further entry
                self.__clear_registered()

                # adding the new registration to the correct array in the 2D Array
                self.all_entities_array[5].append(self.created_registration_object)

                # writing the array back onto the file to save changes
                file_handler.binary_file_writer(self.all_entities_array)

                # displaying that the registration object has been saved
                self.make_notification_window(self.success_register_window_title, self.success_register_window_text, x=50)

                # calling function to edit the disabled entryboxes on the term screen
                # these show the information for the latest registratoin
                self.__fill_terms_fields()

                # calling a function to add a new term for the registration just created and saving it to the file
                self.__term_adder()

                # changing the state of the end_date entrybox to allow user to enter data
                self.end_date_entrybox.config(state='normal')

                # changing the state of the buttons to allow the user to use them
                self.submit_term_button.config(state='normal', bg=style.cyan_blue)
                self.clear_term_button.config(state='normal', bg=style.cyan_blue)

    # function to identify ids for course, schedule and students that have been used in the registration
    def __identify_object_details(self):
        # reading the file so that if updated, those changes can be accessed as well
        self.all_entities_array = file_handler.binary_file_reader()

        # creating a string that will be used later to perform date operations
        self.class_start_date = self.start_day_dropdown_content + "/" + \
                                str(1 + self.months_array.index(self.start_month_dropdown_content)).zfill(2) + "/" + \
                                self.start_year_dropdown_content

        # from the selected course, the course name, fees sessions, and id must be determined
        self.course_objects = self.all_entities_array[2]
        for course_object in self.course_objects:
            # finding the object by matching the object name, level and age and the criteria
            if course_object.name in self.course_dropdown_content \
                    and course_object.level in self.course_dropdown_content \
                    and course_object.age in self.course_dropdown_content:

                # this data will be used to fill the term details
                self.selected_course_id = course_object.course_id
                self.selected_course_name = course_object.name
                self.selected_course_fee = course_object.fee
                self.selected_no_of_days = int(course_object.duration)

        # from the selected schedule, the id must be determined
        self.schedule_objects_array = self.all_entities_array[3]
        for schedule_object in self.schedule_objects_array:
            # finding the object by matching the object day, start and end time and the criteria
            schedule_object_details = schedule_object.day + ' ' + schedule_object.start_time + ' ' + \
                                      schedule_object.end_time

            if schedule_object_details == self.schedule_dropdown_content:
                # will be needed later to create term object
                self.day_of_week = schedule_object.day
                self.selected_schedule_id = schedule_object.schedule_id

        # from the selected student, the  id must be determined
        self.student_object_array = self.all_entities_array[4]
        for student_object in self.student_object_array:

            # finding the object by matching the object name and the criteria
            if student_object.student_name == self.student_entrybox_content:
                self.selected_student_id = student_object.student_id

        # converting start date to datetime format for further calculations
        self.datetime_formatted_day = datetime.strptime(self.class_start_date, "%d/%m/%Y")

        # an array that will hold all future dates for the class
        self.future_dates_array = []
        # determining the future dates on which the course will run
        for no_of_weeks in range(self.selected_no_of_days):
            # adding 7 days to the start day for number of sessions for that course
            next_day = self.datetime_formatted_day + timedelta(days=7 * no_of_weeks)

            # adding the string version of this day on the array for future dates so that they can be seen laer
            self.future_dates_array.append(next_day.strftime('%d/%m/%Y'))

    # function to clear registration entries on GUI
    def __clear_registered(self):
        # resetting input fields so that more data can be added
        self.course_dropdown.set('')
        self.start_day_dropdown.set('DD')
        self.start_month_dropdown.set('MM')
        self.start_year_dropdown.set('YYYY')
        self.student_entrybox.delete(0, END)
        self.student_listbox.delete(0, END)
        self.schedule_dropdown.set('')

    # function to enter data in the terms section
    def __fill_terms_fields(self):
        # filling in the term fields for user convenience to allow editing ot the latest term created if user wishes
        self.__term_entrybox_status('normal')
        self.ID_entrybox.delete(0, END)
        self.course_term_entrybox.delete(0, END)
        self.student_term_entrybox.delete(0, END)
        self.session_entrybox.delete(0, END)
        self.term_fee_entrybox.delete(0, END)
        self.start_date_entrybox.delete(0, END)
        self.end_date_entrybox.delete(0, END)
        self.ID_entrybox.insert(0, "01")
        self.course_term_entrybox.insert(0, self.selected_course_name)
        self.student_term_entrybox.insert(0, self.student_entrybox_content)
        self.session_entrybox.insert(0, self.selected_no_of_days)
        self.term_fee_entrybox.insert(0, self.selected_course_fee)
        self.start_date_entrybox.insert(0, self.class_start_date)
        self.end_date_entrybox.insert(0, self.future_dates_array[-1])
        self.__term_entrybox_status('disabled')
        self.end_date_entrybox.config(state='normal')

    # function to create term object
    def __save_terms(self):
        # there will be no presence checks on the following entry boxes
        # as it is up to the user if they want to make edits now or later when they have the data regarding the terms
        # however, if either 'amount paid' or 'payment date' is entered, they will need to be validated

        # fetching details that may have been entered
        self.end_date_entrybox_content = self.end_date_entrybox.get()
        self.discount_type_dropdown_content = self.discount_type_dropdown.get()
        self.discount_amount_entrybox_content = self.discount_amount_entrybox.get()
        self.payment_method_dropdown_content = self.payment_method_dropdown.get()
        self.amount_paid_entrybox_content = self.amount_paid_entrybox.get()
        self.payment_date_entrybox_content = self.payment_date_entrybox.get()
        self.account_name_entrybox_content = self.account_name_entrybox.get()
        self.status_dropdown_content = self.status_dropdown.get()

        # a condition to check the validity of the data entered in amount_paid and payment_date
        self.amount_and_date_checker = True

        # checking whether amount paid has been entered
        if self.amount_paid_entrybox_content:
            # validating amount paid
            self.validate_fees(self.amount_paid_entrybox_content)
            if not self.boolean_fees_verifier:
                # only if the data has been entered, it must be in the correct format.
                # only numbers and decimals are allowed for this field
                # making an error window if invalid data has been entered
                self.make_notification_window(self.incorrect_window_title, self.incorrect_window_label)
                self.amount_and_date_checker = False

        # checking whether a discount amount has been entered
        if self.discount_amount_entrybox_content:
            # validating discount amount
            self.validate_fees(self.discount_amount_entrybox_content)
            if not self.boolean_fees_verifier:
                # only if the data has been entered, it must be in the correct format.
                # only numbers and decimals are allowed for this field
                # making an error window if invalid data has been entered
                self.make_notification_window(self.incorrect_window_title, self.incorrect_window_label)
                self.amount_and_date_checker = False

        # checking whether a payment date has been entered
        if self.payment_date_entrybox_content:
            try:
                self.split_payment_date = self.payment_date_entrybox_content.split('/')
                # validating payment date
                self.validate_date(int(self.split_payment_date[2]), int(self.split_payment_date[1]),
                                   int(self.split_payment_date[0]))
                if not self.boolean_date_verifier:
                    # only if the data has been entered, it must be in the correct format.
                    # the payment date must be legitimate (e.g. 31/02/2021 would be rejected)
                    # making an error window if invalid data has been entered
                    self.make_notification_window(self.incorrect_window_title, self.incorrect_window_label)
                    self.amount_and_date_checker = False
            except:
                # only if the data has been entered, it must be in the correct format.
                # the payment date must be legitimate (e.g. 31/02/2021 would be rejected)
                # making an error window if invalid data has been entered
                self.make_notification_window(self.incorrect_window_title, self.incorrect_window_label)
                self.amount_and_date_checker = False

        # checking whether an end date has been entered
        if self.end_date_entrybox_content:
            try:
                self.split_end_date = self.end_date_entrybox_content.split('/')
                self.validate_date(int(self.split_end_date[2]), int(self.split_end_date[1]),
                                   int(self.split_end_date[0]))

                if not self.boolean_date_verifier:
                    # if the data has been entered, it must be in the correct format.
                    # the end date must be legitimate (e.g. 31/02/2021 would be rejected)
                    # making an error window if invalid data has been entered
                    self.make_notification_window(self.incorrect_window_title, self.incorrect_window_label)
                    self.amount_and_date_checker = False
            except:
                # only if the data has been entered, it must be in the correct format.
                # the payment date must be legitimate (e.g. 31/02/2021 would be rejected)
                # making an error window if invalid data has been entered
                self.make_notification_window(self.incorrect_window_title, self.incorrect_window_label)
                self.amount_and_date_checker = False

        else:
            # making an error window if all required fields aren't filled
            self.make_notification_window(self.unfilled_window_title, self.unfilled_window_text)
            self.amount_and_date_checker = False

        # only if both end date and payment fees fields have valide data entered
        if self.amount_and_date_checker:
            # creating a new term object
            self.created_term_object = NewTerm('01', self.selected_course_name, self.student_entrybox_content,
                                               self.selected_no_of_days, self.selected_course_fee,
                                               self.class_start_date, self.end_date_entrybox_content,
                                               self.discount_type_dropdown_content, self.discount_amount_entrybox_content,
                                               self.payment_method_dropdown_content, self.amount_paid_entrybox_content,
                                               self.payment_date_entrybox_content, self.account_name_entrybox_content,
                                               self.status_dropdown_content, self.new_registered_id, False)

            # disabling the clear and submit buttons
            self.submit_term_button.config(state='disabled', bg=style.dark_blue)
            self.clear_term_button.config(state='disabled', bg=style.dark_blue)

            # after details have been saved, the fields can be cleared for further entry
            self.__clear_terms()

    # function to save term object in file
    def __term_adder(self):
        #
        self.__save_terms()

        self.all_entities_array = file_handler.binary_file_reader()
        if self.amount_and_date_checker:
            # adding the new term to the correct array in the 2D Array
            self.all_entities_array[6].append(self.created_term_object)
            file_handler.binary_file_writer(self.all_entities_array)

    # function to update and save last created term if user decides to edit it
    def __term_editor(self):
        # creating an edited term object
        self.__save_terms()
        # reading file contents to ensure that the data being worked on is updated
        self.all_entities_array = file_handler.binary_file_reader()
        if self.amount_and_date_checker:
            # editing the new term that was added if the submit term button is pressed
            self.all_entities_array[6][-1] = self.created_term_object
            file_handler.binary_file_writer(self.all_entities_array)

            self.make_notification_window(self.success_term_window_title, self.success_term_window_text, x=50)

    # function to clear term entries on GUI
    def __clear_terms(self):
        self.discount_type_dropdown.set('None')
        self.payment_method_dropdown.set('Bank Transfer')
        self.discount_amount_entrybox.delete(0, END)
        self.amount_paid_entrybox.delete(0, END)
        self.payment_date_entrybox.delete(0, END)
        self.account_name_entrybox.delete(0, END)
        self.status_dropdown.set('NT Pending')

    # function to change status of entryboxes and toggle between enabled and disabled states
    def __term_entrybox_status(self, state):
        self.ID_entrybox.config(state=state)
        self.course_term_entrybox.config(state=state)
        self.student_term_entrybox.config(state=state)
        self.session_entrybox.config(state=state)
        self.term_fee_entrybox.config(state=state)
        self.start_date_entrybox.config(state=state)
        self.end_date_entrybox.config(state=state)
