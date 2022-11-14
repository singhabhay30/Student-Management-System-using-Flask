from flask import *
import mysql.connector
from datetime import date

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
        if data:
            session['loggedin'] = True
            flash("Logged In Successfully")
            return render_template("home.html")
        else:
            flash("Wrong Credentials")
            return render_template('login.html')
    return render_template("login.html")


@app.route("/add", methods=["POST", "GET"])
def add():
    if not session.get('loggedin'):
        return render_template("login.html")
    if request.method == "POST":
        rollno = request.form['roll']
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        mail = request.form['mail']
        address = request.form['address']
        pincode = request.form['pincode']
        gender = request.form['gender']
        stream = request.form['stream']
        dob = request.form['dob']
        print(dob)
        cur = myconn.cursor()
        cur.execute("""select * from students where rollno=%s""", (rollno,))
        data = cur.fetchall()
        if len(data) == 0:
            flash("Registered Successfully")
            cur.execute("""insert into students(rollno, firstname, lastname, phone, mail, address, pincode, gender, stream, dateofbirth, dateofadmission) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (rollno, fname, lname, phone, mail,
                        address, pincode, gender, stream, dob, date.today()))
            myconn.commit()
            return render_template('add.html')
        else:
            print("No")
            flash("Already Exists")
            return render_template('add.html')
    return render_template("add.html")


@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        dele = request.form['delete']
        cur = myconn.cursor()
        cur.execute("delete from students where rollno=%s", (dele,))
        myconn.commit()
        flash("Deleted Successfully")
        return render_template('home.html', data=data)
    cur = myconn.cursor()
    cur.execute("select * from students")
    data = cur.fetchall()
    print(data)
    return render_template('home.html', data=data)


# @app.route("/edit", methods=["POST", "GET"])
# def edit():
#     roll = request.form['edit']
#     cur = myconn.cursor()
#     cur.execute("select * from students where rollno=%s", (roll,))
#     data = cur.fetchall()
#     streams = ["Computer Science", "Information Technology",
#                "EXTC", "Civil", "Mechanical"]
#     genders = ["Male", "Female", "Others"]
#     address = data[0][5].split(" ")
#     print(address)
#     return render_template('edit.html', data=data, streams=streams, genders=genders, address=address)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    session["loggedin"] = False
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
