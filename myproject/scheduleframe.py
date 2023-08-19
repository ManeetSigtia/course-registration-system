from tkinter import Label, Frame

import style
from widgets import Widgets
from verify import Validation
from file_handler import binary_file_reader, binary_file_writer


class NewSchedule:
    # class to make schedule objects that will later be used to register students
    def __init__(self, day, start_time, end_time, description):
        # calling the read function from file handler
        self.all_entities_array = binary_file_reader()

        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.schedule_id = self.__generate_id()

    # private function to generate a unique schedule id
    def __generate_id(self):
        # array containing the days of the week
        days_array = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        # generate ID using 3 fields. Each field makes up a part and constitutes 2 digits
        # index position of the day in the array
        part_a = days_array.index(self.day)
        # first two characters, i.e., the start hour
        part_b = self.start_time[0:2]
        # chronoligical order number when the schedule was created
        # if it is the fifth schedule created, this would depict '05'
        part_c = len(self.all_entities_array[3])+1

        return str(part_a).zfill(2) + str(part_b) + str(part_c).zfill(2)

        # the zfill function adds the required amount of 0s before the string for the required len of string
        # if 2 is passed, the final length of the generated string would be 2

    # public function to save schedule objects in file
    def save(self, element):
        # adding the new course to the correct array in the 2D Array
        self.all_entities_array[3].append(element)

        # writing the updated array back onto the file
        binary_file_writer(self.all_entities_array)


