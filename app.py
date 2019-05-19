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


def edit_log(log):
    """Allows a user to edit a log entry"""
    print("Log Entry Form")

    save = 'n'
    while save == 'n':
        try:
            name = input("What is your name?  ")
            if not name:
                print("Please enter your name")
                continue
            title = input("What is the Task Title?  ")
            if not title:
                print("Please enter a Title")
                continue
            spent_time = int(input("How much time did it take? Enter minutes in numbers only.  "))
            if not spent_time:
                print('Please enter time spent')
                continue
            date = datetime.datetime.strptime(input("Please enter new date in MM/DD/YYYY 00:00PM format  "), "%m/%d/%Y %I:%M%p")

            print("Add your notes here. Press ctl+D when done.")
            notes = sys.stdin.read().strip()
            save = input("Would you like to save this log? Y/n  ")

            if save.lower().strip() == 'y':
                log.date = date
                log.employee_name = name
                log.task_title = title
                log.time_spent = spent_time
                log.general_notes=notes
                log.save()
                print("Saved successfully!")
            else:
                save = 'not saving pal'
        except ValueError:
            print("Please enter minutes as a number only. Ex. 42")
            continue


def remove_log(log):
    """Allows a user to remove a log entry"""
    if input("Are you sure?  y/N  ").lower() == 'y':
        log.delete_instance()
        print("Log deleted!")


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
        logs = logs.where(Log.date.contains(search_date))
    if start_date and end_date:
        logs = Log.select().order_by(Log.date)
        logs = logs.where(Log.date.between(start_date, end_date))
    if search_by_term:
        logs = logs.where(
            Log.task_title.contains(search_by_term) |
            Log.general_notes.contains(search_by_term))
    if name:
        logs = logs.where(Log.employee_name == name)
    if spent:
        logs = logs.where(Log.time_spent == spent)
    if logs:
        print_entry(logs)
    else:
        print("No matches were found.")
        input("\nPress enter to continue.")


def search_by_name():
    """Search by name"""
    logs = Log.select().order_by(Log.date.desc())
    search_name = input("Enter Employee Name: ").lower()
    logs = logs.where(Log.employee_name.contains(search_name))
    name_list = set([log.employee_name for log in logs])
    name_menu = OrderedDict([])

    if len(name_list) == 1:
        find_logs(start_date=None, end_date=None, search_by_term=None, name=search_name)
    else:
        print("Matches:\n")

        for key, value in enumerate(name_list, start=1):
            name_menu.update({key:value})
            print(key, value)
        
        choice = None
        while choice == None:
            try:
                choice = input("\nEnter the number for the correct name.  ")
                choice = int(choice)
                find_logs(start_date=None, end_date=None, search_by_term=None, name=name_menu[choice])
            except KeyError:
                print("That is not a valid choice.")
                choice = None
                continue
            except ValueError:
                print("That is not a valid choice.")
                choice = None
                continue


def view_all_names():
    """Search logs by employee name"""
    logs = Log.select().order_by(Log.date.desc())
    name_list = set([log.employee_name for log in logs])
    sub_menu = OrderedDict([('0', "Search by name")])
    for key, value in enumerate(name_list, start=1):
        sub_menu.update({key:value})
    
    print("Enter 'q' to quit.\n")
    print("Matches:\n")
    for key, value in sub_menu.items():
        print(key, value)
    
    choice = None
    while choice == None:
        try:
            choice = input("\nEnter the number for the correct name.  ")
            if choice.lower().strip() == 'q':
                pass
            elif choice == '0':
                search_by_name()
            else:
                choice = int(choice)
                try:
                    find_logs(start_date=None, end_date=None, search_by_term=None, name=sub_menu[choice])
                except KeyError:
                    print("That is not a valid choice.")
                    choice = None
                    continue
        except ValueError:
            print("That is not a valid choice.")
            choice = None
            continue


