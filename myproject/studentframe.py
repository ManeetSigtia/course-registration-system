from tkinter import Label, Frame, END

import style
from widgets import Widgets
from verify import Validation
from file_handler import binary_file_reader, binary_file_writer


class NewStudent:
    # class to make student objects that will later be used to map students to courses
    def __init__(self, student_name, date_of_birth, parent_name, email, phone):
        # calling the read function from file handler
        self.all_entities_array = binary_file_reader()

        self.student_name = student_name
        self.date_of_birth = date_of_birth
        self.parent_name = parent_name
        self.email = email
        self.phone = phone
        self.student_id = self.__generate_id()

    # private function to generate a unique student id
    def __generate_id(self):
        # array containing the months of the year
        months_array = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        # generating ID using the first 3 fields. Each field makes up a part and constitutes 2 digits
        # ASCII value of the first letter of the student name entered
        part_a = ord(self.student_name[0].upper())
        # date (ranging from 1 to 31)
        part_b = self.date_of_birth[0:2]

        # chronoligical order number when the student was created
        # if it is the fifth student created, this would depict '05'
        part_c = len(self.all_entities_array[4])+1

        return str(part_a) + str(part_b).zfill(2) + str(part_c).zfill(2)

        # the zfill function adds the required amount of 0s before the string for the required len of string
        # if 2 is passed, the final length of the generated string would be 2

    # public function to save schedule objects in file
    def save(self, element):
        # adding the new course to the correct array in the 2D Array
        self.all_entities_array[4].append(element)

        # writing the updated array back onto the file
        binary_file_writer(self.all_entities_array)


