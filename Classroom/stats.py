import globals
import numpy as np
import actions
import assignment
import matplotlib.pyplot as plt


def bar_chart(labels, data1, label1, data2, label2, x_label, y_label, title):
    x1 = np.arange(len(labels))
    x2 = [i + 0.25 for i in x1]
    plt.bar(x1, data1, 0.25, label=label1, color='g')
    plt.bar(x2, data2, 0.25, label=label2, color='r')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(x1 + 0.25 / 2, labels)
    plt.legend()
    plt.show()


def submission():
    query = "SELECT count(1) FROM classroom_roles WHERE class_code = '" + globals.current_classroom + "' AND role = 'Student'"
    cur = globals.connection.cursor()
    cur.execute(query)
    result = cur.fetchone()
    total = result[0]
    if total != 0:
        query = "SELECT cw.title, count(s.id) FROM classwork cw LEFT OUTER JOIN submission s " \
                "ON cw.id = s.asgn_id WHERE cw.class_code = '" + globals.current_classroom + "' GROUP BY cw.id"
        cur = globals.connection.cursor()
        cur.execute(query)
        result = np.array(cur.fetchall())

        labels = np.array(result[:, 0])
        submitted = np.array(result[:, 1])
        submitted = [int(a) for a in submitted]
        not_submitted = [total - a for a in submitted]

        bar_chart(labels, submitted, "Submitted", not_submitted, "Not Submitted", "Assignment Title", "Frequency",
                  "Assignment-wise Statistics")

        actions.update_classroom_main()


def add_to_marks_list(result, total_students, total_marks):
    marks = [0, 0, 0, 0, 0]
    marks[0] += total_students - len(result)
    for m in result:
        if m[0] is not None:
            pct = (m[0] / total_marks) * 100
            if pct > 90:
                marks[4] += 1
            elif pct > 80:
                marks[3] += 1
            elif pct > 60:
                marks[2] += 1
            elif pct > 40:
                marks[1] += 1
            else:
                marks[0] += 1
        else:
            marks[0] += 1
    return marks


def pie_chart(marks, total_students):
    labels = ["(0 - 40)%", "(41 - 60)%", "(61 - 80)%", "(81 - 90)%", "(91 - 100)%"]

    def to_value(p):
        a = int(np.round(p / 100. * total_students, 0))
        if a > 0:
            return "{:d} - {:.1f}%".format(a, p)
        return ""

    plt.pie(marks, autopct=to_value)

    plt.title("Number of Students in the given Percentage Bracket")
    plt.legend(labels=labels, title="Percentage", bbox_to_anchor=(1.5, 1))
    plt.show()


def grades(what):
    query = "SELECT count(1) FROM classroom_roles WHERE class_code = '" + globals.current_classroom + "' AND role = 'Student'"
    cur = globals.connection.cursor()
    cur.execute(query)
    result = cur.fetchone()
    total_students = result[0]
    if total_students != 0:
        total_marks = globals.assignment_selected[4]
        asgn_id = str(globals.assignment_selected[0])
        query = "SELECT marks FROM submission WHERE asgn_id = " + asgn_id
        cur = globals.connection.cursor()
        cur.execute(query)
        result = cur.fetchall()

        marks = add_to_marks_list(result, total_students, total_marks)

        pie_chart(marks, total_students)

        assignment.submission_details(what)


def all_grades():
    query = "SELECT count(1) FROM classroom_roles WHERE class_code = '" + globals.current_classroom + "' AND role = 'Student'"
    cur = globals.connection.cursor()
    cur.execute(query)
    result = cur.fetchone()
    total_students = result[0]

    query = "SELECT sum(marks) FROM classwork WHERE class_code = '" + globals.current_classroom + "'"
    cur = globals.connection.cursor()
    cur.execute(query)
    result = cur.fetchone()
    total_marks = result[0]

    query = "SELECT sum(marks), s_id FROM submission WHERE asgn_id in (SELECT id FROM classwork WHERE class_code = '" + globals.current_classroom + "') GROUP BY s_id"
    cur = globals.connection.cursor()
    cur.execute(query)
    result = cur.fetchall()

    marks = add_to_marks_list(result, total_students, total_marks)

    pie_chart(marks, total_students)
    actions.update_classroom_main()
