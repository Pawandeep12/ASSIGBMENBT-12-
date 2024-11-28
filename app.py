from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from models import db, Student, Quiz, Result

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'

db.init_app(app)


@app.route("/")
def home():
    return render_template("home.html")


# Add Student
@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        if Student.query.filter_by(email=email).first():
            flash("Student with this email already exists!")
        else:
            student = Student(name=name, email=email)
            db.session.add(student)
            db.session.commit()
            flash("Student added successfully!")
        return redirect(url_for("add_student"))
    return render_template("add_student.html")


# Add Quiz
@app.route("/add_quiz", methods=["GET", "POST"])
def add_quiz():
    if request.method == "POST":
        title = request.form["title"]
        date = request.form["date"]
        quiz = Quiz(title=title, date=datetime.strptime(date, "%Y-%m-%d"))
        db.session.add(quiz)
        db.session.commit()
        flash("Quiz added successfully!")
        return redirect(url_for("add_quiz"))
    return render_template("add_quiz.html")


# Add Quiz Result
@app.route("/add_result", methods=["GET", "POST"])
def add_result():
    students = Student.query.all()
    quizzes = Quiz.query.all()

    if request.method == "POST":
        student_id = request.form["student_id"]
        quiz_id = request.form["quiz_id"]
        score = request.form["score"]

        result = Result(student_id=student_id, quiz_id=quiz_id, score=score)
        db.session.add(result)
        db.session.commit()
        flash("Result added successfully!")
        return redirect(url_for("add_result"))

    return render_template("add_result.html", students=students, quizzes=quizzes)


# View Students
@app.route("/view_students")
def view_students():
    students = Student.query.all()
    return render_template("view_students.html", students=students)


# View Quizzes
@app.route("/view_quizzes")
def view_quizzes():
    quizzes = Quiz.query.all()
    return render_template("view_quizzes.html", quizzes=quizzes)


# View Results
@app.route("/view_results")
def view_results():
    results = Result.query.all()
    return render_template("view_results.html", results=results)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
