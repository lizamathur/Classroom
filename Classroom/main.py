import menu
from connection import connect
import globals
import actions

if __name__ == '__main__':

    globals.connection = connect()

    menu.greet()

    actions.authenticate()

