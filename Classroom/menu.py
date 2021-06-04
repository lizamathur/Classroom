import globals


def greet():
    print()
    print("Welcome to Classroom!")


def choice():
    print()
    ch = input("Enter your choice: ")
    return ch


def authentication():
    globals.current_user_id = None
    globals.current_user_name = None
    print()
    print("-------------Main Menu-----------------")
    print("1. Sign In")
    print("2. Register")
    print("0. Exit")
    return choice()


def home():
    print()
    globals.display_name()
    print("1. Classroom")
    print("2. Personal")
    print("0. Exit")
    print("#. Back")
    return choice()


def classroom():
    print()
    globals.display_name()
    print("1. Show Classrooms")
    if globals.user_role == 'Teacher' or globals.user_role == 'admin':
        print("2. Add a new Classroom")
        print("3. Delete a Classroom")
    print("0. Exit")
    print("#. Back")
    return choice()


def personal():
    print()
    globals.display_full_info()
    print("1. Update Name")
    print("2. Update Email")
    print("3. Change Password")
    print("0. Exit")
    print("#. Back")
    return choice()


def classroom_update():
    print()
    globals.display_current_classroom()
    print("1. Add Students")
    print("2. Add Co-Teachers")
    print("3. Update Classroom Info")
    print("4. Classwork")
    print("5. Submission Statistics of All Assignments")
    print("6. Performance of Students - Overall Score")
    print("0. Exit")
    print("#. Back")
    return choice()


def update_classroom_info():
    print()
    globals.display_current_classroom()
    print("1. Update Subject")
    print("2. Update Class/Sem")
    print("3. Change Session")
    print("0. Exit")
    print("#. Back")
    return choice()


def classwork():
    print()
    globals.display_current_classroom()
    print("1. Show Active Assignments")
    print("2. Show Previous Assignments")
    if globals.current_classroom_role != 'Student':
        print("3. Add a new Assignment")
    print("0. Exit")
    print("#. Back")
    return choice()
