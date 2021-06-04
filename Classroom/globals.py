connection = None
current_user_id = None
current_user_name = None
user_role = None
# code
current_classroom = None
current_subject = None
current_session = None
# all data
classroom_selected = None
assignment_selected = None
current_classroom_role = None


def display_name():
    print()
    print("............ Logged in as:", current_user_name, "............")


def get_email():
    query = "SELECT email FROM users WHERE id = " + str(current_user_id)
    cur = connection.cursor()
    cur.execute(query)
    result = cur.fetchone()
    return result[0]


def display_full_info():
    print()
    print("--------- " + current_user_name + " | " + get_email() + " ---------")


def set_classroom_session(code, subject, session):
    global current_classroom, current_subject, current_session
    current_classroom = code
    current_subject = subject
    current_session = session


def display_current_classroom():
    print("--------- " + current_classroom + ": " + current_subject + " | " + current_session + " ---------")


def print_curr_asgn_details():
    print("------ " + assignment_selected[2] + " | " + assignment_selected[3] + " ------")
    print("Question Link: " + assignment_selected[5])
    print("Marks: " + str(assignment_selected[4]) + " | Deadline:" + str(assignment_selected[8]))