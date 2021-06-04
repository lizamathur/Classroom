import menu
import actions
import assignment
import globals


def submitted_asgns(what):
    query = "SELECT u.name, u.email, s.link, s.sub_time, s.marks, u.id FROM submission s INNER JOIN users u ON s.s_id = u.id WHERE asgn_id = " + str(
        globals.assignment_selected[0])
    cur = globals.connection.cursor()
    cur.execute(query)
    sub_list = cur.fetchall()
    i = 0
    for sub in sub_list:
        i += 1
        if sub[4] is not None:
            marks = str(sub[4]) + "/" + str(globals.assignment_selected[4])
        else:
            marks = "0/" + str(globals.assignment_selected[4])
        print(str(i) + ". " + sub[0] + " | " + sub[1] + " --- " + sub[2] + " | " + str(sub[3]) + " --- " + marks)
    if i == 0:
        print("No Submissions Received Yet!")
    print("0. Exit")
    print("#. Back")
    choice = menu.choice()
    if choice == '0':
        actions.authenticate()
    elif choice == '#':
        assignment.action_assignment_selected(what)
    elif int(choice) <= i:
        selected_sub = sub_list[int(choice) - 1]
        marks = input("Enter Marks: ")
        if marks != '':
            query = "UPDATE submission SET marks = " + marks + " WHERE s_id = " + str(
                selected_sub[5]) + " and asgn_id = " + str(globals.assignment_selected[0])
            cur = globals.connection.cursor()
            cur.execute(query)
            print("Marks Updated!")
        submitted_asgns(what)
    else:
        print("Invalid Choice! Try Again!")
        submitted_asgns(what)


def not_submitted(what):
    query = "SELECT name, email FROM users WHERE " \
            "id IN (SELECT user_id FROM classroom_roles WHERE " \
            "role = 'Student' and class_code = '" + globals.current_classroom + "' AND user_id NOT IN" \
            "(SELECT s_id FROM submission WHERE asgn_id = " + str(globals.assignment_selected[0]) + "))"
    cur = globals.connection.cursor()
    cur.execute(query)
    records = cur.fetchall()
    i = 0
    for rec in records:
        i += 1
        print("* " + rec[0] + " | " + rec[1])
    if i == 0:
        print("All Submissions Received!")
    print("0. Exit")
    print("#. Back")
    choice = menu.choice()
    if choice == '0':
        actions.authenticate()
    elif choice == '#':
        assignment.action_assignment_selected(what)
    else:
        print("Invalid Choice! Try Again!")
        not_submitted(what)
