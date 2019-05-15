#!/usr/bin/env python3

"""Work Log Database
Author: Ian H Keith
Created: 05/15/2019
"""

from collections import OrderedDict
import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('work_log.db')

class Log(Model):
     employee_name = CharField(max_length=255)
     task_title = CharField(max_length=255)
     date = DateTimeField(default=datetime.datetime.now)
     time_spent = IntegerField(default=0)
     general_notes = TextField(default=None)

     class Meta:
         database = db


def clear_screen():
    """Clears the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def initialize():
    """Create the database and table if they don't already exist"""
    db.connect()
    db.create_tables([Log], safe=True)


def add_log():
    """Allows a user to add a work log entry"""
    print("Log Entry Form")

    save = 'n'
    name = input("What is your name? ")
    title = input("What is the Task Title?  ")
    while save == 'n':
        try:
            spent_time = int(input("How much time did it take? Enter minutes in numbers only\n>>  "))
            print("Add your notes here. Press ctl+D when done.")
            notes = sys.stdin.read().strip()
            save = input("Would you like to save this log? Y/n  ")

            if save.lower().strip() == 'y':
                Log.create(
                    employee_name=name,
                    task_title=title,
                    time_spent=spent_time,
                    general_notes=notes
                )
                print("Saved successfully!")
            else:
                save = 'not saving pal'
        except ValueError:
            print("Please enter minutes as a number only. Ex. 42")
            continue


def edit_log():
    """Allows a user to edit a log entry"""
    pass


def remove_log(entry):
    """Allows a user to remove a log entry"""
    if input("Are you sure?  y/N  ").lower() == 'y':
        entry.delete_instance()
        print("Entry deleted!")


def view_logs(start_date=None, end_date=None):
    """View all logs"""
    # list all for particular employee
    # list all for a date or search
    # list all for date range
    # list all people if they share a name and allow user to choose
    # display entries one at a time with the ability to page through (previous/next/back)
    logs = Log.select().order_by(Log.date.desc())

    if start_date and end_date:
        logs = Log.select().order_by(Log.date)
        logs = logs.where(Log.date.between(start_date, end_date))

    for log in logs:
        clear_screen()
        date = log.date.strftime('%A %B %d, %Y %I:%M%p')
        print("=" * len(date))
        print(date)
        print("Name: {}".format(log.employee_name))
        print("Task Title: {}".format(log.task_title))
        print("Minutes Worked: {}".format(log.time_spent))
        print("Notes: {}".format(log.general_notes))
        print('=' * len(date))
        print()
        print("N) for next log entry")
        print("d) to delete log entry")
        print('q) return to main menu')

        next_action = input('\nAction: [Ndq]  ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            remove_log(log)


def search_by_name():
    """Search for logs by employee name"""
    # view_logs(input("Enter Employee Name: ").lower())
    logs = Log.select().order_by(Log.date.desc())
    search_name = input("Enter Employee Name: ").lower()
    logs = logs.where(Log.employee_name.contains(search_name))
    print("Matches:\n")
    for log in logs:
        print(log.employee_name)
    input("\nPress enter to return to menu.")


def search_by_date():
    """Search for logs by date range: MM/DD/YYYY"""
    # logs = Log.select().order_by(Log.date.desc())
    start_date = datetime.datetime.strptime(input("Enter Start Date MM/DD/YY: "), "%m/%d/%Y")
    end_date = datetime.datetime.strptime(input("Enter End Date MM/DD/YY: "), "%m/%d/%Y")
    view_logs(start_date, end_date)
    # logs = logs.where(Log.date >= start_date & Log.date <= end_date)
    # for log in logs:
    #     clear_screen()
    #     date = log.date.strftime('%A %B %d, %Y %I:%M%p')
    #     print("=" * len(date))
    #     print(date)
    #     print("Name: {}".format(log.employee_name))
    #     print("Task Title: {}".format(log.task_title))
    #     print("Minutes Worked: {}".format(log.time_spent))
    #     print("Notes: {}".format(log.general_notes))
    #     print('=' * len(date))
    #     print()
    #     print("N) for next log entry")
    #     print("d) to delete log entry")
    #     print('q) return to main menu')

    #     next_action = input('\nAction: [Ndq]  ').lower().strip()
    #     if next_action == 'q':
    #         break
    #     elif next_action == 'd':
    #         remove_log(log)


def print_entry():
    """Print the entries to the screen in a readable format"""
    # print a report to the screen
    # include date, title_of_task, time spent, employee, and general notes
    pass


menu = OrderedDict([
    ("1", add_log),
    ("2", view_logs),
    ("3", search_by_name),
    ("4", search_by_date)
])

sub_menu = OrderedDict([
    ("e", edit_log),
    ("d", remove_log),
])


def menu_loop():
    """Display a menu to the user at program start"""
    choice = None

    while choice != 'q':
        clear_screen()
        print(("*" * 17) + "\nWork Log Database\n" + ("*" * 17) + "\n")
        print("Enter 'q' to quit.\n")
        for key, value in menu.items():
            print('{}) {}\n'.format(key, value.__doc__))
        choice = input("Action:  ").lower().strip()
        if choice in menu:
            clear_screen()
            menu[choice]()


if __name__ == '__main__':
    initialize()
    menu_loop()