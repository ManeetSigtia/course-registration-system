from tkinter import *
from widgets import Widgets
import style
import file_handler
from verify import Validation


class NewCourse:
    # class to make course objects that will later be used to register students
    def __init__(self, name, level, age_group, sessions, fee):
        # calling the read function from file handler
        self.all_entities_array = file_handler.binary_file_reader()

        self.name = name
        self.level = level
        self.age = age_group
        self.duration = sessions
        self.fee = fee
        self.course_id = self.__generate_id()

    # private function to generate a unique course id
    def __generate_id(self):
        # reading the course names and age groups list
        course_names_array = self.all_entities_array[0]
        age_groups_array = self.all_entities_array[1]

        # generate ID using the first 3 fields. Each field makes up a part and constitutes 2 digits
        # index position of the course name in the array
        part_a = course_names_array.index(self.name)
        # ASCII value of the first letter of the level chosen
        part_b = ord(self.level[0])
        # index position of the age group in the array
        part_c = age_groups_array.index(self.age)

        return str(part_a).zfill(2) + str(part_b).zfill(2) + str(part_c).zfill(2)

        # the zfill function adds the required amount of 0s before the string for the required len of string
        # if 2 is passed, the final length of the generated string would be 2

    # public function to save course objects in file
    def save(self, element):
        # adding the new course to the correct array in the 2D Array
        self.all_entities_array[2].append(element)

        # writing the updated array back onto the file
        file_handler.binary_file_writer(self.all_entities_array)


class CourseFrame(Widgets, Validation):
    # inheriting methods and attributes from the Widgets and the Check class
    def __init__(self, root):
        super().__init__()
        # creating a frame in which all widgets will be added
        self.__frame = Frame(root, width=style.frame_width, height=style.frame_height)

        # calling the read function from file handler
        self.all_entities_array = file_handler.binary_file_reader()

        # reading the course names, course levels and age groups list
        # these arrays will be used to set dropdowns for this frame
        self.course_names_array = self.all_entities_array[0]
        self.course_levels_array = ["Beginner", "Intermediate", "Advanced"]
        self.age_groups_array = self.all_entities_array[1]

        # initialising string that will be used in the making of the pop-up window
        self.clear_title = 'Clear Details?'
        self.clear_label = 'Are you sure you want to clear details?'

        self.submit_title = 'Submit Details?'
        self.submit_label = 'Are you sure you want to save details?'

        self.unfilled_window_title = 'Empty Fields'
        self.unfilled_window_text = 'Please fill all required fields'

        self.incorrect_window_title = 'Incorrect Data'
        self.incorrect_window_text = 'Please enter correct data'

        self.success_window_title = 'Successful submission'
        self.success_window_text = 'The course details have been successfully saved.'

        # calling this function to place all created widgets on screen
        self.__frame_elements()

    # public function used to retrieve the private attribute 'frame'
    def get_frame(self):
        return self.__frame

    # private function contaning everything to do with making the screen
    def __frame_elements(self):
        # creating labels for the course frame
        Label(self.__frame, text='Course Name*', font=(style.main_font, 25), fg=style.orange).place(x=380)
        Label(self.__frame, text='Course Level*', font=(style.main_font, 25), fg=style.orange).place(x=380, y=90)
        Label(self.__frame, text='Age Groups*', font=(style.main_font, 25), fg=style.orange).place(x=380, y=180)
        Label(self.__frame, text='Number of Sessions*', font=(style.main_font, 25), fg=style.orange).place(x=380, y=270)
        Label(self.__frame, text='Course Fee (SGD)*', font=(style.main_font, 25), fg=style.orange).place(x=380, y=360)

        # creating dropdowns so that the user has limited input for certain fields
        self.course_name_dropdown = self.make_dropdown(self.__frame, values=self.course_names_array,
                                                       font=(style.main_font, 17), initial='', x=798, y=0, width=24)
        self.course_level_dropdown = self.make_dropdown(self.__frame, values=self.course_levels_array,
                                                        font=(style.main_font, 20), initial='', x=800, y=90, width=20)
        self.age_group_dropdown = self.make_dropdown(self.__frame, values=self.age_groups_array,
                                                     font=(style.main_font, 20), initial='', x=800, y=180, width=20)

        # creating entryboxes so that number of sessions and course fee can be entered
        self.course_sessions_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 20), x=800, y=270,
                                                           width=21)
        self.fee_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 20,), x=800, y=360, width=21)

        # making a button to clear all fields without saving so user can reset and reenter data
        self.clear_button = self.make_button(self.__frame, text="Clear", font=(style.main_font, 20), width=7,
                                             command=lambda: self.make_confirm_window(self.clear_title,
                                                                                      self.clear_label,
                                                                                      self.__clear),
                                             state='normal', x=630, y=450)

        # making a submit button to save details after certain validation checks
        self.submit_button = self.make_button(self.__frame, text="Submit", font=(style.main_font, 20), width=7,
                                              command=lambda: self.make_confirm_window(self.submit_title,
                                                                                       self.submit_label,
                                                                                       self.__create_object),
                                              state='normal', x=750, y=450)

    # private function to clear user entries on GUI
    def __clear(self):
        # resetting input fields so that more data can be added
        self.course_name_dropdown.set('')
        self.course_level_dropdown.set('')
        self.age_group_dropdown.set('')
        self.course_sessions_entrybox.delete(0, END)
        self.fee_entrybox.delete(0, END)

    # private function to create course object and save it in file
    def __create_object(self):
        # fetching details that have been entered
        self.course_name_dropdown_content = self.course_name_dropdown.get()
        self.course_level_dropdown_content = self.course_level_dropdown.get()
        self.age_group_dropdown_content = self.age_group_dropdown.get()
        self.course_sessions_entrybox_content = self.course_sessions_entrybox.get()
        self.fee_entrybox_content = self.fee_entrybox.get()

        # checking for unfilled details - if they exist, then display an error window
        if not self.course_name_dropdown_content \
                or not self.course_level_dropdown_content \
                or not self.age_group_dropdown_content \
                or not self.course_sessions_entrybox_content \
                or not self.fee_entrybox_content:

            # making an error window if all required fields aren't filled
            self.unfilled_fields_master = self.make_notification_window(self.unfilled_window_title,
                                                                        self.unfilled_window_text)

        # if all details filled:
        else:
            # checking for validity of sessions and fees input
            self.validate_sessions(self.course_sessions_entrybox_content)
            self.validate_fees(self.fee_entrybox_content)

            # checking whether validations have been passed
            if not self.boolean_fees_verifier or not self.boolean_sessions_verifier:
                # making an error window if invalid data has been entered
                self.incorrect_data_master = self.make_notification_window(self.incorrect_window_title,
                                                                           self.incorrect_window_text)
            else:
                # all validation checks passed
                # calling the read function from file handler to read binary file
                self.all_entities_array = file_handler.binary_file_reader()

                # creating new course object
                self.created_course_object = NewCourse(self.course_name_dropdown_content,
                                                       self.course_level_dropdown_content,
                                                       self.age_group_dropdown_content,
                                                       self.course_sessions_entrybox_content,
                                                       self.fee_entrybox_content)

                # saving the new course object
                self.created_course_object.save(self.created_course_object)

                # after details have been saved, the fields can be cleared for further entry
                self.__clear()

                # displaying that the course object has been saved
                self.make_notification_window(self.success_window_title, self.success_window_text, x=50)
