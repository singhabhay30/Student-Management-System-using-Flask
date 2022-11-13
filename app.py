from flask import *
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret"

myconn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database=" student_management"
)
# cur = myconn.cursor()
# cur.execute(
#     "if does not exists create table admin(username varchar(20) NOT NULL Primary KEY, password varchar(64) NOT NULL)")
# myconn.commit()


@ app.route("/")
@ app.route("/admin", methods=["POST", "GET"])
def admin():
    if request.method == "POST":
        uname = request.form['username']
        passw = request.form['password']
        print(uname, passw)
        cur = myconn.cursor()
        cur.execute(
            """select * from admin where username=%s and password=%s""", (uname, passw))
        data = cur.fetchall()
        print(data)
        if len(data) != 0:
            session['logged in'] = True
            flash("Logged In Successfully")
            return render_template("index.html")
        else:
            flash("Wrong Credentials")
    return render_template("login.html")


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        print("Yess")
        return render_template('add.html')
    return render_template("add.html")


if __name__ == "__main__":
    app.run(debug=True)
