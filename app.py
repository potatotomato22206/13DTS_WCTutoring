from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

db = "C:/Users/22206/PycharmProjects/WC_Tutoring_Project/WC_Tutoring_db"


@app.route('/')
def homepage():  # put application's code here
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM Tutor_Sessions")
    rows = cur.fetchall()
    con.close()
    output = [dict(row) for row in rows]
    print(output)
    return render_template('homepage.html', AllTutorSeshData=output)


if __name__ == '__main__':
    app.run()
