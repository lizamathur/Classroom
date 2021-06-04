import mysql.connector as mysql


def connect():
    try:
        con = mysql.connect(host='localhost', user='root', password='', database='classroom')
        print(con)
        query = 'CREATE TABLE IF NOT EXISTS users(' \
                'id int PRIMARY KEY AUTO_INCREMENT, ' \
                'name VARCHAR(100), ' \
                'email VARCHAR(100), ' \
                'password VARCHAR(100), ' \
                'role VARCHAR(20))'

        cur = con.cursor()
        cur.execute(query)

        query = 'CREATE TABLE IF NOT EXISTS classrooms(' \
                'id int PRIMARY KEY AUTO_INCREMENT, ' \
                'code VARCHAR(6), ' \
                'owner int, ' \
                'subject VARCHAR(100), ' \
                'class VARCHAR(100), ' \
                'session VARCHAR(100), ' \
                'FOREIGN KEY(owner) REFERENCES users(id))'

        cur = con.cursor()
        cur.execute(query)

        query = 'CREATE TABLE IF NOT EXISTS classroom_roles(' \
                'id int PRIMARY KEY AUTO_INCREMENT, ' \
                'class_code VARCHAR(6), ' \
                'user_id int, ' \
                'role VARCHAR(100), ' \
                'FOREIGN KEY(user_id) REFERENCES users(id), ' \
                'FOREIGN KEY(class_code) REFERENCES classrooms(code))'

        cur = con.cursor()
        cur.execute(query)

        query = 'CREATE TABLE IF NOT EXISTS classwork(id int PRIMARY KEY AUTO_INCREMENT, class_code VARCHAR(6), ' \
                'title VARCHAR(255), description VARCHAR(255), marks FLOAT, link VARCHAR(255), ' \
                'started DATETIME DEFAULT now(), duration FLOAT, FOREIGN KEY(class_code) REFERENCES classrooms(code))'

        cur = con.cursor()
        cur.execute(query)

        query = 'CREATE TABLE IF NOT EXISTS submission(id int AUTO_INCREMENT PRIMARY KEY, ' \
                'asgn_id int, s_id int, link VARCHAR(255), sub_time DATETIME DEFAULT now(), marks float, ' \
                'FOREIGN KEY(asgn_id) REFERENCES classwork(id), ' \
                'FOREIGN KEY(s_id) REFERENCES users(id))'

        cur = con.cursor()
        cur.execute(query)

        return con
    except mysql.errors.InterfaceError:
        print("Host cannot be found!")
        exit(1)
    except mysql.errors.ProgrammingError:
        print("Incorrect user/password/database for creating connection!")
        exit(1)
