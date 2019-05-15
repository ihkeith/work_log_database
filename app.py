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
     date = DateTimeField(default=datetime.datetime.now())
     time_spent = None  # fill in with a duration
     general_notes = TextField()

     class Meta:
         database = db


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def initialize():
    """Create the database and table if they don't already exist"""
    db.connect()
    db.create_tables([Log], safe=True)


def menu():
    """Display a menu to the user at program start"""
    pass


def add_entry():
    """Allows a user to add a work log entry"""
    # allow a user to create an entry
    pass


def edit_entry():
    # allow a user to edit an entry
    pass


def remove_entry():
    # remove an entry
    pass


def list_entries():
    # list all for particular employee
    # list all for a date or search
    # list all for date range
    # list all people if they share a name and allow user to choose
    # display entries one at a time with the ability to page through (previous/next/back)
    pass


def print_entry():
    # print a report to the screen
    # include date, title_of_task, time spent, employee, and general notes
    pass


