import classrooms
import globals
import actions
import menu
import submissions
import stats
import mysql.connector as mysql


def add_assignment():
    print()
    globals.display_current_classroom()
    title = input("Title: ")
    desc = input("Desc: ")
    marks = input("Marks: ")
    link = input("Assignment Link: ")
    time = input("Allotted Time (hours): ")
    try:
        query = "INSERT INTO classwork(class_code, title, description, marks, link, duration) values(" \
                "'" + globals.current_classroom + "', '" + title + "', '" + desc + "', " \
                                                                                   "" + marks + ", '" + link + "', " + time + ")"
        cur = globals.connection.cursor()
        cur.execute(query)
        print("Assignment Created!")
        actions.classwork()
    except mysql.errors.ProgrammingError:
        print("Something went wrong!")
        add_assignment()


def fetch_asgns(query):
    cur = globals.connection.cursor()
    cur.execute(query)
    assignments = cur.fetchall()
    return assignments


def submission_details(what):
    globals.print_curr_asgn_details()
    print()
    print("1. Submissions")
    print("2. Not yet Submitted")
    print("3. Performance of Students")
    print("0. Exit")
    print("#. Back")
    choice = menu.choice()
    if choice == '0':
        actions.authenticate()
    elif choice == '#':
        show_asgn(what)
    elif choice == '1':
        submissions.submitted_asgns(what)
    elif choice == '2':
        submissions.not_submitted(what)
    elif choice == '3':
        stats.grades(what)
    else:
        print("Invalid Choice! Try Again!")
        action_assignment_selected(what)


def action_assignment_selected(what):

    if globals.current_classroom_role == 'Student':

        if what == 'active':
            globals.print_curr_asgn_details()
            print()
            print("1. Submit Assignment")
            print("0. Exit")
            print("#. Back")
            choice = menu.choice()
            if choice == '0':
                actions.authenticate()
            elif choice == '#':
                show_asgn('active')
            elif choice == '1':
                print("Press # to go back")
                link = input("Enter link to your assignment(can't be edited): ")
                if link != '':
                    if link != '#':
                        try:
                            query = "INSERT INTO submission(asgn_id, s_id, link) " \
                                    "SELECT " + str(globals.assignment_selected[0]) + ", " + str(globals.current_user_id) + ", " \
                                    "'" + link + "' FROM dual WHERE NOT EXISTS (" \
                                    "SELECT * FROM submission WHERE asgn_id = " + str(globals.assignment_selected[0]) + " and " \
                                    "s_id = " + str(globals.current_user_id) + ")"
                            cur = globals.connection.cursor()
                            cur.execute(query)
                            if cur.rowcount == 1:
                                print("Assignment Submitted Successfully!")
                            else:
                                query = "SELECT link FROM submission WHERE asgn_id = " + str(globals.assignment_selected[0]) + " and " \
                                        "s_id = " + str(globals.current_user_id)
                                cur = globals.connection.cursor()
                                cur.execute(query)
                                result = cur.fetchone()
                                print("Sorry, you have already submitted your assignment - " + result[0])
                        except mysql.errors.ProgrammingError:
                            print("Something went wrong!")
                    show_asgn('active')
                else:
                    print("Link cannot be blank! Try Again!")
                    action_assignment_selected(what)
            else:
                print("Invalid Choice! Try Again!")
                action_assignment_selected(what)
        elif what == 'old':
            query = "SELECT link FROM submission WHERE asgn_id = " + str(globals.assignment_selected[0]) + " and " \
                    "s_id = " + str(globals.current_user_id)
            cur = globals.connection.cursor()
            cur.execute(query)
            result = cur.fetchone()
            globals.print_curr_asgn_details()
            if result is not None:
                print("Submitted Link: " + result[0])
            else:
                print("No Submission Found!")
            show_asgn(what)
    else:
        submission_details(what)
    print()


def show_asgn(what):
    print()
    query = None
    if what == 'active':
        query = "SELECT *, DATE_ADD(started, interval duration*60 minute) FROM classwork WHERE " \
                "class_code = '" + globals.current_classroom + "' and " \
                                                               "TIMESTAMPDIFF(MINUTE, now(), DATE_ADD(started, interval duration*60 minute)) > 0"
    elif what == 'old':
        query = "SELECT *, DATE_ADD(started, interval duration*60 minute) FROM classwork WHERE " \
                "class_code = '" + globals.current_classroom + "' and " \
                                                               "TIMESTAMPDIFF(MINUTE, now(), DATE_ADD(started, interval duration*60 minute)) <= 0"

    assignments = fetch_asgns(query)
    i = 0
    for asgn in assignments:
        i += 1
        print(str(i) + ". " + asgn[2] + " | " + asgn[3] + " | Due: " + str(asgn[8]))
    if i == 0:
        print("No Assignments!")
    print("0. Exit")
    print("#. Back")
    ch = menu.choice()
    if ch == '0':
        actions.authenticate()
    elif ch == '#':
        actions.classwork()
    elif int(ch) <= i:
        globals.assignment_selected = assignments[int(ch) - 1]
        action_assignment_selected(what)
    else:
        print("Invalid Choice! Try Again!")
        show_asgn(what)


def action(choice):
    if choice == '0':
        actions.authenticate()
    elif choice == '#':
        classrooms.show_classes('show')
    elif choice == '1':
        show_asgn('active')
    elif choice == '2':
        show_asgn('old')
    else:
        if choice == '3' and (globals.current_classroom_role == 'Teacher' or globals.classroom_selected[6] != 'Student'):
            add_assignment()
        else:
            print("Invalid Choice! Try Again!")
            actions.classwork()
