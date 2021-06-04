import actions
import classrooms
import globals
import utilities
import mysql.connector as mysql


def add_classroom():
    print()
    print("-------------Create Classroom-----------------")
    subject = input("Enter Subject: ")
    class_name = input("Enter Class/Semester: ")
    session = input("Enter Session: ")
    code = utilities.generate_code()
    if subject != '' and class_name != '' and session != '':
        try:
            query = "INSERT INTO classrooms(code, owner, subject, class, session) VALUES (" \
                    "'" + code + "', " + str(globals.current_user_id) + ", '" + subject + "', '" + class_name + "', " \
                    "'" + session + "')"
            cur = globals.connection.cursor()
            cur.execute(query)
            print("Classroom Created | Code:", code)
            globals.current_classroom = code
            globals.current_classroom_role = 'Teacher'
            globals.set_classroom_session(code, subject, session)
            actions.update_classroom_main()
        except mysql.errors.ProgrammingError:
            print("Something went wrong!")
            add_classroom()
    else:
        print("Please enter all the fields!")
        add_classroom()


def delete_class():
    # query = "DELETE FROM submission WHERE asgn_id in " \
    #         "(SELECT id FROM classwork WHERE class_code = '" + globals.current_classroom + "')"
    # cur = globals.connection.cursor()
    # cur.execute(query)
    #
    # query = "DELETE FROM classwork WHERE class_code = '" + globals.current_classroom + "'"
    # cur = globals.connection.cursor()
    # cur.execute(query)
    #
    # query = "DELETE FROM classroom_roles WHERE class_code = '" + globals.current_classroom + "'"
    # cur = globals.connection.cursor()
    # cur.execute(query)
    #
    # query = "DELETE FROM classrooms WHERE code = '" + globals.current_classroom + "'"
    query = "DELETE c, cr, cw, s FROM classrooms c LEFT OUTER JOIN classroom_roles cr ON c.code = cr.class_code " \
            "LEFT OUTER JOIN classwork cw ON c.code = cw.class_code LEFT OUTER JOIN submission s ON cw.id = s.asgn_id WHERE c.code='" + globals.current_classroom + "'"
    cur = globals.connection.cursor()
    cur.execute(query)

    print("Classroom Successfully deleted!")


def delete_classroom():
    print()
    print("-------------Delete Classroom-----------------")
    classrooms.show_classes('delete')
    if globals.current_classroom is not None:
        sure = input("Are you sure you want to delete? (Y/Others): ")
        if sure == 'Y' or sure == 'y':
            delete_class()
        delete_classroom()
    else:
        print("You do not own any Classroom!")
        actions.classroom()


def action(choice):
    if choice == '0':
        actions.authenticate()
    elif choice == '#':
        actions.home()
    elif choice == '1':
        classrooms.show_classes('show')
    else:
        if globals.user_role == 'Teacher' or globals.user_role == 'admin':
            if choice == '2':
                add_classroom()
            elif choice == '3':
                delete_classroom()
            else:
                print("Invalid Choice! Try Again!")
                actions.classroom()
        else:
            print("Invalid Choice! Try Again!")
            actions.classroom()
