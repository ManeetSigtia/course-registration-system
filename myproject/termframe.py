from tkinter import Tk, Label, Button, Frame, PhotoImage
from tkinter import ttk
from tkinter.font import Font
from datetime import datetime, timedelta
import os

import style
from widgets import Widgets
from quicksort import quicksort
from verify import Validation
from file_handler import binary_file_reader, binary_file_writer, text_file_writer


class NewTerm:
    # class to generate terms for each registration
    def __init__(self, term_id, course, student, sessions, fee, start, end, discount_type, discount_amount,
                 payment_method, amount_paid, payment_date, account_name, status, registration_id, more_terms):
        self.term_id = term_id
        self.registration_id = registration_id
        self.course_name = course
        self.student_name = student
        self.no_of_sessions = sessions
        self.start_date = start
        self.end_date = end
        self.discount_type = discount_type
        self.discount_amount = discount_amount
        self.course_fee = fee
        self.payment_method = payment_method
        self.amount_paid = amount_paid
        self.payment_date = payment_date
        self.account_name = account_name
        self.status = status
        self.term_checker = more_terms


class TermFrame(Widgets, Validation):
    # inheriting from the Widgets and the Check class
    def __init__(self, root):
        super().__init__()
        # creating a frame in which all widgets will be added
        self.__frame = Frame(root, width=style.frame_width, height=style.frame_height)

        # determining the font in the dropdowns in the window for aesthetics purposes
        self.dropdown_size = Font(family=style.main_font, size=13)
        self.__frame.option_add("*TCombobox*Listbox*Font", self.dropdown_size)

        # image that will be used for the search button
        self.search_image = PhotoImage(file=os.path.join(os.path.dirname(__file__), "images", "search_1.png"))

        # list used in the discount type dropdown
        self.discount_types_array = ["None", "Early Bird", "Packaged", "Referral", "Sibling"]

        # list used in the payment method dropdown
        self.payment_methods_array = ["Bank Transfer", "PayLah", "PayNow"]

        # list used in the status dropdown
        self.statuses_array = ["NT Pending", "Paid", "In-Progress", "Closed"]

        # initialising strings that will later be used in the making of pop-up windows
        self.incorrect_window_title = 'Incorrect Data'
        self.incorrect_window_label = 'Please enter correct data.'

        self.delete_window_title = 'Delete Term?'
        self.delete_window_label = 'Are you sure you want to delete this term?'

        self.save_window_title = 'Save Terms?'
        self.save_window_label = 'Are you sure you want to file details?'

        self.edit_window_title = 'Unchosen term'
        self.edit_window_label = 'Please choose a valid term to edit.'

        self.delete_error_window_title = 'Unchosen term'
        self.delete_error_window_label = 'Please choose a valid term to delete.'

        self.unfilled_window_title = 'Empty Fields'
        self.unfilled_window_text = 'Please fill all required fields'

        self.success_term_window_title = 'Successful submission'
        self.success_term_window_text = 'The term details have been successfully saved.'

        # reading the file to get the updated version of the course objects
        self.all_entities_array = binary_file_reader()

        # calling this function to place all created widgets on screen
        self.__frame_elements()

        # inserting data into the table when the program starts
        self.__insert_data()

    # public function used to retrieve the private attribute 'frame'
    def get_frame(self):
        return self.__frame

    # function contaning everything to do with making the screen
    def __frame_elements(self):
        # creating labels for the frame
        Label(self.__frame, text='Search by courses:', font=(style.main_font, 14), fg=style.orange).place(x=100, y=20)
        Label(self.__frame, text='Search by students:', font=(style.main_font, 14), fg=style.orange).place(x=530, y=20)
        Label(self.__frame, text='Search by status:', font=(style.main_font, 14), fg=style.orange).place(x=1000, y=20)

        # creating dropdowns so that the user has limited input for certain fields
        self.course_search_dropdown = self.make_dropdown(self.__frame, values=['None'] + self.all_entities_array[0],
                                                         font=(style.main_font, 11), initial='', x=260, y=25, width=27)
        self.status_search_dropdown = self.make_dropdown(self.__frame, values=['None'] + self.statuses_array,
                                                         font=(style.main_font, 11), initial='', x=1180, y=25, width=20)

        self.student_search_entrybox = self.make_entrybox(self.__frame, font=(style.main_font, 11), x=720, y=25, width=25,
                                                          borderwidth=3)
        # an array containing the header values for the table that will display the reports
        self.term_table_columns = ["", "Term ID", "Course Name", "Student Name", "Sessions", "Course Fee",
                                   "Start Date", "End Date", "Discount Type", "Discount Amount", "Payment Method",
                                   "Amount Paid", "Payment Date", "Account Name", "Status"]
        # array containing the width of each column
        self.term_table_columns_width = [0, 60, 210, 110, 65, 80, 85, 95, 100, 110, 120, 100, 100, 110, 90]

        # making table that will be used to show the individual term details
        self.term_table = self.make_table(self.__frame, 0, 100, self.term_table_columns_width, self.term_table_columns,
                                          height=13)
        # binding the table to the mouse click to carry out certain actions
        # it is an input method that is used to increase user convenvience
        self.term_table.bind("<Button-1>", self.__enable_buttons)

        # each row in the table will be shown in alternating colours for aesthetic purposes and clarity
        self.striped_rows(self.term_table)

        # making a button to allow user to search for a particular term based on course name, student name and status
        self.search_student_button = Button(self.__frame, image=self.search_image, font=(style.main_font, 13),
                                            width=20, command=self.__insert_data, state='normal')
        self.search_student_button.place(x=1450, y=20)

        # making a button to allow user to edit a selected term
        self.edit_button = self.make_button(self.__frame, text="Edit", font=(style.main_font, 15), width=7,
                                            command=self.__edit, state='disabled', x=615, y=500)

        # making a button to allow users to export reports to a text file
        self.save_text_button = self.make_button(self.__frame, text="Save", font=(style.main_font, 15), width=7,
                                                 command=lambda: self.make_confirm_window(self.save_window_title,
                                                                                          self.save_window_label,
                                                                                          self.__save_in_textfile),
                                                 state='normal', x=725, y=500)

        # making a button to permanently delete a selected term
        self.delete_button = self.make_button(self.__frame, text="Delete", font=(style.main_font, 15), width=7,
                                              command=lambda: self.make_confirm_window(self.delete_window_title,
                                                                                       self.delete_window_label,
                                                                                       self.__delete), state='disabled',
                                              x=835, y=500)

        # setting the colour of the buttons to dark blue to indicate they are disabled and cant be used
        self.edit_button.config(bg=style.dark_blue)
        self.delete_button.config(bg=style.dark_blue)

    # function to enable buttons if user clicks on table
    def __enable_buttons(self, event):
        self.edit_button.config(state='normal', bg=style.cyan_blue)
        self.delete_button.config(state='normal', bg=style.cyan_blue)

    # function to disable buttons
    def __disable_buttons(self):
        self.edit_button.config(state='disabled', bg=style.dark_blue)
        self.delete_button.config(state='disabled', bg=style.dark_blue)

    # function to determine selected row and corresponding values
    def __edit(self):
        # pre-filling details into the window from the terms table for ease of user
        # selecting a row to edit
        self.selected_row = self.term_table.focus()

        # loading values from that row into a variable
        self.table_values = self.term_table.item(self.selected_row, 'values')

        if not self.table_values:
            # making an error window if a term has not been selected
            self.make_notification_window(self.edit_window_title, self.edit_window_label)
        else:
            # creating a new window to input new details for the selected term
            self.__make_edit_window()

    # function to delete a term
    def __delete(self):
        # reading the file to get the updated version of the term objects
        self.all_entities_array = binary_file_reader()
        try:
            # determining which term has been selected
            self.selected_row = self.term_table.focus()

            # deleting term based on the index position of the selected row from the table
            self.all_entities_array[6].pop(int(self.selected_row))

            # writing the array after the dleetion of the term back onto the file
            binary_file_writer(self.all_entities_array)

            # inserting term details into the table and re-disabling the buttons
            self.__insert_data()
            self.__disable_buttons()
        except:
            # making an error window if a term has not been selected
            self.make_notification_window(self.delete_error_window_title, self.delete_error_window_label)

    # function to generate reports in text file
    def __save_in_textfile(self):
        # header that will be written onto the text file
        # also the string to which the relevant term details will be concatenated
        self.final_string = 'Registration ID,Term ID,Course Name,Student Name,Sessions,Course Fee,Start Date,End Date,' \
                            'Discount Type,Discount Amount,Payment Method,Amount Paid,Payment Date,Account Name,Status'

        # reading the terms object array from the binary file
        self.term_object_array = binary_file_reader()[6]

        # looping through the terms object array
        for term in self.term_object_array:
            # writing the details of each term as an element of an array and making it a string
            term_details_array = [term.registration_id, term.term_id, term.course_name, term.student_name,
                                  str(term.no_of_sessions), str(term.course_fee), term.start_date, term.end_date,
                                  term.discount_type, str(term.discount_amount), term.payment_method,
                                  str(term.amount_paid), term.payment_date, term.account_name, term.status]

            # joining all the elements (concatenating)
            self.row_string = ','.join(term_details_array)

            # adding each record on a new line
            self.final_string += '\n' + self.row_string

        # writing the final string onto the file
        text_file_writer(self.final_string, 'terms')

        # displaying that the term details have been saved to the text file
        self.make_notification_window(self.success_term_window_title, self.success_term_window_title)

    # function to make a new window for editing terms
    def __make_edit_window(self):
        # initialising the root window
        self.edit_master = Tk()

        # styling the new window the created
        self.style = ttk.Style(self.edit_master)
        self.style.theme_use('clam')
        self.edit_master.geometry('780x350+450+330')
        self.edit_master.iconbitmap(r'images/App_icon.ico')
        self.edit_master.title('Edit Details')

        # setting the initial pivot position based on which the label y values of the lable will change
        self.title_y = 20

        # creating labels for the term edit window
        Label(self.edit_master, text='No. of sessions*', font=(style.main_font, 16), fg=style.orange).place(x=20,
                                                                                                            y=self.title_y)
        Label(self.edit_master, text='End date*', font=(style.main_font, 16), fg=style.orange).place(x=20,
                                                                                                     y=self.title_y + 60)
        Label(self.edit_master, text='DD/MM/YYYY', font=(style.main_font, 16), fg=style.orange).place(x=20,
                                                                                                      y=self.title_y + 90)
        Label(self.edit_master, text='Discount type', font=(style.main_font, 16), fg=style.orange).place(x=20,
                                                                                                         y=self.title_y + 150)
        Label(self.edit_master, text='Discount amount', font=(style.main_font, 16), fg=style.orange).place(x=20,
                                                                                                           y=self.title_y + 210)
        Label(self.edit_master, text='Payment method', font=(style.main_font, 16), fg=style.orange).place(x=20,
                                                                                                          y=self.title_y + 270)
        Label(self.edit_master, text='Amount paid', font=(style.main_font, 16), fg=style.orange).place(x=420,
                                                                                                       y=self.title_y)
        Label(self.edit_master, text='Payment date', font=(style.main_font, 16), fg=style.orange).place(x=420,
                                                                                                        y=self.title_y + 60)
        Label(self.edit_master, text='DD/MM/YYYY', font=(style.main_font, 16), fg=style.orange).place(x=420,
                                                                                                      y=self.title_y + 90)
        Label(self.edit_master, text='Account name', font=(style.main_font, 16), fg=style.orange).place(x=420,
                                                                                                        y=self.title_y + 150)
        Label(self.edit_master, text='Status', font=(style.main_font, 16), fg=style.orange).place(x=420,
                                                                                                  y=self.title_y + 210)

        # creating entryboxes so that number of sessions and course fee can be entered
        self.number_of_sessions_entrybox = self.make_entrybox(self.edit_master, font=(style.main_font, 13),
                                                              width=15, x=200, y=self.title_y)
        self.end_date_entrybox = self.make_entrybox(self.edit_master, font=(style.main_font, 13), width=15,
                                                    x=200, y=self.title_y + 75)
        self.discount_amount_entrybox = self.make_entrybox(self.edit_master, font=(style.main_font, 13), width=15,
                                                           x=200, y=self.title_y + 210)
        self.amount_paid_entrybox = self.make_entrybox(self.edit_master, font=(style.main_font, 13), width=15,
                                                       x=600, y=self.title_y)
        self.payment_date_entrybox = self.make_entrybox(self.edit_master, font=(style.main_font, 13), width=15,
                                                        x=600, y=self.title_y + 60)
        self.account_name_entrybox = self.make_entrybox(self.edit_master, font=(style.main_font, 13), width=15,
                                                        x=600, y=self.title_y + 150)

        # creating dropdowns so that the user has limited input for certain fields
        self.discount_type_dropdown = self.make_dropdown(self.edit_master, values=self.discount_types_array,
                                                         font=(style.main_font, 13), initial='None', width=14,
                                                         x=200, y=self.title_y + 150)
        self.payment_method_dropdown = self.make_dropdown(self.edit_master, values=self.payment_methods_array,
                                                          font=(style.main_font, 13), initial='Bank Transfer',
                                                          width=14, x=200, y=self.title_y + 270)
        self.status_dropdown = self.make_dropdown(self.edit_master, values=self.statuses_array,
                                                  font=(style.main_font, 13), initial='NT Pending', width=14,
                                                  x=600, y=self.title_y + 210)

        # making a submit button to save details after certain validation checks
        self.submit_button = self.make_button(self.edit_master, text='Submit', font=(style.main_font, 14), width=7,
                                              command=self.__submit_edits, x=520, y=self.title_y + 270, state='normal')

        # preinserting details in the widgets for user convenience
        # the user only needs to change the details that they want to rather than inserting all the details again
        self.number_of_sessions_entrybox.insert(0, self.table_values[3])
        self.end_date_entrybox.insert(0, self.table_values[6])
        self.discount_type_dropdown.set(self.table_values[7])
        self.discount_amount_entrybox.insert(0, self.table_values[8])
        self.payment_method_dropdown.set(self.table_values[9])
        self.amount_paid_entrybox.insert(0, self.table_values[10])
        self.payment_date_entrybox.insert(0, self.table_values[11])
        self.account_name_entrybox.insert(0, self.table_values[12])
        self.status_dropdown.set(self.table_values[13])
        self.edit_master.mainloop()

    # function to save edited term
    def __submit_edits(self):
        # calling the read function from file handler
        # reading the term list and making it an attribute of this class
        self.all_entities_array = binary_file_reader()
        self.edited_term_object = self.all_entities_array[6][int(self.selected_row)]

        # fetching the deta from the fields
        self.number_of_sessions_entrybox_content = self.number_of_sessions_entrybox.get()
        self.end_date_entrybox_content = self.end_date_entrybox.get()
        self.discount_type_dropdown_content = self.discount_type_dropdown.get()
        self.discount_amount_entrybox_content = self.discount_amount_entrybox.get()
        self.payment_method_dropdown_content = self.payment_method_dropdown.get()
        self.amount_paid_entrybox_content = self.amount_paid_entrybox.get()
        self.payment_date_entrybox_content = self.payment_date_entrybox.get()
        self.account_name_entrybox_content = self.account_name_entrybox.get()
        self.status_dropdown_content = self.status_dropdown.get()

        if not self.number_of_sessions_entrybox_content or not self.end_date_entrybox_content:
            # if the required details, i.e. number of sessions and end date have not been entered
            # display an error message
            self.make_notification_window(self.unfilled_window_title, self.unfilled_window_text)
        else:
            # determining if the number of sessions is a decimal
            if type(self.number_of_sessions_entrybox_content) == float:
                self.sessions = False
                # displaying an error if the sessions entered is not of type integer
                self.make_notification_window(self.incorrect_window_title, self.incorrect_window_label)
            else:
                self.sessions_checker = True
                try:
                    # checking if the sessions entered is of type integer
                    int(self.number_of_sessions_entrybox_content)
                except:
                    # displaying an error if the sessions entered is not of type integer
                    self.make_notification_window(self.incorrect_window_title, self.incorrect_window_label)
                    self.sessions_checker = False
            if self.sessions_checker:
                # converting start date to datetime format
                self.datetime_formatted_day = datetime.strptime(self.edited_term_object.start_date, "%d/%m/%Y")

                # making an array that will hold all future dates for the class
                self.future_dates = []
                for no_of_weeks in range(int(self.number_of_sessions_entrybox_content)):

                    # adding 7 days to the start day for number of sessions for that course
                    next_day = self.datetime_formatted_day + timedelta(days=7 * no_of_weeks)

                    # adding this day on the array for future dates so that they can be seen later
                    # converting to string and adding it
                    self.future_dates.append(next_day.strftime('%d/%m/%Y'))

                # a condition to check the validity of the data entered
                self.amount_and_date_checker = True

                # in discount amount, amount_paid and payment_date
                # checking if either of the 3 fields have been entered
                if self.end_date_entrybox_content != '':
                    try:
                        self.split_end_date = self.end_date_entrybox_content.split('/')
                        self.validate_date(int(self.split_end_date[2]), int(self.split_end_date[1]),
                                           int(self.split_end_date[0]))
                        if not self.boolean_date_verifier:
                            # only if the data has been entered, it must be in the correct format
                            # the payment date must be legitimate (e.g. 31/02/2021 would be rejected)
                            self.make_notification_window(self.incorrect_window_title, self.incorrect_window_label)
                            self.amount_and_date_checker = False
                    except:
                        # displaying an error window since the date entered is invalid
                        self.make_notification_window(self.incorrect_window_title, self.incorrect_window_label)
                        self.amount_and_date_checker = False
                else:
                    # displaying an error window since the required field 'end date' has not been entered
                    self.make_notification_window(self.unfilled_window_title, self.unfilled_window_text)

                if self.discount_amount_entrybox_content != '':
                    # validating discount amount if it has been ented by the user
                    self.validate_fees(self.discount_amount_entrybox_content)
                    if not self.boolean_fees_verifier:
                        # only if the data has been entered, it must be in the correct format
                        # only numbers and decimals are allowed for this field
                        # displaying an error window since invalid data has been entered
                        self.make_notification_window(self.incorrect_window_title, self.incorrect_window_label)
                        self.amount_and_date_checker = False

                if self.amount_paid_entrybox_content != '':
                    # validating amount paid if it has been ented by the user
                    self.validate_fees(self.amount_paid_entrybox_content)
                    if not self.boolean_fees_verifier:
                        # only if the data has been entered, it must be in the correct format
                        # only numbers and decimals are allowed for this field
                        # displaying an error window since invalid data has been entered
                        self.make_notification_window(self.incorrect_window_title, self.incorrect_window_label)
                        self.amount_and_date_checker = False

                if self.payment_date_entrybox_content != '':
                    try:
                        self.split_payment_date = self.payment_date_entrybox_content.split('/')
                        self.validate_date(int(self.split_payment_date[2]), int(self.split_payment_date[1]),
                                           int(self.split_payment_date[0]))
                        if not self.boolean_date_verifier:
                            # only if the data has been entered, it must be in the correct format.
                            # the payment date must be legitimate (e.g. 31/02/2021 would be rejected)
                            # displaying an error window since invalid data has been entered
                            self.make_notification_window(self.incorrect_window_title, self.incorrect_window_label)
                            self.amount_and_date_checker = False
                    except:
                        # only if the data has been entered, it must be in the correct format.
                        # the payment date must be legitimate (e.g. 31/02/2021 would be rejected)
                        # displaying an error window since invalid data has been entered
                        self.make_notification_window(self.incorrect_window_title, self.incorrect_window_label)
                        self.amount_and_date_checker = False

                if self.amount_and_date_checker:
                    # updating attributes for the required term chosen by the user
                    self.edited_term_object.end_date = self.future_dates[-1]
                    self.edited_term_object.no_of_sessions = self.number_of_sessions_entrybox_content
                    self.edited_term_object.end_date = self.end_date_entrybox_content
                    self.edited_term_object.discount_type = self.discount_type_dropdown_content
                    self.edited_term_object.discount_amount = self.discount_amount_entrybox_content
                    self.edited_term_object.payment_method = self.payment_method_dropdown_content
                    self.edited_term_object.amount_paid = self.amount_paid_entrybox_content
                    self.edited_term_object.payment_date = self.payment_date_entrybox_content
                    self.edited_term_object.account_name = self.account_name_entrybox_content
                    self.edited_term_object.status = self.status_dropdown_content

                    # changing the attribute on the term objects array
                    self.all_entities_array[6][int(self.selected_row)] = self.edited_term_object

                    # saving the term objects array
                    binary_file_writer(self.all_entities_array)

                    # updating the sessions on the new course file as well
                    self.__course_session_changer()

                    # adding new terms depending on the whether status changed from pending to paid
                    self.__term_adder()

                    # inserting updated data into the table
                    self.__insert_data()

                    # disabling buttons so that no error is thrown
                    self.__disable_buttons()

                    self.make_notification_window(self.success_term_window_title, self.success_term_window_text, x=50)
                    self.edit_master.destroy()

    # function to enter term details into table
    def __insert_data(self):
        self.all_entities_array = binary_file_reader()

        # clearing all previous fields present in the table
        for record in self.term_table.get_children():
            self.term_table.delete(record)

        #  will be used to determine the colour of a particular row in the table
        self.table_row_counter = 0

        # array containing all the term objects
        self.terms_object_array = self.all_entities_array[6]

        # sorting the array using quicksort and storing it in a new variable
        self.sorted_term_info = quicksort(0, len(self.terms_object_array) - 1, self.terms_object_array)  # sorting the array
        # before entering data into the table

        # fetching the search conditions
        self.course_search_dropdown_content = self.course_search_dropdown.get()
        self.student_search_entrybox_content = self.student_search_entrybox.get()
        self.status_search_dropdown_content = self.status_search_dropdown.get()

        # if no search condition is given, i.e. if None is chosen, the search condition is an empty string
        if self.status_search_dropdown_content == 'None':
            self.status_search_dropdown_content = ''
        if self.course_search_dropdown_content == 'None':
            self.course_search_dropdown_content = ''

        # looping through all term ojbects
        for term in self.terms_object_array:
            # checking if any of the search criteria have been provided, and if they have, whether they match
            # searching for the terms with course names that match the course name provided by user
            if self.course_search_dropdown_content in term.course_name:
                # searching for the terms with student names that match the student name provided by user
                if self.student_search_entrybox_content.lower().strip() in term.student_name.lower():
                    # searching for the terms with status that match the status provided by user
                    if self.status_search_dropdown_content in term.status:

                        # only choosing the objects that meet the criteria
                        self.row_of_terms = (term.term_id, term.course_name, term.student_name, term.no_of_sessions,
                                             term.course_fee, term.start_date, term.end_date, term.discount_type,
                                             term.discount_amount, term.payment_method, term.amount_paid,
                                             term.payment_date, term.account_name, term.status)

                        # determining the colour of the row and based on that inserting data
                        if self.table_row_counter % 2 == 1:
                            self.term_table.insert(parent='', index='end', iid=self.table_row_counter, text='',
                                                   values=self.row_of_terms, tags=('even',))
                        else:
                            self.term_table.insert(parent='', index='end', iid=self.table_row_counter, text='',
                                                   values=self.row_of_terms, tags=('odd',))
                        self.table_row_counter += 1

    # function to change course sessions in corresponding course objects
    def __course_session_changer(self):
        self.course_objects_array = self.all_entities_array[2]
        self.term_objects_array = self.all_entities_array[6]

        for objects in self.course_objects_array:
            # determining which course's session has been changed based on the registration id
            if objects.course_id == self.term_objects_array[int(self.selected_row)].registration_id[0:6]:
                # making the edit to the course session
                objects.duration = self.number_of_sessions_entrybox_content

    # function to automatically generate consecutive term if status is changed from pending to paid
    def __term_adder(self):
        # looping through the file contents to determine which term has been changed to paid
        for index in range(len(self.term_objects_array)):
            self.term_object = self.term_objects_array[index]
            if self.term_object.status == "Paid" and not self.term_object.term_checker:
                # if a new term is created, it should not be created again when the status is edited,
                # since it would result in a copy
                self.term_object.term_checker = True

                # calculating the dates for the new term created
                # converting to datetime format
                current_end_date = datetime.strptime(self.term_object.end_date, "%d/%m/%Y")

                # finding future start date in datetime format
                future_start_date = (current_end_date + timedelta(days=7))

                # finding future end date in datetime format, assuming the number of days is constant for that term
                future_end_date = future_start_date + timedelta(days=7 * (int(self.term_object.no_of_sessions) - 1))

                # converting both the dates from datetime to string
                future_start_date = future_start_date.strftime('%d/%m/%Y')
                future_end_date = future_end_date.strftime('%d/%m/%Y')

                # making a new term object for the same registration with all calculated attributes
                self.new_term = NewTerm(str(int(self.term_object.term_id) + 1).zfill(2), self.term_object.course_name,
                                        self.term_object.student_name, self.term_object.no_of_sessions,
                                        self.term_object.course_fee, future_start_date, future_end_date,
                                        self.term_object.discount_type, self.term_object.discount_amount,
                                        self.term_object.payment_method, self.term_object.amount_paid,
                                        self.term_object.payment_date, self.term_object.account_name, "NT Pending",
                                        self.term_object.registration_id, False)

                # inserting it into the file so that it appears right below the previous term
                self.all_entities_array[6].insert(index + 1, self.new_term)

                # writing the edited array back onto the file
                binary_file_writer(self.all_entities_array)
