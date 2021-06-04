import globals
import menu
import actions


def show_menu(classes, why):
    i = 0
    for det in classes:
        i += 1
        print(str(i) + ". " + det[1] + " | " + det[3] + " | " + det[4] + " | " + det[5] + " ---- " + det[6])
    if i == 0:
        print("No Classrooms!")
    print("0. Exit")
    print("#. Back")
    ch = menu.choice()
    if ch == '0':
        actions.authenticate()
    elif ch == '#':
        actions.classroom()
    elif int(ch) <= i:
        globals.classroom_selected = classes[int(ch) - 1]
        globals.current_classroom = globals.classroom_selected[1]
        globals.current_subject = globals.classroom_selected[3]
        globals.current_session = globals.classroom_selected[5]
        globals.current_classroom_role = globals.classroom_selected[6]
        print("Classroom selected: " + globals.current_classroom)
        if why != 'delete':
            if globals.current_classroom_role != 'Student':
                actions.update_classroom_main()
            else:
                actions.classwork()
    else:
        print("Invalid Choice! Try Again")
        show_classes(why)


def show_all(query):
    print()
    cur = globals.connection.cursor()
    cur.execute(query)
    classes = cur.fetchall()
    if len(classes) > 0:
        print("-------------Classrooms-----------------")
    else:
        print("-------------No Classrooms-----------------")
    show_menu(classes, 'show')


def show_mine(query):
    cur = globals.connection.cursor()
    cur.execute(query)
    classes = cur.fetchall()
    show_menu(classes, 'delete')


def show_classes(why):
    if why == 'delete':
        query = "SELECT *, 'Teacher' as role from classrooms where owner = " + str(globals.current_user_id)
        show_mine(query)
    elif why == 'show':
        if globals.user_role == 'admin':
            query = "SELECT c.*, u.email as owner from classrooms c INNER JOIN users u ON c.owner = u.id"
        else:
            query = "SELECT *, 'Teacher' as role from classrooms where owner = " + str(globals.current_user_id) + \
                " UNION (SELECT c.*, cr.role FROM classrooms c INNER JOIN classroom_roles cr ON " \
                "c.code = cr.class_code WHERE cr.user_id = " + str(globals.current_user_id) + ")"
        show_all(query)
