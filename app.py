#!/usr/bin/env python3

"""Work Log Database
Author: Ian H Keith
Created: 05/15/2019
"""

from collections import OrderedDict
import datetime
import os
import re
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
    """Create a new log entry"""
    print("Log Entry Form")

    save = 'n'
    while save == 'n':
        try:
            name = input("What is your name? ")
            if not name:
                print("Please enter your name")
                continue
            title = input("What is the Task Title?  ")
            if not title:
                print("Pleae enter a Title")
                continue
            spent_time = int(input("How much time did it take? Enter minutes in numbers only\n>>  "))
            if not spent_time:
                print('Please enter time spent')
                continue
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


def find_logs(
    search_date=None,
    start_date=None,
    end_date=None,
    search_by_term=None,
    name=None,
    spent=None
    ):
    """View all logs"""
    logs = Log.select().order_by(Log.date.desc())

    if search_date:
        logs = logs.where(Log.date == search_date)
    if start_date and end_date:
        logs = Log.select().order_by(Log.date)
        logs = logs.where(Log.date.between(start_date, end_date))
    if search_by_term:
        logs = logs.where(
            Log.task_title.contains(search_by_term) |
            Log.general_notes.contains(search_by_term))
    if name:
        logs = logs.where(Log.employee_name.contains(name))
    if spent:
        logs = logs.where(Log.time_spent == spent)

    if logs:
        print_entry(logs)
    else:
        print("No matches were found.")
        input("Press enter to continue.")


def view_all_names():
    """Search logs by employee name"""
    logs = Log.select().order_by(Log.date.desc())
    name_list = set([log.employee_name for log in logs])
    for key, value in enumerate(name_list, start=1):
        sub_menu.update({key:value})
    
    print("Matches:\n")
    for key, value in sub_menu.items(): print(key, value)
    name = int(input("\nEnter the number for the correct name.  "))

    search_name = input("Enter Employee Name: ").lower()
    logs = logs.where(Log.employee_name.contains(search_name))
    
    
    find_logs(start_date=None, end_date=None, search_by_term=None, name=sub_menu[name])


def search_by_name():
    """Search by name"""
    pass


def search_by_date():
    """Search for logs by date or date range"""
    choice = None
    print("1) Search by Date")
    print("2) Search by Date Range")

    while not choice:
        choice = input("\nAction:  ")
        if choice == '1':
            try:
                search_date = datetime.datetime.strptime(input("Enter Date MM/DD/YYYY: "), "%m/%d/%Y")
                find_logs(search_date)
            except ValueError:
                print("That is not a valid date. Please try again")
                choice = None
                continue
        if  choice == '2':
            try:
                start_date = datetime.datetime.strptime(input("Enter Start Date MM/DD/YYYY: "), "%m/%d/%Y")
                end_date = datetime.datetime.strptime(input("Enter End Date MM/DD/YYYY: "), "%m/%d/%Y")
                find_logs(start_date, end_date)
            except ValueError:
                print("That is not a valid date. Please try again")
                choice = None
                continue
        else:
            print("That is not a valid action.")
            choice = None
            continue


def search_by_term():
    """Search Title and Notes for term"""
    find_logs(start_date=None, end_date=None, search_by_term=input("Enter Term:  "))


def search_by_time_spent():
    """Search logs by time spent"""
    tspent = None
    while not tspent:
        tspent = input("Enter amount of time spent:  ")
        try:
            tspent = int(tspent)
            find_logs(start_date=None, end_date=None, search_by_term=None, spent=tspent)
        except ValueError:
            print("That is not a valid number.")
            tspent = None
            continue


def print_entry(logs):
    """Print the entries to the screen in a readable format"""
    # print a report to the screen
    # include date, title_of_task, time spent, employee, and general notes
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


def search_menu():
    """Search log entries"""
    s_menu = OrderedDict([
    ("1", view_all_names),
    ("2", search_by_date),
    ("3", search_by_time_spent),
    ("4", search_by_term),
    ])
    choice = None

    while choice != 'q':
        clear_screen()
        print("Enter 'q' to quit.\n")
        for key, value in s_menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input("\nAction:  ").lower().strip()
        if choice in s_menu:
            clear_screen()
            s_menu[choice]()


menu = OrderedDict([
    ("1", add_log),
    ("2", search_menu),
])

sub_menu = OrderedDict([('0', search_by_name)])


def menu_loop():
    """Display a menu to the user at program start"""
    choice = None

    while choice != 'q':
        clear_screen()
        print(("*" * 17) + "\nWork Log Database\n" + ("*" * 17) + "\n")
        print("Enter 'q' to quit.\n")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input("\nAction:  ").lower().strip()
        if choice in menu:
            clear_screen()
            menu[choice]()


if __name__ == '__main__':
    initialize()
    menu_loop()