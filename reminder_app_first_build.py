import tkinter as tk
import threading
import os
import pickle
from tkinter import messagebox
from passlib.hash import pbkdf2_sha256


#TODO List as of 8/4/19:
# Revamp the log in menu to display all available user accounts.
# Add a back button to the reminder creation menu.
# Add the ability to see current reminders.
# Refactor code and fit the front end function such as GUI windows' and put them together with their backend counterparts.
# Bug Testing
# Implement settings and management options for admin user.

class ReminderApp:
    def __init__(self):
        self.starting_dir = os.getcwd()
        self.user_signed_in = ''
        self.root_window = tk.Tk()
        self.root_window.withdraw()
        # self.root_window.mainloop()
        self.setup()
        self.account_options_window()

    def back(self, window_to_close, window_to_reopen):
        window_to_close.destroy()
        window_to_reopen.deiconify()

    def account_options_window(self):
        account_options_menu = tk.Toplevel()
        account_options_menu.title('Account Options')
        account_options_menu.resizable(width=False, height=False)
        make_new_account_button = tk.Button(account_options_menu, text='Create Account',
                                            command=lambda:self.make_account_window(account_options_menu))
        make_new_account_button.grid(row=0)
        sign_in_button = tk.Button(account_options_menu, text='Sign In',
                                   command=lambda:self.log_in_window(account_options_menu))
        sign_in_button.grid(row=1)
        admin_options = tk.Button(account_options_menu, text='Admin Settings',
                                  command=lambda:self.check_for_admin_acc(account_options_menu))
        admin_options.grid(row=2)
        account_options_menu.mainloop()

    def check_for_admin_acc(self, parent_win):
        os.chdir('.users')
        if '.admin' in os.listdir():
            self.admin_options_window(parent_win)
        else:
            os.chdir(self.starting_dir)
            self.make_admin_account_window(parent_win)

    def admin_options_window(self, parent_win):
        # Work on admin menu
        pass

    def make_admin_account_window(self, parent_win):
        parent_win.withdraw()
        new_admin_acc_win = tk.Toplevel()
        new_admin_acc_win.resizable(width=False, height=False)
        new_admin_acc_win.title('Admin Account Setup')
        new_admin_acc_win.protocol('WM_DELETE_WIN', lambda:self.back(new_admin_acc_win, parent_win))
        admin_password_label = tk.Label(new_admin_acc_win, text='Admin Password:')
        admin_password_label.grid(row=0)
        admin_password_entry = tk.Entry(new_admin_acc_win)
        admin_password_entry.grid(row=0, column=1)
        admin_password_entry.configure(show='*')
        state_variable = tk.IntVar()
        show_password_check_box = tk.Checkbutton(new_admin_acc_win, text='Show Password',
                                                 command=lambda:self.get_var_state(state_variable,
                                                                                   admin_password_entry))
        show_password_check_box.grid(row=1)
        setup_admin_acc_button = tk.Button(new_admin_acc_win, text='Setup Admin Account',
                                           command=lambda:self.set_admin_acc_password(admin_password_entry))
        setup_admin_acc_button.grid(row=1, column=1)
        back_button = tk.Button(new_admin_acc_win, text='Back',
                                command=lambda:self.back(new_admin_acc_win, parent_win))
        back_button.grid(row=2)

    def set_admin_acc_password(self, admin_password_var):
        os.chdir('.users')
        os.mkdir('.admin')
        admin_password_string = admin_password_var.get()
        if len(admin_password_string) < 4:
            messagebox.showerror('Error', 'Your password cannot be less than 4 letters!')
        else:
            os.chdir('.admin')
            hashed_password = pbkdf2_sha256.hash(admin_password_string)
            with open('info', 'wb') as doc:
                pickle.dump(hashed_password, doc)
            messagebox.showinfo('Admin Account Made!', 'Your Admin Account Has Been Created!')
            os.chdir(self.starting_dir)
            admin_password_var.delete(0, 'end')

    def make_account_window(self, parent_window):
        parent_window.withdraw()
        make_acc_win = tk.Toplevel()
        make_acc_win.title('New Account')
        make_acc_win.protocol('WM_DELETE_WINDOW', lambda:self.back(make_acc_win, parent_window))
        make_acc_win.resizable(width=False, height=False)
        username_label = tk.Label(make_acc_win, text='Username:')
        username_label.grid(row=0)
        username_entry = tk.Entry(make_acc_win)
        username_entry.grid(row=0, column=1)
        password_label = tk.Label(make_acc_win, text='Password:')
        password_label.grid(row=1)
        password_entry = tk.Entry(make_acc_win)
        password_entry.grid(row=1, column=1)
        password_entry.configure(show='*')
        state_var = tk.IntVar()
        show_password_checkbutton = tk.Checkbutton(make_acc_win, variable=state_var, text='Show Password',
                                                   command=lambda:self.get_var_state(state_var, password_entry))
        show_password_checkbutton.grid(row=2, column=0)
        make_account_button = tk.Button(make_acc_win, text='Create Account',
                                        command=lambda:self.make_account(username_entry, password_entry))
        make_account_button.grid(row=2, column=1)
        back_button = tk.Button(make_acc_win, text='Back', command=lambda:self.back(make_acc_win, parent_window))
        back_button.grid(row=3)

    def get_var_state(self, state_variable, password_entry):
        if state_variable.get() == 0:
            password_entry.configure(show='*')
        else:
            password_entry.configure(show='')

    def make_account(self, username_var, password_var):
        # This function is responsible for creating an account
        password_string = password_var.get()
        username_string = username_var.get()
        if len(username_string) < 4 or len(password_string) < 4 or '.' in username_string:
            messagebox.showerror('Error!', 'Your username and password have to be above 4 characters and cannot contain dots')
            username_var.delete(0, 'end')
            password_var.delete(0, 'end')
        else:
            username_string = '.' + username_var.get()
            os.chdir('.users')
            if username_string in os.listdir():
                messagebox.showerror('Username Already In Use!', 'That username is already being used!')
                username_var.delete(0, 'end')
                password_var.delete(0, 'end')
            else:
                os.mkdir(username_string)
                os.chdir(username_string)
                os.mkdir('.reminders')
                password_hash = pbkdf2_sha256.hash(password_string)
                with open('info', 'wb') as doc:
                    pickle.dump(password_hash, doc)
                os.chdir(self.starting_dir)
                messagebox.showinfo('Account Created!', 'Your account has been created!')
                username_var.delete(0, 'end')
                password_var.delete(0, 'end')

    def log_in_window(self, parent_window):
        parent_window.withdraw()
        log_in_win = tk.Toplevel()
        log_in_win.resizable(width=False, height=False)
        log_in_win.protocol('WM_DELETE_WINDOW', lambda:self.back(log_in_win, parent_window))
        log_in_win.title('Log In')
        username_label = tk.Label(log_in_win, text='Username:')
        username_label.grid(row=0)
        username_entry = tk.Entry(log_in_win)
        username_entry.grid(row=0, column=1)
        password_label = tk.Label(log_in_win, text='Password:')
        password_label.grid(row=1)
        password_entry = tk.Entry(log_in_win)
        password_entry.grid(row=1, column=1)
        password_entry.configure(show='*')
        state_variable = tk.IntVar()
        show_password_checkbox = tk.Checkbutton(log_in_win, variable=state_variable, text='Show Password',
                                                command=lambda:self.get_var_state(state_variable, password_entry))
        show_password_checkbox.grid(row=2, column=0)
        log_in_button = tk.Button(log_in_win, text='Log In',
                                  command=lambda:self.log_in(username_entry, password_entry, log_in_win,
                                                             parent_window))
        log_in_button.grid(row=2, column=1)
        back_button = tk.Button(log_in_win, text='Back', command=lambda:self.back(log_in_win, parent_window))
        back_button.grid(row=3)

    def reminders_window(self, log_in_window, parent_window):
        log_in_window.destroy()
        parent_window.destroy()
        print(self.user_signed_in)
        reminder_options_window = tk.Toplevel()
        reminder_options_window.title('Reminder Options')
        reminder_options_window.resizable(width=False, height=False)
        new_reminder_button = tk.Button(reminder_options_window, text='Create New Reminder',
                                        command=lambda:self.create_new_reminder_window(reminder_options_window))
        new_reminder_button.grid(row=0)
        check_reminders_button = tk.Button(reminder_options_window, text='Check Active Reminders')
        check_reminders_button.grid(row=1)

    def create_new_reminder_window(self, reminder_win):
        reminder_win.withdraw()
        new_reminder_win = tk.Toplevel()
        new_reminder_win.protocol('WM_DELETE_WINDOW', lambda:self.back(new_reminder_win, reminder_win))
        new_reminder_win.title('New Reminder')
        new_reminder_win.resizable(width=False, height=False)
        reminder_name_label = tk.Label(new_reminder_win, text='Reminder Name:')
        reminder_name_label.grid(row=0)
        reminder_entry = tk.Entry(new_reminder_win)
        reminder_entry.grid(row=0, column=1)
        reminder_description_label = tk.Label(new_reminder_win, text='Description:')
        reminder_description_label.grid(row=1)
        reminder_description_text_box = tk.Text(new_reminder_win, heigh=10, width=30)
        reminder_description_text_box.grid(row=2, column=1)
        create_reminder_button = tk.Button(new_reminder_win, text='Create Reminder',
                                           command=lambda:self.create_new_reminder(reminder_entry,
                                                                                   reminder_description_text_box))
        create_reminder_button.grid(row=3, column=1)

    def create_new_reminder(self, reminder_title_var, reminder_desc_var):
        reminder_title_string = reminder_title_var.get()
        reminder_desc_string = reminder_desc_var.get('1.0', 'end')
        if len(reminder_title_string) <= 1 or len(reminder_desc_string) <= 1:
            messagebox.showerror('Length Error', 'You need more than one character!')
        else:
            os.chdir('.users')
            os.chdir(self.user_signed_in)
            os.chdir('.reminders')
            with open(reminder_title_string, 'wb') as doc:
                pickle.dump(reminder_desc_string, doc)
            messagebox.showinfo('Reminder has been created!', 'Your reminder has been created!')
            os.chdir(self.starting_dir)
            reminder_title_var.delete(0, 'end')
            reminder_desc_var.delete(1.0, 'end')

    def log_in(self, username_var, password_var, log_in_win, parent_window):
        username_string = username_var.get()
        password_string = password_var.get()
        if len(username_string) < 4 or len(password_string) < 4 or '.' in username_string or ' ' in username_string:
            messagebox.showerror('Error!', 'Your username and password have to be above 4 characters and cannot contain dots')
        else:
            username_string = '.' + username_var.get()
            os.chdir('.users')
            if username_string in os.listdir():
                os.chdir(username_string)
                with open('info', 'rb') as doc:
                    hashed_password = pickle.load(doc)
                verification = pbkdf2_sha256.verify(password_string, hashed_password)
                if verification is True:
                    print('Correct Password!')
                    self.user_signed_in = username_string
                    os.chdir(self.starting_dir)
                    self.reminders_window(log_in_win, parent_window)
                else:
                    messagebox.showerror('Invalid Password!', 'Your password was invalid!')
                    os.chdir(self.starting_dir)
                    password_var.delete(0, 'end')
            else:
                messagebox.showerror('Account Not Found', 'That Account Was Not Found')
                os.chdir(self.starting_dir)
                username_var.delete(0, 'end')
                password_var.delete(0, 'end')

    def setup(self):
        # This function checks if the necessary things are there for the program to run.
        if '.users' in os.listdir():
            pass
        else:
            os.mkdir('.users')


instance_1 = ReminderApp()