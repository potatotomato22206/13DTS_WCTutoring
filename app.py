from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

db = "WC_Tutoring_db"


def db_query(phrase, secondary=None):
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if secondary is None:
        cur.execute(phrase)
    else:
        cur.execute(phrase, secondary)

    raw_output = cur.fetchall()
    con.close()
    return raw_output


@app.route('/')
def homepage():  # put application's code here
    raw = db_query("SELECT * FROM Tutor_Sessions")
    output = [dict(row) for row in raw]
    name_dict = []
    for row in output:
        if row["Ses_Tutor"] is None:
            name_zipped = "No Tutor"
        else:
            name_raw = db_query("SELECT first_name, last_name FROM tutors WHERE tutor_pk=?", (row["Ses_Tutor"], ))
            name = [dict(row) for row in name_raw]
            name_zipped = name[0]["first_name"] + " " + name[0]["last_name"]
        name_dict.append([row["Ses_pk"], name_zipped])

    return render_template('homepage.html', AllTutorSeshData=output, Tutor_Name=name_dict)


@app.route('/session/<session_number>')
def view_session(session_number):
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Tutor_Sessions WHERE Ses_pk=?", (session_number, ))
    raw_output = cur.fetchall()
    con.close()
    output = [dict(row) for row in raw_output]
    print(output)
    return render_template("Session_Viewer.html", FAH_output=output)


@app.route('/account/login', methods=['POST', 'GET'])
def login():
    return render_template("login.html")


@app.route('/account/signup', methods=['POST', 'GET'])
def signup():
    return render_template("signup.html")


if __name__ == '__main__':
    app.run()
