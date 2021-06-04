import actions
import globals
import stats
import utilities


def verify_and_add(email, role):
    query = "SELECT id FROM users WHERE email = '" + email + "'"
    cur = globals.connection.cursor()
    cur.execute(query)
    result = cur.fetchone()
    if result is not None:
        user_id = result[0]
        query = "INSERT INTO classroom_roles(class_code, user_id, role) " \
                "SELECT '" + globals.current_classroom + "', " + str(user_id) + ", '" + role + "' FROM dual " \
                "WHERE NOT EXISTS (SELECT * FROM classroom_roles WHERE " \
                "class_code = '" + globals.current_classroom + "' AND user_id = " + str(user_id) + ")"
        cur = globals.connection.cursor()
        cur.execute(query)
        if cur.rowcount == 1:
            print(email + " added as " + role + "!")
        else:
            query = "SELECT role FROM classroom_roles WHERE " \
                    "user_id = " + str(user_id) + " AND class_code = '" + globals.current_classroom + "'"
            cur = globals.connection.cursor()
            cur.execute(query)
            result = cur.fetchone()
            print("User already present in the Classroom as", result[0])
    else:
        print("User with email ", email, "does not exist!")


def display_added_users(role):
    query = "SELECT u.email from users u INNER JOIN classroom_roles cr ON u.id = cr.user_id " \
            "WHERE cr.class_code = '" + globals.current_classroom+ "' and cr.role = '" + role + "'"
    cur = globals.connection.cursor()
    cur.execute(query)
    users = cur.fetchall()
    for u in users:
        print(" - " + u[0] + " - ")


def add_user_to_classroom(role):
    globals.display_current_classroom()
    display_added_users(role)
    print("Note: To add more than 1 ", role + "s use ',' to separate several emails")
    email = input("Email(s):")
    emails = email.split(',')
    for email in emails:
        email = email.strip()
        verify_and_add(email, role)
    actions.update_classroom_main()


def update_classroom_info():
    actions.update_classroom_info()


def base_action(choice):
    if choice == '0':
        actions.authenticate()
    elif choice == '#':
        actions.classroom()
    elif choice == '1':
        add_user_to_classroom('Student')
    elif choice == '2':
        add_user_to_classroom('Co-teacher')
    elif choice == '3':
        update_classroom_info()
    elif choice == '4':
        actions.classwork()
    elif choice == '5':
        # assignment submission statistics - bar chart
        stats.submission()
    elif choice == '6':
        # overall score of students (range of %)
        stats.all_grades()
    else:
        print("Invalid Choice! Try Again!")
        actions.update_classroom_main()


def update(what):
    globals.display_current_classroom()
    print("Press # to go back")
    entered = input("Enter new " + what + ": ")

    if entered != '#':
        pswd = input("Password: ")
        if entered != '' and pswd != '':
            if pswd == utilities.get_pass():
                query = "UPDATE classrooms SET " + what + " = '" + entered + "' " \
                                                                             "WHERE code = '" + globals.current_classroom + "'"
                cur = globals.connection.cursor()
                cur.execute(query)
                print(what + " Updated!")
                if what == 'subject':
                    globals.current_subject = entered
                elif what == 'session':
                    globals.current_session = entered
                actions.update_classroom_info()
            else:
                print("Incorrect Password! Try Again!")
                update(what)
        else:
            print("Please enter all the fields!")
            update(what)
    else:
        actions.update_classroom_info()


def update_action(choice):
    if choice == '0':
        actions.authenticate()
    elif choice == '#':
        actions.update_classroom_main()
    elif choice == '1':
        update('subject')
    elif choice == '2':
        update('class')
    elif choice == '3':
        update('session')
    else:
        print("Invalid Choice! Try Again!")
        actions.update_classroom_info()
