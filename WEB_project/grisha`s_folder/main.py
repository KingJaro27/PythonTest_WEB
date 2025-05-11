from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from tester import TestingSystem, TestCase
import os

app = Flask(__name__)
app.secret_key = "9515d755178ad60074008112b4f06acf74e810389559766c047f53f189718679"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Database Models
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    progress = db.relationship("UserProgress", backref="user", lazy=True)


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    solution = db.Column(db.Text, nullable=False)
    test_cases = db.relationship("TestCase", backref="task", lazy=True)
    user_progress = db.relationship("UserProgress", backref="task", lazy=True)


class TestCase(db.Model):
    __tablename__ = "test_cases"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)
    input = db.Column(db.Text, nullable=False)
    output = db.Column(db.Text, nullable=False)


class UserProgress(db.Model):
    __tablename__ = "user_progress"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), primary_key=True)
    completed = db.Column(db.Boolean, default=False)
    completion_date = db.Column(db.DateTime)


# Create tables and sample data
def init_db():
    with app.app_context():
        db.create_all()

        if Task.query.count() == 0:
            sample_tasks = [
                {
                    "title": "Sum Two Numbers",
                    "description": "Write a function that takes two numbers from input and returns their sum.",
                    "difficulty": "Easy",
                    "solution": "def sum_numbers(a, b):\n    return a + b",
                    "test_cases": [
                        {"input": "2, 3", "output": "5"},
                        {"input": "10, -5", "output": "5"},
                    ],
                },
                {
                    "title": "Factorial Calculator",
                    "description": "Write a function that calculates the factorial of a number.",
                    "difficulty": "Medium",
                    "solution": "def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)",
                    "test_cases": [
                        {"input": "5", "output": "120"},
                        {"input": "0", "output": "1"},
                    ],
                },
                {
                    "title": "Prime Number Checker",
                    "description": "Write a function that checks if a number is prime.",
                    "difficulty": "Hard",
                    "solution": "def is_prime(n):\n    if n <= 1:\n        return False\n    for i in range(2, int(n**0.5)+1):\n        if n % i == 0:\n            return False\n    return True",
                    "test_cases": [
                        {"input": "7", "output": "True"},
                        {"input": "4", "output": "False"},
                    ],
                },
            ]

            for task_data in sample_tasks:
                task = Task(
                    title=task_data["title"],
                    description=task_data["description"],
                    difficulty=task_data["difficulty"],
                    solution=task_data["solution"],
                )
                db.session.add(task)
                db.session.flush()  # To get the task.id

                for case in task_data["test_cases"]:
                    test_case = TestCase(
                        task_id=task.id, input=case["input"], output=case["output"]
                    )
                    db.session.add(test_case)

            db.session.commit()


if not os.path.exists("instance/database.db"):
    init_db()


@app.route("/")
def index():
    tasks = Task.query.all()
    completed_tasks = []
    if "user_id" in session:
        completed_progress = UserProgress.query.filter_by(
            user_id=session["user_id"], completed=True
        ).all()
        completed_tasks = [progress.task_id for progress in completed_progress]
    return render_template(
        "index.html",
        logged_in="user_id" in session,
        username=session.get("username"),
        tasks=tasks,
        completed_tasks=completed_tasks,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form.get("email", "")
        if User.query.filter_by(username=username).first():
            flash("Username already taken", "danger")
            return redirect(url_for("register"))
        try:
            new_user = User(
                username=username,
                password_hash=generate_password_hash(password),
                email=email,
            )
            db.session.add(new_user)
            db.session.flush()  # To get the new_user.id
            # Initialize progress for all tasks
            tasks = Task.query.all()
            for task in tasks:
                progress = UserProgress(user_id=new_user.id, task_id=task.id)
                db.session.add(progress)
            db.session.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred during registration", "danger")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["username"] = user.username
            flash("Logged in successfully!", "success")
            return redirect(url_for("index"))

        flash("Invalid username or password", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    flash("Logged out successfully", "info")
    return redirect(url_for("index"))


@app.route("/profile")
def profile():
    if "user_id" not in session:
        flash("Please login to view your profile", "danger")
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    if not user:
        flash("User not found", "danger")
        return redirect(url_for("index"))

    total_tasks = Task.query.count()
    completed_tasks = UserProgress.query.filter_by(
        user_id=session["user_id"], completed=True
    ).count()

    recent_tasks = (
        db.session.query(
            Task.id, Task.title, Task.difficulty, UserProgress.completion_date
        )
        .join(UserProgress, Task.id == UserProgress.task_id)
        .filter(
            UserProgress.user_id == session["user_id"], UserProgress.completed == True
        )
        .order_by(UserProgress.completion_date.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "profile.html",
        user=user,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        recent_tasks=recent_tasks,
        logged_in=True,
        username=session.get("username"),
    )


@app.route("/task/<int:task_id>")
def view_task(task_id):
    task = Task.query.get_or_404(task_id)
    test_cases = TestCase.query.filter_by(task_id=task_id).all()

    completed = False
    if "user_id" in session:
        progress = UserProgress.query.filter_by(
            user_id=session["user_id"], task_id=task_id
        ).first()
        completed = progress.completed if progress else False

    return render_template(
        "task.html",
        task=task,
        test_cases=test_cases,
        logged_in="user_id" in session,
        completed=completed,
    )


@app.route("/submit_solution/<int:task_id>", methods=["POST"])
def submit_solution(task_id):
    if "user_id" not in session:
        flash("Please login to submit solutions", "danger")
        return redirect(url_for("login"))

    task = Task.query.get_or_404(task_id)
    test_cases = TestCase.query.filter_by(task_id=task_id).all()

    user_code = request.form["code"]
    temp_file = f"user_solution_{session['user_id']}.py"
    with open(temp_file, "w") as f:
        f.write(user_code)

    tester = TestingSystem()
    for case in test_cases:
        tester.add_test_case(case.input, case.output)

    all_passed = tester.run_tests(temp_file)
    os.remove(temp_file)

    if all_passed:
        progress = UserProgress.query.filter_by(
            user_id=session["user_id"], task_id=task_id
        ).first()

        if progress:
            progress.completed = True
            progress.completion_date = datetime.utcnow()
            db.session.commit()

        flash("All tests passed! Solution accepted.", "success")
    else:
        flash("Some tests failed. Check your solution.", "danger")

    return redirect(url_for("view_task", task_id=task_id))


if __name__ == "__main__":
    app.run(debug=True)
