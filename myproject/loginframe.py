from tkinter import Tk, Label
from tkinter import ttk

import style
from screens import Screens
from widgets import Widgets
from encryption import encrypt, decrypt
from file_handler import binary_file_reader, binary_file_writer


class Login(Widgets):
    def __init__(self, root):
        super().__init__()
        self.login_root = root
        self.login_root.title('Login')
        self.login_root.iconbitmap(r"images/App_icon.ico")
        self.login_root.state('zoomed')

        # initialising strings that will later be used in the making of pop-up windows
        self.unfilled_window_title = 'Empty Fields'
        self.unfilled_window_text = 'Please fill all required fields'

        self.username_exists_window_title = 'Username Exists'
        self.username_exists_window_text = 'This username already exists. Enter a new one.'

        self.no_username_window_title = 'Username Not Found'
        self.no_username_window_text = 'Please enter a valid username.'

        self.incorrect_password_window_title = 'Incorrect Password'
        self.incorrect_password_window_text = 'Pleae enter a valid password.'

        self.success_window_title = 'Successful login'
        self.success_window_text = 'The login was successful.'

        # calling this function to place all created widgets on screen
        self.__frame_elements()

    # function contaning everything to do with making the screen
    def __frame_elements(self):
        # making the title text on 2 different lines
        Label(self.login_root, text="GENIUS", font=(style.title_font, 50, "bold"), fg=style.cyan_blue).place(x=600, y=50)
        Label(self.login_root, text="ASSEMBLY", font=(style.title_font, 50, "bold"), fg=style.cyan_blue).place(x=700, y=130)

        # creating labels for the login frame
        Label(self.login_root, text='Username*', font=(style.main_font, 25), fg=style.orange).place(x=450, y=320)
        Label(self.login_root, text='Password*', font=(style.main_font, 25), fg=style.orange).place(x=450, y=450)

        self.login_username_entrybox = self.make_entrybox(self.login_root, font=(style.main_font, 20), x=750, y=320,
                                                          width=21)
        self.login_password_entrybox = self.make_entrybox(self.login_root, font=(style.main_font, 20), x=750, y=450,
                                                          width=21, show='*')

        self.signup_button = self.make_button(self.login_root, text="Sign Up", font=(style.main_font, 20), width=7,
                                              command=self.signup, state='normal', x=640, y=600)
        self.login_button = self.make_button(self.login_root, text="Login", font=(style.main_font, 20), width=7,
                                             command=self.__login, state='normal', x=760, y=600)

    # function to allow users to make new accounts
    def signup(self):
        self.sign_in_master = Tk()
        self.style = ttk.Style(self.sign_in_master)
        self.style.theme_use('clam')
        self.sign_in_master.geometry('650x300+450+350')
        self.sign_in_master.iconbitmap(r'App_icon.ico')
        self.sign_in_master.title('Sign Up')

        # creating labels for the login frame
        Label(self.sign_in_master, text='Username*', font=(style.main_font, 25), fg=style.orange).place(x=50, y=40)
        Label(self.sign_in_master, text='Password*', font=(style.main_font, 25), fg=style.orange).place(x=50, y=140)

        self.signup_username_entrybox = self.make_entrybox(self.sign_in_master, font=(style.main_font, 18), x=360, y=42,
                                                           width=18)
        self.signup_password_entrybox = self.make_entrybox(self.sign_in_master, font=(style.main_font, 18), x=360, y=142,
                                                           width=18)

        self.submit_button = self.make_button(self.sign_in_master, text="Submit", font=(style.main_font, 18), width=7,
                                              command=self.__submit_new_user, state='normal', x=495, y=230)
        self.sign_in_master.mainloop()

    # function to save created user
    def __submit_new_user(self):
        self.signup_username_entrybox_content = self.signup_username_entrybox.get()
        self.signup_password_entrybox_content = self.signup_password_entrybox.get()

        if not self.signup_password_entrybox_content or not self.signup_username_entrybox_content:

            # error window if all fields aren't filled
            self.unfilled_fields_master = self.make_notification_window(self.unfilled_window_title, self.unfilled_window_text)

        else:
            self.all_entities_array = binary_file_reader()
            self.username_details = self.all_entities_array[7]
            if self.signup_username_entrybox_content in self.username_details:
                # error window if username already exists
                self.preexisting_username_master = self.make_notification_window(self.username_exists_window_title,
                                                                                 self.username_exists_window_text, x=50)
            else:
                # adding the new user to the dictionary and saving the contents by writing it onto the file after encryption
                self.all_entities_array[7][self.signup_username_entrybox_content] = encrypt(self.signup_password_entrybox_content, 1)
                binary_file_writer(self.all_entities_array)
                self.sign_in_master.destroy()

    # function to validate login entries
    def __login(self):
        self.login_username_entrybox_content = self.login_username_entrybox.get()
        self.login_password_entrybox_content = self.login_password_entrybox.get()
        if not self.login_password_entrybox_content or not self.login_username_entrybox_content:

            # error window if all fields aren't filled
            self.unfilled_fields_master = self.make_notification_window(self.unfilled_window_title, self.unfilled_window_text)

        else:
            # reading the contents of the file to ensure that even if new users have been created, they are accounted for
            self.all_entities_array = binary_file_reader()
            self.username_details = self.all_entities_array[7]    # the dictionary containing username details
            if self.login_username_entrybox_content in self.username_details:   # checking if the username entered exists
                # checking if the passwords match
                if decrypt(self.username_details[self.login_username_entrybox_content], 1) == self.login_password_entrybox_content:
                    # closing login window and opening the application window once a successful login has been made
                    self.make_notification_window(self.success_window_title, self.success_window_text, x=150)
                    self.login_root.destroy()
                    self.app_root = Tk()
                    self.application = Screens(self.app_root)
                    self.app_root.mainloop()
                else:
                    # error window if username and password don't match
                    self.incorrect_password_master = self.make_notification_window(self.incorrect_password_window_title,
                                                                                   self.incorrect_password_window_text)
            else:
                # error window if username not found
                self.no_username_master = self.make_notification_window(self.no_username_window_title,
                                                                        self.no_username_window_text)
