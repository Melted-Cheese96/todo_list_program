import tkinter as tk
import threading
import os
import pickle
from tkinter import messagebox
from passlib.hash import pbkdf2_sha256
import view_reminder_script as view

#TODO List as of 8/4/19:
# Revamp the log in menu to display all available user accounts. - Not Done
# Add a back button to the reminder creation menu. - Done(technically, user just has to click X instead
# Add the ability to see current reminders. - Done
# Refactor code and fit the front end function such as GUI windows' and put them together with their backend
# counterparts. - Essentially Done
# Bug Testing - Done(most bugs have been fixed as of writing)
# Implement settings and management options for admin user. - Not Done
# Implement the backend features for the reminder options window, let the user edit their reminders, delete and whatnot.
# - Not Done(frontend has been done but not backend)

class ReminderApp:
    def __init__(self):
        self.starting_dir = os.getcwd()
        self.user_signed_in = ''
        self.root_window = tk.Tk()
        self.root_window.withdraw()
        # self.root_window.mainloop()
        self.setup()
        self.account_options_window()

    def setup(self):
        # This function checks if the necessary things are there for the program to run.
        if '.users' in os.listdir():
            pass
        else:
            os.mkdir('.users')

    def get_var_state(self, state_variable, password_entry):
        if state_variable.get() == 0:
            password_entry.configure(show='*')
        else:
            password_entry.configure(show='')

    def back(self, window_to_close, window_to_reopen):
        window_to_close.destroy()
        window_to_reopen.deiconify()

    def account_options_window(self):
        account_options_menu = tk.Toplevel()
        for x in range(3):
            account_options_menu.rowconfigure(x, weight=1)
        for y in range(3):
            account_options_menu.columnconfigure(0, weight=1)
        account_options_menu.title('Account Options')
        # account_options_menu.resizable(width=False, height=False)
        make_new_account_button = tk.Button(account_options_menu, text='Create Account',
                                            command=lambda:self.make_account_window(account_options_menu))
        make_new_account_button.grid(row=0, sticky='N'+'S'+'E'+'W')
        sign_in_button = tk.Button(account_options_menu, text='Sign In',
                                   command=lambda:self.log_in_window(account_options_menu))
        sign_in_button.grid(row=1, sticky='N'+'S'+'E'+'W')
        admin_options = tk.Button(account_options_menu, text='Admin Settings',
                                  command=lambda:self.check_for_admin_acc(account_options_menu))
        admin_options.grid(row=2, sticky='N'+'S'+'E'+'W')
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
                os.mkdir('.completed')
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

    def reminders_window(self, log_in_window, parent_window):
        log_in_window.destroy()
        parent_window.destroy()
        print(self.user_signed_in)
        reminder_options_window = tk.Toplevel()
        for x in range(3):
            reminder_options_window.rowconfigure(x, weight=1)
        for y in range(3):
            reminder_options_window.columnconfigure(0, weight=1)
        reminder_options_window.title('Reminder Options')
        # reminder_options_window.resizable(width=False, height=False)
        reminder_options_window.protocol('WM_DELETE_WINDOW', lambda:self.sign_out_of_account(reminder_options_window))
        new_reminder_button = tk.Button(reminder_options_window, text='Create New Reminder',
                                        command=lambda:self.create_new_reminder_window(reminder_options_window))
        new_reminder_button.grid(row=0, sticky='N'+'S'+'E'+'W')
        check_reminders_button = tk.Button(reminder_options_window, text='Check Active Reminders',
                                           command=lambda:self.reminder_management_menu(reminder_options_window))
        check_reminders_button.grid(row=1, sticky='N'+'S'+'E'+'W')
        view_finished_reminders_button = tk.Button(reminder_options_window, text='View Completed Reminders')
        view_finished_reminders_button.grid(row=2, sticky='N'+'S'+'E'+'W')
        log_out_button = tk.Button(reminder_options_window, text='Log out of {}'.format(self.user_signed_in),
                                   command=lambda:self.sign_out_of_account(reminder_options_window))
        log_out_button.grid(row=3, sticky='N'+'S'+'E'+'W')

    def sign_out_of_account(self, options_menu):
        self.user_signed_in = ''
        options_menu.destroy()
        self.account_options_window()

    def reminder_management_menu(self, previous_window):
        previous_window.withdraw()
        # This menu displays all the active reminders in the user's folder.
        reminder_management_window = tk.Toplevel()
        reminder_management_window.resizable(width=False, height=False)
        reminder_management_window.protocol('WM_DELETE_WINDOW', lambda: self.back(reminder_management_window, previous_window))
        menu_label = tk.Label(reminder_management_window, text='Click on a reminder for options!')
        menu_label.grid(row=0)
        self.display_reminders(reminder_management_window, previous_window)

    def display_reminders(self, window_to_display_on, main_window):
        # This function is responsible for displaying all active reminders in the user's folder to the menu in the function above.
        row_count = 0
        os.chdir('.users')
        os.chdir(self.user_signed_in)
        os.chdir('.reminders')
        reminder_list = []
        for item in os.listdir():
            reminder_list.append(item)
        if len(reminder_list) == 0:
            messagebox.showerror('No Reminders!', 'You have no reminders!')
            window_to_display_on.destroy()
            main_window.deiconify()
        else:
            for reminder in reminder_list:
                row_count += 1
                tk.Button(window_to_display_on, text=reminder,
                          command=lambda reminder_name=reminder:self.reminder_settings_window(reminder_name,
                                                                  window_to_display_on, main_window)).grid(row=row_count)
            os.chdir(self.starting_dir)

    def reminder_settings_window(self, reminder_name, previous_window, main_window):
        # This menu displays the various options when clicking on a reminder.
        # Previous window is the reminder_management_window
        # Main window is the window that is created in the reminders_window() function
        # The reason for that window to be passed in this function is for when a file is deleted, the window can
        # be refreshed with the updated file list.
        previous_window.withdraw()
        reminder_options = tk.Toplevel()
        for x in range(4):
            reminder_options.rowconfigure(x, weight=1)
        for y in range(4):
            reminder_options.columnconfigure(0, weight=1)
        reminder_options.protocol('WM_DELETE_WINDOW', lambda:self.back(reminder_options, previous_window))
        reminder_options.title(reminder_name)
        view_reminder_button = tk.Button(reminder_options, text='View "{}"'.format(reminder_name),
                                         command=lambda:self.view_reminder(reminder_options, reminder_name))
        view_reminder_button.grid(row=0, sticky='N'+'S'+'E'+'W')
        edit_reminder_button = tk.Button(reminder_options, text='Edit "{}"'.format(reminder_name))
        edit_reminder_button.grid(row=1, sticky='N'+'S'+'E'+'W')
        delete_reminder_button = tk.Button(reminder_options, text='Delete "{}"'.format(reminder_name),
                                           command=lambda:self.remove_reminder_from_folder(reminder_name,
                                                                                           reminder_options,
                                                                                           main_window, previous_window))
        delete_reminder_button.grid(row=2, sticky='N'+'S'+'E'+'W')

    def view_reminder(self, previous_window, reminder_name):
        previous_window.withdraw()
        reminder_desc = self.get_reminder_description(reminder_name)
        description_view_window = tk.Toplevel()
        description_view_window.title(reminder_name)
        description_view_window.protocol('WM_DELETE_WINDOW', lambda:self.back(description_view_window, previous_window))
        description_view_window.resizable(width=False, height=False)
        reminder_name_label = tk.Label(description_view_window, text='Reminder Name: {}'.format(reminder_name))
        reminder_name_label.grid(row=0)
        reminder_description_label = tk.Label(description_view_window, text='Description:')
        reminder_description_label.grid(row=1)
        reminder_description = tk.Text(description_view_window, height=10, width=30)
        reminder_description.grid(row=2)
        reminder_description.insert('end', reminder_desc)
        reminder_description.configure(state='disabled')
        remove_reminder_button = tk.Button(description_view_window, text='Mark As Done')
        # Continue this function!

    def get_reminder_description(self, reminder_name):
        os.chdir('.users')
        os.chdir(self.user_signed_in)
        os.chdir('.reminders')
        with open(reminder_name, 'rb') as doc:
            content = pickle.load(doc)
        os.chdir(self.starting_dir)
        return content

    def remove_reminder_from_folder(self, reminder_name, reminder_management_win, main_window, reminder_list_window):
        # The main window argument is passed into this function so the reminder_management_win can be displayed again
        delete_verification = messagebox.askyesno('Confirm', 'Are you sure you want to delete "{}"'.format(reminder_name))
        if delete_verification is True:
            os.chdir('.users')
            os.chdir(self.user_signed_in)
            os.chdir('.reminders')
            try:
                os.remove(reminder_name)
                os.chdir(self.starting_dir)
                reminder_management_win.destroy()
                reminder_list_window.destroy()
                main_window.deiconify()
                self.reminder_management_menu(main_window)
            except FileNotFoundError:
                messagebox.showerror('File Already Deleted!', 'That file appears to already be deleted!')
                os.chdir(self.starting_dir)
                # reminder_list_win.destroy()
        else:
            pass

    def create_new_reminder_window(self, reminder_win):
        # Allows the user to create a new reminder, the reminder_win parameter should have the reminder_options_window.
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
        back_button = tk.Button(new_reminder_win, text='Back', command=lambda:self.back(new_reminder_win, reminder_win))
        back_button.grid(row=3)

    def create_new_reminder(self, reminder_title_var, reminder_desc_var):
        # Creates the reminder from the information filled in the menu above.
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

instance_1 = ReminderApp()
