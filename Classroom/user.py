import actions
import globals
import utilities


def update_name():
    globals.display_full_info()
    print("Press # to go back")
    name = input("New Name: ")
    pswd = input("Password: ")
    if name != '' and pswd != '':
        if name != '#':
            if pswd == utilities.get_pass():
                query = "UPDATE users SET name = '" + name + "' " \
                        "WHERE id = " + str(globals.current_user_id)
                cur = globals.connection.cursor()
                cur.execute(query)
                globals.current_user_name = name
                print("Name Updated!")
                actions.personal_info()
            else:
                print("Incorrect Password! Try Again!")
                update_name()
        else:
            actions.personal_info()
    else:
        print("Name cannot be blank! Try again!")
        update_name()


def update_email():
    globals.display_full_info()
    print("Press # to go back")
    email = input("New Email: ")
    pswd = input("Password: ")
    if email != '' and pswd != '':
        if email != '#':
            if pswd == utilities.get_pass():
                query = "UPDATE users SET email = '" + email + "' " \
                                                             "WHERE id = " + str(globals.current_user_id)
                cur = globals.connection.cursor()
                cur.execute(query)
                print("Email Updated!")
                actions.personal_info()
            else:
                print("Incorrect Password! Try Again!")
                update_email()
        else:
            actions.personal_info()
    else:
        print("Email cannot be blank! Try again!")
        update_email()


def update_password():
    globals.display_full_info()
    print("Press # to go back")
    cur_pas = input("Current Password: ")
    if cur_pas != '#':
        if cur_pas == utilities.get_pass():
            pswd = input("New Password: ")
            c_pswd = input("Confirm Password: ")
            if pswd == c_pswd:
                query = "UPDATE users SET password = '" + pswd + "' WHERE id = " + str(globals.current_user_id)
                cur = globals.connection.cursor()
                cur.execute(query)
                print("Password Updated!")
            else:
                print("Passwords do not match!")
            actions.personal_info()
        else:
            print("Incorrect Password! Try again!")
            update_password()
    else:
        actions.personal_info()


def action(choice):
    if choice == '0':
        exit()
    elif choice == '#':
        actions.home()
    elif choice == '1':
        update_name()
    elif choice == '2':
        update_email()
    elif choice == '3':
        update_password()
    else:
        print("Invalid Choice! Try Again!")
        actions.personal_info()
