from tkinter import Label, Button, Frame

import style
from courseframe import CourseFrame
from studentframe import StudentFrame
from scheduleframe import ScheduleFrame
from reportframe import ReportFrame
from registerframe import RegisterFrame
from termframe import TermFrame


class Screens:
    def __init__(self, root):
        # customizing the main window
        self.root = root
        self.root.title('Genius Assembly Management System')
        self.root.iconbitmap(r"images/App_icon.ico")
        self.root.state('zoomed')

        # stack which will control the back flow of frame objects
        self.back_stack = []

        # making the back button
        # when clicked, takes user to the previous frame they were at
        self.back_button = Button(self.root, text='Back', font=(style.main_font, 20), width=5, bg=style.dark_blue,
                                  fg=style.gray, command=self.__go_back, state='disabled')
        self.back_button.place(x=30, y=65)

        # making the title text on 2 different lines
        self.heading1 = Label(self.root, text="GENIUS", font=(style.title_font, 50, "bold"),
                              fg=style.cyan_blue).place(x=600, y=50)
        self.heading2 = Label(self.root, text="ASSEMBLY", font=(style.title_font, 50, "bold"),
                              fg=style.cyan_blue).place(x=700, y=130)

        # making the objects from different user defined classes. These will be used to display all the widgets
        self.course_object = CourseFrame(root)
        self.student_object = StudentFrame(root)
        self.schedule_object = ScheduleFrame(root)
        self.register_object = RegisterFrame(root)
        self.report_object = ReportFrame(root)
        self.term_object = TermFrame(root)

        # making the frames from each of the above class as attributes so that they can be worked with later
        self.course_frame = self.course_object.get_frame()
        self.student_frame = self.student_object.get_frame()
        self.schedule_frame = self.schedule_object.get_frame()
        self.register_frame = self.register_object.get_frame()
        self.report_frame = self.report_object.get_frame()
        self.term_frame = self.term_object.get_frame()

        # making the the home frame with buttons leading to other frames
        self.home_frame = Frame(root, width=style.frame_width, height=style.frame_height)

        # these are texts that appear on the screen on the home frame
        self.add_new_label = Label(self.home_frame, text="Add", font=(style.main_font, 30),
                                   fg=style.orange).place(x=50, y=50)
        self.register_label = Label(self.home_frame, text="Register Student", font=(style.main_font, 30),
                                    fg=style.orange).place(x=50, y=200)
        self.reports_label = Label(self.home_frame, text="Reports", font=(style.main_font, 30),
                                   fg=style.orange).place(x=50, y=350)

        # button that leads to the course frame when clicked
        self.course_button = Button(self.home_frame, text='Course', font=(style.main_font, 30), bg=style.cyan_blue,
                                    fg=style.gray, command=lambda: self.__go_to_frame(self.course_frame))
        self.course_button.place(x=410, y=50)

        # button that leads to the schedule frame when clicked
        self.schedule_button = Button(self.home_frame, text='Schedule', font=(style.main_font, 30), bg=style.cyan_blue,
                                      fg=style.gray, command=lambda: self.__go_to_frame(self.schedule_frame))
        self.schedule_button.place(x=720, y=50)

        # button that leads to the student frame when clicked
        self.student_button = Button(self.home_frame, text='Student', font=(style.main_font, 30), bg=style.cyan_blue,
                                     fg=style.gray, command=lambda: self.__go_to_frame(self.student_frame))
        self.student_button.place(x=1050, y=50)

        # button that leads to the register frame when clicked
        self.register_button = Button(self.home_frame, text='Register', font=(style.main_font, 30),
                                      bg=style.cyan_blue,
                                      fg=style.gray, width=8, command=lambda: self.__go_to_frame(self.register_frame))
        self.register_button.place(x=400, y=200)

        # button that leads to the term frame when clicked
        self.term_button = Button(self.home_frame, text='Terms', font=(style.main_font, 30), bg=style.cyan_blue,
                                  fg=style.gray, command=lambda: self.__go_to_frame(self.term_frame))
        self.term_button.place(x=425, y=350)

        # button that leads to the report frame when clicked
        self.report_button = Button(self.home_frame, text='Generate', font=(style.main_font, 30), bg=style.cyan_blue,
                                    fg=style.gray, command=lambda: self.__go_to_frame(self.report_frame), width=10)
        self.report_button.place(x=710, y=350)

        # placing the home frame
        self.__go_to_frame(self.home_frame)

        # disabling the back button
        self.back_button.config(state='disabled', bg=style.dark_blue)

    # function to bring up previous frame user was on
    def __go_back(self):
        # ensuring that the stack doesnt underflow
        if len(self.back_stack) == 2:
            self.back_button.config(state='disabled', bg=style.dark_blue)
        # removing the last element from the stack
        self.back_stack.pop()
        # bringing up the new last element, i.e., the previous frame
        self.back_stack[-1].tkraise()

    # function to add current frame to the stack
    def __go_to_frame(self, frame):
        frame.place(x=50, y=250)
        # bringing the new frame to the top so that users can access this screen
        frame.tkraise()
        # adding frame to the stack
        self.back_stack.append(frame)
        # enabling the back button so that users can access the previous frame
        self.back_button.config(state='normal', bg=style.cyan_blue)
