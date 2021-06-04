import menu
import authentication
import user
import classes
import update_classroom
import assignment


def authenticate():
    choice = menu.authentication()
    authentication.action(choice)


def personal_info():
    choice = menu.personal()
    user.action(choice)


def classroom():
    choice = menu.classroom()
    classes.action(choice)


def home():
    choice = menu.home()
    if choice == '0':
        authenticate()
    elif choice == '#':
        authenticate()
    elif choice == '1':
        classroom()
    elif choice == '2':
        personal_info()
    else:
        print("Invalid Choice! Try Again!")
        home()


def update_classroom_main():
    choice = menu.classroom_update()
    update_classroom.base_action(choice)


def update_classroom_info():
    choice = menu.update_classroom_info()
    update_classroom.update_action(choice)


def classwork():
    choice = menu.classwork()
    assignment.action(choice)