def search_by_date():
    """Search for logs by date or date range"""
    choice = None
    print("Enter 'q' to quit.\n")
    print("1) Search by Date")
    print("2) Search by Date Range")

    while not choice:
        choice = input("\nAction:  ")
        if choice == '1':
            logs = Log.select().order_by(Log.date.desc())
            log_list = set([log.date.strftime("%m/%d/%Y") for log in logs])
            log_choices = [log for log in log_list]
            for key, value in enumerate(log_choices, start=1):
                print("{}) {}".format(key, value))
            
            new_choice = None
            while new_choice == None:
                try: 
                    new_choice = input("Enter number for date to search.  ")
                    new_choice = log_choices[int(new_choice) - 1]
                    choice_date = datetime.datetime.strptime(new_choice, "%m/%d/%Y")
                    find_logs(search_date=choice_date.date())
                except ValueError:
                    print("That is not a valid date. Please try again")
                    choice = None
                    continue
        elif  choice == '2':
            try:
                start_date_ = datetime.datetime.strptime(input("Enter Start Date MM/DD/YYYY: "), "%m/%d/%Y")
                end_date_ = datetime.datetime.strptime(input("Enter End Date MM/DD/YYYY: "), "%m/%d/%Y")
                find_logs(start_date=start_date_.date(), end_date=end_date_.date()+datetime.timedelta(days=1))
            except ValueError:
                print("That is not a valid date. Please try again")
                choice = None
                continue
        elif choice.lower().strip() == 'q':
            pass
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
    log_list = [log for log in logs]
    index = 0
    while True:
        try:
            actions = [
        "N) for next log entry",
        "p) for previous log entry",
        "d) to delete log entry",
        "e) to edit log entry",
        'q) return to main menu',
    ]
            clear_screen()
            if index == 0:
                actions.remove("p) for previous log entry")
            date = log_list[index].date.strftime('%A %B %d, %Y %I:%M%p')
            print("=" * len(date))
            print(date)
            print("Name: {}".format(log_list[index].employee_name))
            print("Task Title: {}".format(log_list[index].task_title))
            print("Minutes Worked: {}".format(log_list[index].time_spent))
            print("Notes: {}".format(log_list[index].general_notes))
            print('=' * len(date))
            print()
            for action in actions:
                print(action)

            next_action = input('\nAction:  ').lower().strip()
            if next_action == 'q':
                clear_screen()
                print(("*" * 17) + "\nWork Log Database\n" + ("*" * 17) + "\n")
                print("Thank you using the Work Log Database. Have a great day!")
                break
            elif next_action == 'd':
                remove_log(log_list[index])
            elif next_action == 'e':
                edit_log(log_list[index])
            elif next_action == 'p' and index == 0:
                pass
            elif next_action == 'p' and index != 0:
                index -= 1
                continue
            else:
                index += 1
        except IndexError:
            print("No more records to view here.")
            input("Press enter to return to the previous menu.")
            return False


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


def menu_loop():
    """Display a menu to the user at program start"""
    choice = None

    while choice != 'q':
        try:
            clear_screen()
            print(("*" * 17) + "\nWork Log Database\n" + ("*" * 17) + "\n")
            print("Enter 'q' to quit.\n")
            for key, value in menu.items():
                print('{}) {}'.format(key, value.__doc__))
            choice = input("\nAction:  ").lower().strip()
            if choice in menu:
                clear_screen()
                menu[choice]()
            if choice == 'q':
                clear_screen()
                print(("*" * 17) + "\nWork Log Database\n" + ("*" * 17) + "\n")
                print("Thank you using the Work Log Database. Have a great day!\n")
        except KeyboardInterrupt:
            print("\nNice try, but you can't quit that way!")
            input("Press enter to continue")


if __name__ == '__main__':
    try:
        initialize()
        menu_loop()
    except KeyboardInterrupt:
        print("\nFine. Go ahead and leave. See if I care.")