class StudentFrame(Widgets, Validation):
    # inheriting from the Widgets and the Check class
    def __init__(self, root):
        super().__init__()
        # creating a frame in which all widgets will be added
        self.__frame = Frame(root, width=style.frame_width, height=style.frame_height)

        # array containing the dates of days
        self.days_array = [str(x).zfill(2) for x in range(1, 32)]

        # array containing the months of a year
        self.months_array = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        # array containing years ranging from 2000 to 2022
        self.years_array = [x for x in range(2000, 2023)]

        # initialising string that will be used in the making of the pop-up window
        self.unfilled_window_title = 'Empty Fields'
        self.unfilled_window_text = 'Please fill all required fields.'

        self.incorrect_window_title = 'Incorrect Data'
        self.incorrect_window_text = 'Please enter correct data.'

        self.clear_window_title = 'Clear Details?'
        self.clear_window_label = 'Are you sure you want to clear details?'

        self.submit_window_title = 'Submit Details?'
        self.submit_window_label = 'Are you sure you want to save details?'

        self.success_window_title = 'Successful submission'
        self.success_window_text = 'The student details have been successfully saved.'

        # calling this function to place all created widgets on screen
        self.__frame_elements()

    # public function used to retrieve the private attribute 'frame'
    def get_frame(self):
        return self.__frame

    # private function contaning everything to do with making the screen
    def __frame_elements(self):
        # creating labels for the student frame
        Label(self.__frame, text='Student Name*', font=(style.main_font, 25), fg=style.orange).place(x=300)
        Label(self.__frame, text='Date of Birth*', font=(style.main_font, 25), fg=style.orange).place(x=300, y=90)
        Label(self.__frame, text='Parent Name*', font=(style.main_font, 25), fg=style.orange).place(x=300, y=180)
        Label(self.__frame, text='Email', font=(style.main_font, 25), fg=style.orange).place(x=300, y=270)
        Label(self.__frame, text='Phone Number', font=(style.main_font, 25), fg=style.orange).place(x=300, y=360)

        # creating entryboxes so that user can input data
        self.student_name_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 20), x=650, y=0, width=30)
        self.parent_name_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 20), x=650, y=180, width=30)
        self.email_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 20), x=650, y=270, width=30)
        self.phone_number_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 20), x=650, y=360, width=30)

        # creating dropdowns so that the user has limited input for certain fields
        self.day_dropdown = self.make_dropdown(self.__frame, values=self.days_array, font=(style.main_font, 20), initial='DD',
                                               x=650, y=90, width=7)
        self.month_dropdown = self.make_dropdown(self.__frame, values=self.months_array, font=(style.main_font, 20), initial='MM',
                                                 x=790, y=90, width=7)
        self.year_dropdown = self.make_dropdown(self.__frame, values=self.years_array, font=(style.main_font, 20), initial='YYYY',
                                                x=926, y=90, width=10)

        # making a button to clear all fields without saving so user can reset and reenter data
        self.clear_button = self.make_button(self.__frame, text="Clear", font=(style.main_font, 20), width=7,
                                             command=lambda: self.make_confirm_window(self.clear_window_title,
                                                                                      self.clear_window_label,
                                                                                      self.__clear),
                                             state='normal', x=580, y=450)

        # making a submit button to save details after certain validation checks
        self.submit_button = self.make_button(self.__frame, text="Submit", font=(style.main_font, 20), width=7,
                                              command=lambda: self.make_confirm_window(self.submit_window_title,
                                                                                       self.submit_window_label,
                                                                                       self.__create_object),
                                              state='normal', x=695, y=450)

    # private function to clear user entries on GUI
    def __clear(self):
        # resetting input fields so that more data can be added
        self.student_name_entrybox.delete(0, END)
        self.day_dropdown.set('DD')
        self.month_dropdown.set('MM')
        self.year_dropdown.set('YYYY')
        self.parent_name_entrybox.delete(0, END)
        self.email_entrybox.delete(0, END)
        self.phone_number_entrybox.delete(0, END)

    # private function to create student object and save it in file
    def __create_object(self):
        # fetching details that have been entered
        self.student_name_entrybox_content = self.student_name_entrybox.get()
        self.day_dropdown_content = self.day_dropdown.get()
        self.month_dropdown_content = self.month_dropdown.get()
        self.year_dropdown_content = self.year_dropdown.get()
        self.parent_name_entrybox_content = self.parent_name_entrybox.get()
        self.email_entrybox_content = self.email_entrybox.get()
        self.phone_number_entrybox_content = self.phone_number_entrybox.get()

        # checking for unfilled mandatory details - if they exist, then display an error window
        if not self.student_name_entrybox_content \
                or self.day_dropdown_content == 'DD' \
                or self.month_dropdown_content == 'MM' \
                or self.year_dropdown_content == 'YYYY' \
                or not self.parent_name_entrybox_content:

            # making an error window if all required fields aren't filled
            self.unfilled_fields_master = self.make_notification_window(self.unfilled_window_title, self.unfilled_window_text)

        # if all mandatory details filled:
        else:
            # the following indices will allow the datetime module to validate date
            self.day_index = int(self.day_dropdown_content)
            self.month_index = 1 + self.months_array.index(self.month_dropdown_content)
            self.year_index = int(self.year_dropdown_content)

            # checking the validity of the date of birth, email and phone number fields
            # validating date of birth
            self.validate_date(self.year_index, self.month_index, self.day_index)

            # if a phone number has been entered, validate it
            if self.phone_number_entrybox_content:
                self.validate_phone(self.phone_number_entrybox_content)
            else:
                self.boolean_numbers_verifier = True

            # if an email has been entered, validate it
            if self.email_entrybox_content:
                self.validate_email(self.email_entrybox_content)
            else:
                self.boolean_emails_verifier = True

            # checking whether all validations have been passed
            if not self.boolean_emails_verifier or not self.boolean_numbers_verifier or not self.boolean_date_verifier:
                # making an error window if invalid data has been entered
                self.incorrect_data_master = self.make_notification_window(self.incorrect_window_title,
                                                                           self.incorrect_window_text)
            else:
                # all validation checks passed
                # calling the read function from file handler to read binary file
                self.all_entities_array = binary_file_reader()

                # concatenating the date of birth in DD/MMM/YYYY format
                self.date_of_birth = self.day_dropdown_content + "/" + \
                                     self.month_dropdown_content + "/" + \
                                     self.year_dropdown_content

                # creating new student object
                self.created_student_object = NewStudent(self.student_name_entrybox_content,
                                                         self.date_of_birth,
                                                         self.parent_name_entrybox_content,
                                                         self.email_entrybox_content,
                                                         self.phone_number_entrybox_content)

                # saving the new student object
                self.created_student_object.save(self.created_student_object)

                # after details have been saved, the fields can be cleared for further entry
                self.__clear()

                # displaying that the student object has been saved
                self.make_notification_window(self.success_window_title, self.success_window_text, x=50)
