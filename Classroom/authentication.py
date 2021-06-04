import globals
import actions
import mysql.connector as mysql


def login():
    print()
    print("-------------Log In-----------------")
    email = input("Email: ")
    password = input("Password: ")
    query = "SELECT * FROM users WHERE " \
            "email = '" + email + "' and " + \
            "password = '" + password + "'"
    cur = globals.connection.cursor()
    cur.execute(query)
    result = cur.fetchone()
    if result is not None:
        globals.current_user_id = result[0]
        globals.current_user_name = result[1]
        globals.user_role = result[4]
        print("Welcome,", result[1] + "!")
        actions.home()
    else:
        print("Incorrect email or password!")
        login()


def register():
    print()
    print("-------------Sign Up-----------------")
    name = input("Name: ")
    email = input("Email: ")
    password = input("Password: ")
    c_password = input("Confirm Password: ")
    if name != '' and email != '' and password != '' and c_password != '':
        if password == c_password:
            try:
                query = "INSERT INTO users(name, email, password, role) values (" \
                        "'" + name + "', '" + email + "', '" + password + "', 'student')"
                cur = globals.connection.cursor()
                cur.execute(query)
                print("Registration Successful!")
                actions.authenticate()
            except mysql.errors.ProgrammingError:
                print("Something went wrong!")
                register()
        else:
            print("Passwords do not match!")
            register()
    else:
        print("Please enter all the fields!")
        register()


def action(choice):
    if choice == '0':
        exit(1)
    elif choice == '1':
        login()
    elif choice == '2':
        register()
    else:
        print("Invalid Choice! Try Again!")
        actions.authenticate()
