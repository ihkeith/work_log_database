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
     time_spent = DateTimeField()  # fill in time spent in minutes
     general_notes = TextField()

     class Meta:
         database = db


def clear_screen():
    """Clears the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def initialize():
    """Create the database and table if they don't already exist"""
    db.connect()
    db.create_tables([Log], safe=True)


def add_entry():
    """Allows a user to add a work log entry"""
    print("Log Entry Form")

    pass


def edit_entry():
    """Allows a user to edit an entry"""
    pass


def remove_entry():
    """Allows a user to remove an entry"""
    pass


def find_entries():
    """Allows a user to find entries based on various search criteria"""
    # list all for particular employee
    # list all for a date or search
    # list all for date range
    # list all people if they share a name and allow user to choose
    # display entries one at a time with the ability to page through (previous/next/back)
    pass


def print_entry():
    """Print the entries to the screen in a readable format"""
    # print a report to the screen
    # include date, title_of_task, time spent, employee, and general notes
    pass


menu = OrderedDict([
    ("1", add_entry),
    ("2", find_entries),
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