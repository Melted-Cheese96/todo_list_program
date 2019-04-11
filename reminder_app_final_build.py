import tkinter as tk
import threading
import os
import pickle
from tkinter import messagebox
from passlib.hash import pbkdf2_sha256
import shutil


# TODO List as of 11/4/19:
# Revamp the log in menu to display all available user accounts. - Done
# Add a back button to the reminder creation menu. - Done(technically, user just has to click X instead
# Add the ability to see current reminders. - Done
# Refactor code and fit the front end function such as GUI windows' and put them together with their backend
# counterparts. - Essentially Done
# Bug Testing - Done(most bugs have been fixed as of writing)
# Implement settings and management options for admin user. - Not Done
# Implement the backend features for the reminder options window, let the user edit their reminders, delete and whatnot.
# - User has the ability to view their reminders and delete but not edit, still working on letting the user edit
#their created reminders.
# Work on allowing the user to edit reminders that have been created.

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
                                            command=lambda: self.make_account_window(account_options_menu))
        make_new_account_button.grid(row=0, sticky='N' + 'S' + 'E' + 'W')
        #sign_in_button = tk.Button(account_options_menu, text='Sign In',
         #                          command=lambda: self.log_in_window(account_options_menu))
        sign_in_button = tk.Button(account_options_menu, text='Sign In',
                                   command=lambda:self.user_selection_window(account_options_menu))
        sign_in_button.grid(row=1, sticky='N' + 'S' + 'E' + 'W')
        admin_options = tk.Button(account_options_menu, text='Admin Settings',
                                  command=lambda: self.check_for_admin_acc(account_options_menu))
        admin_options.grid(row=2, sticky='N' + 'S' + 'E' + 'W')
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
        new_admin_acc_win.protocol('WM_DELETE_WIN', lambda: self.back(new_admin_acc_win, parent_win))
        admin_password_label = tk.Label(new_admin_acc_win, text='Admin Password:')
        admin_password_label.grid(row=0)
        admin_password_entry = tk.Entry(new_admin_acc_win)
        admin_password_entry.grid(row=0, column=1)
        admin_password_entry.configure(show='*')
        state_variable = tk.IntVar()
        show_password_check_box = tk.Checkbutton(new_admin_acc_win, text='Show Password',
                                                 command=lambda: self.get_var_state(state_variable,
                                                                                    admin_password_entry))
        show_password_check_box.grid(row=1)
        setup_admin_acc_button = tk.Button(new_admin_acc_win, text='Setup Admin Account',
                                           command=lambda: self.set_admin_acc_password(admin_password_entry))
        setup_admin_acc_button.grid(row=1, column=1)
        back_button = tk.Button(new_admin_acc_win, text='Back',
                                command=lambda: self.back(new_admin_acc_win, parent_win))
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
        make_acc_win.protocol('WM_DELETE_WINDOW', lambda: self.back(make_acc_win, parent_window))
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
                                                   command=lambda: self.get_var_state(state_var, password_entry))
        show_password_checkbutton.grid(row=2, column=0)
        make_account_button = tk.Button(make_acc_win, text='Create Account',
                                        command=lambda: self.make_account(username_entry, password_entry))
        make_account_button.grid(row=2, column=1)
        back_button = tk.Button(make_acc_win, text='Back', command=lambda: self.back(make_acc_win, parent_window))
        back_button.grid(row=3)

    def make_account(self, username_var, password_var):
        # This function is responsible for creating an account
        password_string = password_var.get()
        username_string = username_var.get()
        if len(username_string) < 4 or len(password_string) < 4 or '.' in username_string:
            messagebox.showerror('Error!',
                                 'Your username and password have to be above 4 characters and cannot contain dots')
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

    def user_selection_window(self, previous_window):
        previous_window.withdraw()
        user_selection_win = tk.Toplevel()
        user_selection_win.title('Select User')
        user_selection_win.resizable(width=False, height=False)
        user_selection_win.protocol('WM_DELETE_WINDOW', lambda:self.back(user_selection_win, previous_window))
        instructions_label = tk.Label(user_selection_win, text='Select User!')
        instructions_label.grid(row=0)
        self.display_all_users(user_selection_win, previous_window)

    def log_in_window(self, username_chosen, user_selection_window_obj, account_options_win):
        user_selection_window_obj.withdraw()
        log_in_win = tk.Toplevel()
        log_in_win.resizable(width=False, height=False)
        log_in_win.title('Log In')
        log_in_win.protocol('WM_DELETE_WINDOW', lambda:self.back(log_in_win, user_selection_window_obj))
        password_label = tk.Label(log_in_win, text='Password:')
        password_label.grid(row=0)
        password_entry = tk.Entry(log_in_win)
        password_entry.grid(row=0, column=1)
        password_entry.configure(show='*')
        checkbutton_state_var = tk.IntVar()
        show_password_checkbutton = tk.Checkbutton(log_in_win, variable=checkbutton_state_var, text='Show Password',
                                                   command=lambda:self.get_var_state(checkbutton_state_var,
                                                                                     password_entry))
        show_password_checkbutton.grid(row=1)
        log_in_button = tk.Button(log_in_win, text='Log In', command=lambda:self.log_in(username_chosen, password_entry,
                                                                                        log_in_win, user_selection_window_obj,
                                                                                        account_options_win))
        log_in_button.grid(row=1, column=1)
        back_button = tk.Button(log_in_win, text='Back', command=lambda:self.back(log_in_win, user_selection_window_obj))
        back_button.grid(row=2)

    def display_all_users(self, window_to_draw_onto, account_options_window):
        os.chdir('.users')
        row_count = 0
        for user in os.listdir():
            row_count += 1
            tk.Button(window_to_draw_onto, text=user,
                      command=lambda user_name=user:self.log_in_window(user_name,
                                                                       window_to_draw_onto, account_options_window
                                                                       )).grid(row=row_count)
        os.chdir(self.starting_dir)

    def log_in(self, username_string, password_var, log_in_win, selection_win, account_options_win):
        password_string = password_var.get()
        if len(username_string) < 4 or len(password_string) < 4 or ' ' in username_string:
            messagebox.showerror('Error!',
                                 'Your username and password have to be above 4 characters and cannot contain dots')
        else:
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
                    self.reminders_window(log_in_win, selection_win, account_options_win)
                else:
                    messagebox.showerror('Invalid Password!', 'Your password was invalid!')
                    os.chdir(self.starting_dir)
                    password_var.delete(0, 'end')
            else:
                messagebox.showerror('Account Not Found', 'That Account Was Not Found')
                os.chdir(self.starting_dir)
                password_var.delete(0, 'end')

    def reminders_window(self, log_in_window, user_selection_win, account_options_win):
        log_in_window.destroy()
        user_selection_win.destroy()
        account_options_win.destroy()
        print(self.user_signed_in)
        reminder_options_window = tk.Toplevel()
        for x in range(3):
            reminder_options_window.rowconfigure(x, weight=1)
        for y in range(3):
            reminder_options_window.columnconfigure(0, weight=1)
        reminder_options_window.title('Reminder Options')
        # reminder_options_window.resizable(width=False, height=False)
        reminder_options_window.protocol('WM_DELETE_WINDOW', lambda: self.sign_out_of_account(reminder_options_window))
        new_reminder_button = tk.Button(reminder_options_window, text='Create New Reminder',
                                        command=lambda: self.create_new_reminder_window(reminder_options_window))
        new_reminder_button.grid(row=0, sticky='N' + 'S' + 'E' + 'W')
        check_reminders_button = tk.Button(reminder_options_window, text='Check Active Reminders',
                                           command=lambda: self.reminder_management_menu(reminder_options_window))
        check_reminders_button.grid(row=1, sticky='N' + 'S' + 'E' + 'W')
        view_finished_reminders_button = tk.Button(reminder_options_window, text='View Completed Reminders',
                                                   command=lambda:self.completed_reminders_window(reminder_options_window))
        view_finished_reminders_button.grid(row=2, sticky='N' + 'S' + 'E' + 'W')
        log_out_button = tk.Button(reminder_options_window, text='Log out of {}'.format(self.user_signed_in),
                                   command=lambda: self.sign_out_of_account(reminder_options_window))
        log_out_button.grid(row=3, sticky='N' + 'S' + 'E' + 'W')

    def sign_out_of_account(self, options_menu):
        self.user_signed_in = ''
        options_menu.destroy()
        self.account_options_window()

    def reminder_management_menu(self, previous_window):
        previous_window.withdraw()
        # This menu displays all the active reminders in the user's folder.
        reminder_management_window = tk.Toplevel()
        reminder_management_window.resizable(width=False, height=False)
        reminder_management_window.protocol('WM_DELETE_WINDOW',
                                            lambda: self.back(reminder_management_window, previous_window))
        menu_label = tk.Label(reminder_management_window, text='Click on a reminder for options!')
        menu_label.grid(row=0)
        back_button = tk.Button(reminder_management_window, text='Back',
                                command=lambda:self.back(reminder_management_window, previous_window))
        back_button.grid(row=1)
        buffer_label = tk.Label(reminder_management_window, text='--------------------------------')
        buffer_label.grid(row=2)
        self.display_reminders(reminder_management_window, previous_window)

    def display_reminders(self, window_to_display_on, main_window):
        # This function is responsible for displaying all active reminders in the user's folder to the menu in the function above.
        row_count = 2
        os.chdir('.users')
        os.chdir(self.user_signed_in)
        os.chdir('.reminders')
        reminder_list = []
        for item in os.listdir():
            reminder_list.append(item)
        if len(reminder_list) == 0:
            messagebox.showerror('No Reminders!', 'You have no reminders!')
            os.chdir(self.starting_dir)
            window_to_display_on.destroy()
            main_window.deiconify()
        else:
            for reminder in reminder_list:
                row_count += 1
                tk.Button(window_to_display_on, text=reminder,
                          command=lambda reminder_name=reminder: self.reminder_settings_window(reminder_name,
                                                                                               window_to_display_on,
                                                                                               main_window)).grid(
                    row=row_count)
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
        reminder_options.protocol('WM_DELETE_WINDOW', lambda: self.back(reminder_options, previous_window))
        reminder_options.title(reminder_name)
        view_reminder_button = tk.Button(reminder_options, text='View "{}"'.format(reminder_name),
                                         command=lambda: self.view_reminder(reminder_options, reminder_name,
                                                                            main_window))
        view_reminder_button.grid(row=0, sticky='N' + 'S' + 'E' + 'W')
        edit_reminder_button = tk.Button(reminder_options, text='Edit "{}"'.format(reminder_name),
                                         command=lambda:self.edit_reminder(reminder_name, reminder_options)) # Work on this.
        edit_reminder_button.grid(row=1, sticky='N' + 'S' + 'E' + 'W')
        delete_reminder_button = tk.Button(reminder_options, text='Delete "{}"'.format(reminder_name),
                                           command=lambda: self.remove_reminder_from_folder(reminder_name,
                                                                                            reminder_options,
                                                                                            main_window,
                                                                                            previous_window))
        delete_reminder_button.grid(row=2, sticky='N' + 'S' + 'E' + 'W')

    def completed_reminders_window(self, reminder_management_window):
        reminder_management_window.withdraw()
        completed_reminders_display = tk.Toplevel()
        completed_reminders_display.title('Completed Reminders')
        completed_reminders_display.resizable(width=False, height=False)
        display_label = tk.Label(completed_reminders_display, text='Click on a reminder for options!:')
        display_label.grid(row=0)
        self.display_completed_reminders(completed_reminders_display, reminder_management_window)

    def display_completed_reminders(self, window_to_draw_to, reminder_management_win):
        row_count = 1
        os.chdir('.users')
        os.chdir(self.user_signed_in)
        os.chdir('.completed')
        reminders = os.listdir()
        if len(reminders) <= 0:
            messagebox.showerror('No completed reminders!', 'You have no completed reminders!')
            os.chdir(self.starting_dir)
            window_to_draw_to.destroy()
            reminder_management_win.deiconify()
        else:
            for single_reminder in reminders:
                tk.Button(window_to_draw_to, text=single_reminder,
                          command=lambda name=single_reminder:self.completed_reminder_options(name,
                                                                                              window_to_draw_to,
                                                                                              reminder_management_win)).grid(row=row_count)
                row_count += 1
            os.chdir(self.starting_dir)

    def completed_reminder_options(self, reminder_name, completed_reminder_window_list, reminder_management_win):
        completed_reminder_window_list.withdraw()
        reminder_options_win = tk.Toplevel()
        reminder_options_win.title('Completed Reminder Options')
        for x in range(4):
            reminder_options_win.rowconfigure(x, weight=1)
        for y in range(4):
            reminder_options_win.columnconfigure(0, weight=1)
        # mark_reminder_as_undone_button = tk.Button(reminder_options_win, text='Mark as undone')
        # mark_reminder_as_undone_button.grid(row=0, sticky='N'+'S'+'E'+'W')
        delete_reminder_button = tk.Button(reminder_options_win, text='Delete',
                                           command=lambda:self.delete_completed_reminder(reminder_name,
                                                                                         completed_reminder_window_list,
                                                                                         reminder_management_win,
                                                                                         reminder_options_win))
        delete_reminder_button.grid(row=1, sticky='N'+'S'+'E'+'W')

    def delete_completed_reminder(self, reminder_name, completed_reminder_win, reminder_management_window, reminder_settings_win):
        # This function deletes a reminder that has been marked as completed
        os.chdir('.users')
        os.chdir(self.user_signed_in)
        os.chdir('.completed')
        os.remove(reminder_name)
        os.chdir(self.starting_dir)
        messagebox.showinfo('Reminder has been deleted!', 'Your reminder has been deleted')
        completed_reminder_win.destroy()
        reminder_settings_win.destroy()
        self.completed_reminders_window(reminder_management_window)

    def edit_reminder(self, reminder_name, reminder_settings_win):
        reminder_desc = self.get_reminder_description(reminder_name)
        reminder_settings_win.withdraw()
        edit_reminder_window = tk.Toplevel()
        edit_reminder_window.title('Edit Reminder')
        edit_reminder_window.protocol('WM_DELETE_WINDOW', lambda:self.back(edit_reminder_window, reminder_settings_win))
        edit_reminder_window.resizable(width=False, height=False)
        reminder_title_label = tk.Label(edit_reminder_window, text='Title: {}'.format(reminder_name))
        reminder_title_label.grid(row=0)
        reminder_description = tk.Text(edit_reminder_window, height=10, width=30)
        reminder_description.grid(row=1)
        reminder_description.insert('end', reminder_desc)
        save_changes_button = tk.Button(edit_reminder_window, text='Save Changes',
                                        command=lambda:self.save_new_changes_to_reminder(reminder_name,
                                                                                  reminder_description.get(1.0, 'end')))
        save_changes_button.grid(row=2)
        back_button = tk.Button(edit_reminder_window, text='Back',
                                command=lambda:self.back(edit_reminder_window, reminder_settings_win))
        back_button.grid(row=3)
        # Continue this function!

    def save_new_changes_to_reminder(self, reminder_name, new_changes):
        print(new_changes)
        save_verification = messagebox.askyesno('Save changes?', 'Are you sure that you want to save these new changes?')
        if save_verification is True:
            os.chdir('.users')
            os.chdir(self.user_signed_in)
            os.chdir('.reminders')
            with open(reminder_name, 'wb') as doc:
                pickle.dump(new_changes, doc)
            os.chdir(self.starting_dir)
            messagebox.showinfo('Saved!', 'Your changes to "{}" have been saved!'.format(reminder_name))
        else:
            pass

    def mark_reminder_as_done(self, reminder_name, view_reminder_win, reminder_list_win, main_window):
        os.chdir('.users')
        os.chdir(self.user_signed_in)
        user_directory = os.getcwd()
        os.chdir('.completed')
        completed_reminders_dir = os.getcwd()
        os.chdir(user_directory)
        os.chdir('.reminders')
        shutil.copy(reminder_name, completed_reminders_dir)
        os.remove(reminder_name)
        os.chdir(self.starting_dir)
        messagebox.showinfo('Reminder Marked As Done!', 'Your reminder has been marked as done!')
        view_reminder_win.destroy()
        reminder_list_win.destroy()
        self.reminder_management_menu(main_window)

    def view_reminder(self, previous_window, reminder_name, main_window):
        previous_window.withdraw()
        reminder_desc = self.get_reminder_description(reminder_name)
        description_view_window = tk.Toplevel()
        description_view_window.title(reminder_name)
        description_view_window.protocol('WM_DELETE_WINDOW',
                                         lambda: self.back(description_view_window, previous_window))
        description_view_window.resizable(width=False, height=False)
        reminder_name_label = tk.Label(description_view_window, text='Reminder Name: {}'.format(reminder_name))
        reminder_name_label.grid(row=0)
        reminder_description_label = tk.Label(description_view_window, text='Description:')
        reminder_description_label.grid(row=1)
        reminder_description = tk.Text(description_view_window, height=10, width=30)
        reminder_description.grid(row=2)
        reminder_description.insert('end', reminder_desc)
        reminder_description.configure(state='disabled')
        mark_reminder_as_done_button = tk.Button(description_view_window, text='Mark As Done',
                                                 command=lambda:self.mark_reminder_as_done(reminder_name,
                                                                                           description_view_window,
                                                                                           previous_window,
                                                                                           main_window))
        mark_reminder_as_done_button.grid(row=3)
        back_button = tk.Button(description_view_window, text='Back', command=lambda:self.back(description_view_window,
                                                                                               previous_window))
        back_button.grid(row=4)
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
        delete_verification = messagebox.askyesno('Confirm',
                                                  'Are you sure you want to delete "{}"'.format(reminder_name))
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
        new_reminder_win.protocol('WM_DELETE_WINDOW', lambda: self.back(new_reminder_win, reminder_win))
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
                                           command=lambda: self.create_new_reminder(reminder_entry,
                                                                                    reminder_description_text_box))
        create_reminder_button.grid(row=3, column=1)
        back_button = tk.Button(new_reminder_win, text='Back',
                                command=lambda: self.back(new_reminder_win, reminder_win))
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
