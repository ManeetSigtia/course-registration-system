from tkinter import Tk, Label, Button, Entry, Scrollbar, Text, Listbox, Frame, Y, NO, W, RIGHT
from tkinter import ttk

import style


class Widgets:
    # function to make a verification window
    def make_confirm_window(self, title, text, command):
        self.validation_window = Tk()
        self.validation_window.title(title)
        self.validation_window.geometry('600x130+480+390')   # centered screen
        Label(self.validation_window, text=text, font=(style.main_font, 20)).place(x=55, y=10)
        self.yes_button = self.make_button(self.validation_window, text="OK", width=7, font=(style.main_font, 15),
                                           command=lambda: [command(), self.validation_window.destroy()], state='normal',
                                           x=200, y=70)
        self.no_button = self.make_button(self.validation_window, text="Cancel", width=7, font=(style.main_font, 15),
                                          command=self.validation_window.destroy, state='normal', x=300, y=70)

    # function to make a notification window that displays a message to the user
    def make_notification_window(self, title, text, x=100):
        self.incorrect_data_window = Tk()
        self.incorrect_data_window.title(title)
        self.incorrect_data_window.geometry('600x130+480+390')  # centered screen
        Label(self.incorrect_data_window, text=text, font=(style.main_font, 20)).place(x=x, y=10)
        self.ok_button = self.make_button(self.incorrect_data_window, text="OK", width=7, font=(style.main_font, 15),
                                          command=self.incorrect_data_window.destroy, state='normal', x=250, y=70)

    # function to make a button widget
    def make_button(self, frame, text, font, width, command, state, x, y):
        self.button = Button(frame, text=text, font=font, width=width, bg=style.cyan_blue, fg=style.gray,
                             command=command, state=state)
        self.button.place(x=x, y=y)
        return self.button

    # function to make a dropdown menu
    def make_dropdown(self, frame, values, font, initial, x, y, width):
        self.dropdown = ttk.Combobox(frame, state="readonly", value=values, font=font, width=width)
        self.dropdown.current(0)
        self.dropdown.set(initial)
        self.dropdown.bind("<<ComboboxSelected>>")
        self.dropdown.place(x=x, y=y)
        return self.dropdown

    # function to make an entry field
    def make_entrybox(self, frame, font, x, y, width, borderwidth=5, textvariable=None, show=''):
        self.entrybox = Entry(frame, font=font, borderwidth=borderwidth, width=width, textvariable=textvariable, show=show)
        self.entrybox.place(x=x, y=y)
        return self.entrybox

    # function to make a larger entry field
    def make_textbox(self, frame, font, height, width, borderwidth, x, y):
        self.textbox = Text(frame, font=font, height=height, width=width, borderwidth=borderwidth)
        self.textbox.place(x=x, y=y)
        return self.textbox

    # function to make a listbox from which a particular row can be selected
    def make_listbox(self, frame, font, height, width, borderwidth, x, y):
        self.listbox = Listbox(frame, font=font, height=height, width=width, borderwidth=borderwidth)
        self.listbox.place(x=x, y=y)
        return self.listbox

    # function to make a table for better representation of data
    def make_table(self, root, x, y, breadth, values, height=5):
        self.table_columns = values
        self.table_frame = Frame(root)

        self.scrollbar = Scrollbar(self.table_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.table = ttk.Treeview(self.table_frame, yscrollcommand=self.scrollbar.set, height=height)
        self.table.pack()

        self.scrollbar.config(command=self.table.yview)

        for i in range(len(self.table_columns) - 1):
            self.column = tuple(self.table['columns']) + (f'#{i}',)
            self.table.configure(columns=self.column)

        for i in range(len(self.table_columns)):
            if i == 0:
                self.table.heading(column=f'#{i}', text='', anchor='w')
                self.table.column(column=f'#{i}', width=0, stretch=NO, anchor=W)
            else:
                self.table.heading(column=f'#{i}', text=self.table_columns[i], anchor='w')
                self.table.column(column=f'#{i}', width=breadth[i], stretch=False, anchor=W)

        self.table_frame.place(x=x, y=y)
        return self.table

    # function to introduce striped rows in tables for aesthetics
    def striped_rows(self, table):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Treeview', background=style.gray, foreground=style.cyan_blue, fieldbackground=style.gray,
                             borderwidth=5, rowheight=25, font=(style.main_font, 13), height=10)
        self.style.configure("Treeview.Heading", background=style.dark_blue, foreground=style.gray,
                             font=(style.main_font, 10), borderwidth=5)
        self.style.map('Treeview', background=[('selected', 'gray')])
        table.tag_configure('even', background=style.gray)
        table.tag_configure('odd', background=style.light_blue)