class ScheduleFrame(Widgets, Validation):
    # inheriting from the Widgets and the Check class
    def __init__(self, root):
        super().__init__()
        # creating a frame in which all widgets will be added
        self.__frame = Frame(root, width=style.frame_width, height=style.frame_height)

        # array containing the days of the week
        self.days_array = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        # array containing hours for the start of the course
        self.start_hours_array = [str(x).zfill(2) for x in range(8, 21)]

        # array containing hours for the end of the course
        self.end_hours_array = [str(x).zfill(2) for x in range(9, 23)]

        # array containing minutes for the course timings
        self.minutes_array = [str(x).zfill(2) for x in range(0, 60, 15)]

        # initialising string that will be used in the making of the pop-up window
        self.unfilled_window_title = 'Empty Fields'
        self.unfilled_window_text = 'Please fill all required fields'

        self.incorrect_window_title = 'Incorrect Data'
        self.incorrect_window_text = 'Please enter correct data'

        self.clear_window_title = 'Clear Details?'
        self.clear_window_label = 'Are you sure you want to clear details?'

        self.submit_window_title = 'Submit Details?'
        self.submit_window_label = 'Are you sure you want to save details?'

        self.success_window_title = 'Successful submission'
        self.success_window_text = 'The schedule details have been successfully saved.'

        # calling this function to place all created widgets on screen
        self.__frame_elements()

    # public function used to retrieve the private attribute 'frame'
    def get_frame(self):
        return self.__frame

    # private function contaning everything to do with making the screen
    def __frame_elements(self):
        # creating labels for the schedule frame
        Label(self.__frame, text='Day*', font=(style.main_font, 25), fg=style.orange).place(x=400)
        Label(self.__frame, text='Start Time*', font=(style.main_font, 25), fg=style.orange).place(x=400, y=90)
        Label(self.__frame, text='End Time*', font=(style.main_font, 25), fg=style.orange).place(x=400, y=180)
        Label(self.__frame, text='Description', font=(style.main_font, 25), fg=style.orange).place(x=400, y=270)

        # creating dropdowns so that the user has limited input for certain fields
        self.day_dropdown = self.make_dropdown(self.__frame, values=self.days_array, font=(style.main_font, 20),
                                               initial='', x=700, y=00, width=25)
        self.start_hour_dropdown = self.make_dropdown(self.__frame, values=self.start_hours_array,
                                                      font=(style.main_font, 20), initial='Hours', x=700, y=90, width=9)
        self.start_minute_dropdown = self.make_dropdown(self.__frame, values=self.minutes_array,
                                                        font=(style.main_font, 20), initial='Minutes', x=920, y=90,
                                                        width=9)
        self.end_hour_dropdown = self.make_dropdown(self.__frame, values=self.end_hours_array,
                                                    font=(style.main_font, 20), initial='Hours', x=700, y=180, width=9)
        self.end_minute_dropdown = self.make_dropdown(self.__frame, values=self.minutes_array,
                                                      font=(style.main_font, 20), initial='Minutes', x=920, y=180,
                                                      width=9)

        # creating a text box for multiline inputs for description
        self.description_textbox = self.make_textbox(self.__frame, font=(style.main_font, 15), height=5, width=35,
                                                     borderwidth=10, x=700, y=270)

        # making a button to clear all fields without saving so user can reset and reenter data
        self.clear_button = self.make_button(self.__frame, text="Clear", font=(style.main_font, 20), width=7,
                                             command=lambda: self.make_confirm_window(self.clear_window_title,
                                                                                      self.clear_window_label,
                                                                                      self.__clear),
                                             state='normal', x=620, y=450)

        # making a submit button to save details after certain validation checks
        self.submit_button = self.make_button(self.__frame, text="Submit", font=(style.main_font, 20), width=7,
                                              command=lambda: self.make_confirm_window(self.submit_window_title,
                                                                                       self.submit_window_label,
                                                                                       self.__create_object),
                                              state='normal', x=740, y=450)

    # private function to clear user entries on GUI
    def __clear(self):
        # resetting input fields so that more data can be added
        self.day_dropdown.set('')
        self.start_hour_dropdown.set('Hours')
        self.start_minute_dropdown.set('Minutes')
        self.end_hour_dropdown.set('Hours')
        self.end_minute_dropdown.set('Minutes')
        self.description_textbox.delete("1.0", "end")

    # private function to create schedule object and save it in file
    def __create_object(self):
        # fetching details that have been entered
        self.day_dropdown_content = self.day_dropdown.get()
        self.start_hour_dropdown_content = self.start_hour_dropdown.get()
        self.start_minute_dropdown_content = self.start_minute_dropdown.get()
        self.end_hour_dropdown_content = self.end_hour_dropdown.get()
        self.end_minute_dropdown_content = self.end_minute_dropdown.get()
        self.description_textbox_content = self.description_textbox.get('1.0')

        # checking for unfilled details - if they exist, then display an error window
        # the description field is optional
        if not self.day_dropdown_content \
                or self.start_hour_dropdown_content == 'Hours' \
                or self.start_minute_dropdown_content == 'Minutes' \
                or self.end_hour_dropdown_content == 'Hours' \
                or self.end_minute_dropdown_content == 'Minutes':

            # making an error window if all fields aren't filled
            self.unfilled_fields_master = self.make_notification_window(self.unfilled_window_title, self.unfilled_window_text)

        # if all details filled:
        else:
            # checking for validity of the timings input (i.e. start time < end time)
            # concatenating the two start hour and minute into one string and converting to integers
            self.start_combination = int(self.start_hour_dropdown_content + self.start_minute_dropdown_content)

            # concatenating the two end hour and minute into one string and converting to integers
            self.end_combination = int(self.end_hour_dropdown_content + self.end_minute_dropdown_content)

            # end minus start should be positive. if negative, display error window
            self.difference = self.end_combination - self.start_combination

            # if class ends before it starts:
            if self.difference < 0:
                # making an error window if invalid data has been entered
                self.incorrect_data_master = self.make_notification_window(self.incorrect_window_title,
                                                                           self.incorrect_window_text)
            else:
                # all validation checks passed
                # calling the read function from the file handler to read binary file
                self.all_entities_array = binary_file_reader()

                # converting the times to string so that they can be 2 digits
                self.start_combination = str(self.start_combination).zfill(4)
                self.end_combination = str(self.end_combination).zfill(4)

                # creating new schedule object
                self.created_schedule_object = NewSchedule(self.day_dropdown_content,
                                                           self.start_combination,
                                                           self.end_combination,
                                                           self.description_textbox_content)

                # saving the new course object
                self.created_schedule_object.save(self.created_schedule_object)

                # after details have been saved, the fields can be cleared for further entry
                self.__clear()

                # displaying that the schedule object has been saved
                self.make_notification_window(self.success_window_title, self.success_window_text, x=20)
