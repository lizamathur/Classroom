import random
import string
import globals


def generate_code():
    source = string.ascii_letters + string.digits
    code = ''.join((random.choice(source) for i in range(6)))
    return code


def get_pass():
    query = "SELECT password FROM users WHERE id = " + str(globals.current_user_id)
    cur = globals.connection.cursor()
    cur.execute(query)
    result = cur.fetchone()
    return result[0]
