from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from tester import PythonTester, TestCase
import os
import tempfile

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


def init_db():
    with app.app_context():
        db.create_all()

        if Task.query.count() == 0:
            sample_tasks = [
                # ======== EASY TASKS ========
                {
                    "title": "Sum Two Numbers",
                    "description": "Write a function that takes two numbers from input and returns their sum.",
                    "difficulty": "Easy",
                    "test_cases": [
                        {"input": "2, 3", "output": "5"},
                        {"input": "10, -5", "output": "5"},
                    ],
                },
                {
                    "title": "Even or Odd",
                    "description": "Write a function that takes a number and returns 'Even' if the number is even, 'Odd' otherwise.",
                    "difficulty": "Easy",
                    "test_cases": [
                        {"input": "4", "output": "Even"},
                        {"input": "7", "output": "Odd"},
                        {"input": "0", "output": "Even"},
                    ],
                },
                {
                    "title": "Reverse String",
                    "description": "Write a function that reverses a string.",
                    "difficulty": "Easy",
                    "test_cases": [
                        {"input": "'hello'", "output": "olleh"},
                        {"input": "'Python'", "output": "nohtyP"},
                        {"input": "''", "output": ""},
                    ],
                },
                {
                    "title": "Count Vowels",
                    "description": "Write a function that counts the number of vowels in a string (a, e, i, o, u).",
                    "difficulty": "Easy",
                    "test_cases": [
                        {"input": "'hello'", "output": "2"},
                        {"input": "'Python is awesome'", "output": "6"},
                        {"input": "'xyz'", "output": "0"},
                    ],
                },
                {
                    "title": "Find Maximum",
                    "description": "Write a function that takes three numbers and returns the largest one.",
                    "difficulty": "Easy",
                    "test_cases": [
                        {"input": "1, 2, 3", "output": "3"},
                        {"input": "-5, -1, -10", "output": "-1"},
                        {"input": "0, 0, 0", "output": "0"},
                    ],
                },
                {
                    "title": "Calculate Average",
                    "description": "Write a function that calculates the average of a list of numbers.",
                    "difficulty": "Easy",
                    "test_cases": [
                        {"input": "[1, 2, 3, 4, 5]", "output": "3.0"},
                        {"input": "[10, 20, 30]", "output": "20.0"},
                        {"input": "[-1, 0, 1]", "output": "0.0"},
                    ],
                },
                # ======== MEDIUM TASKS ========
                {
                    "title": "Factorial Calculator",
                    "description": "Write a function that calculates the factorial of a number.",
                    "difficulty": "Medium",
                    "test_cases": [
                        {"input": "5", "output": "120"},
                        {"input": "0", "output": "1"},
                        {"input": "10", "output": "3628800"},
                    ],
                },
                {
                    "title": "Prime Number Checker",
                    "description": "Write a function that checks if a number is prime.",
                    "difficulty": "Medium",
                    "test_cases": [
                        {"input": "7", "output": "True"},
                        {"input": "4", "output": "False"},
                        {"input": "1", "output": "False"},
                    ],
                },
                {
                    "title": "Fibonacci Sequence",
                    "description": "Write a function that returns the nth Fibonacci number.",
                    "difficulty": "Medium",
                    "test_cases": [
                        {"input": "0", "output": "0"},
                        {"input": "1", "output": "1"},
                        {"input": "10", "output": "55"},
                    ],
                },
                {
                    "title": "Palindrome Checker",
                    "description": "Write a function that checks if a string is a palindrome (reads the same backward as forward).",
                    "difficulty": "Medium",
                    "test_cases": [
                        {"input": "'racecar'", "output": "True"},
                        {"input": "'hello'", "output": "False"},
                        {"input": "'A man a plan a canal Panama'", "output": "True"},
                    ],
                },
                {
                    "title": "Anagram Checker",
                    "description": "Write a function that checks if two strings are anagrams of each other.",
                    "difficulty": "Medium",
                    "test_cases": [
                        {"input": "'listen', 'silent'", "output": "True"},
                        {"input": "'hello', 'world'", "output": "False"},
                        {
                            "input": "'Tom Marvolo Riddle', 'I am Lord Voldemort'",
                            "output": "True",
                        },
                    ],
                },
                {
                    "title": "List Intersection",
                    "description": "Write a function that returns the intersection of two lists (common elements).",
                    "difficulty": "Medium",
                    "test_cases": [
                        {"input": "[1, 2, 3], [2, 3, 4]", "output": "[2, 3]"},
                        {"input": "['a', 'b', 'c'], ['x', 'y', 'z']", "output": "[]"},
                        {"input": "[1, 1, 2, 3], [1, 1, 1, 4]", "output": "[1]"},
                    ],
                },
                # ======== HARD TASKS ========
                {
                    "title": "Binary Search",
                    "description": "Implement the binary search algorithm to find an element in a sorted list.",
                    "difficulty": "Hard",
                    "test_cases": [
                        {"input": "[1, 3, 5, 7, 9], 5", "output": "2"},
                        {"input": "[1, 3, 5, 7, 9], 2", "output": "-1"},
                        {"input": "[], 1", "output": "-1"},
                    ],
                },
                {
                    "title": "Merge Two Sorted Lists",
                    "description": "Write a function that merges two sorted lists into one sorted list.",
                    "difficulty": "Hard",
                    "test_cases": [
                        {
                            "input": "[1, 3, 5], [2, 4, 6]",
                            "output": "[1, 2, 3, 4, 5, 6]",
                        },
                        {"input": "[], [1, 2, 3]", "output": "[1, 2, 3]"},
                        {
                            "input": "[5, 6, 7], [1, 2, 3]",
                            "output": "[1, 2, 3, 5, 6, 7]",
                        },
                    ],
                },
                {
                    "title": "Valid Parentheses",
                    "description": "Write a function that checks if a string of parentheses is balanced.",
                    "difficulty": "Hard",
                    "test_cases": [
                        {"input": "'()[]{}'", "output": "True"},
                        {"input": "'(]'", "output": "False"},
                        {"input": "'([{}])'", "output": "True"},
                    ],
                },
                {
                    "title": "Longest Substring Without Repeating Characters",
                    "description": "Find the length of the longest substring without repeating characters.",
                    "difficulty": "Hard",
                    "test_cases": [
                        {"input": "'abcabcbb'", "output": "3"},
                        {"input": "'bbbbb'", "output": "1"},
                        {"input": "'pwwkew'", "output": "3"},
                    ],
                },
                {
                    "title": "Matrix Rotation",
                    "description": "Rotate an N x N matrix 90 degrees clockwise.",
                    "difficulty": "Hard",
                    "test_cases": [
                        {
                            "input": "[[1,2,3],[4,5,6],[7,8,9]]",
                            "output": "[[7, 4, 1], [8, 5, 2], [9, 6, 3]]",
                        },
                        {"input": "[[1]]", "output": "[[1]]"},
                        {"input": "[[1,2],[3,4]]", "output": "[[3, 1], [4, 2]]"},
                    ],
                },
                {
                    "title": "Word Break",
                    "description": "Given a string and a dictionary of words, determine if the string can be segmented into space-separated words from the dictionary.",
                    "difficulty": "Hard",
                    "test_cases": [
                        {"input": "'leetcode', ['leet', 'code']", "output": "True"},
                        {
                            "input": "'applepenapple', ['apple', 'pen']",
                            "output": "True",
                        },
                        {
                            "input": "'catsandog', ['cats', 'dog', 'sand', 'and', 'cat']",
                            "output": "False",
                        },
                    ],
                },
            ]

            for task_data in sample_tasks:
                task = Task(
                    title=task_data["title"],
                    description=task_data["description"],
                    difficulty=task_data["difficulty"],
                )
                db.session.add(task)
                db.session.flush()  # To get the task.id

                for case in task_data["test_cases"]:
                    test_case = TestCase(
                        task_id=task.id, input=case["input"], output=case["output"]
                    )
                    db.session.add(test_case)

            db.session.commit()


init_db()


@app.route("/")
def index():
    difficulty = request.args.get("difficulty", None)

    # Base query
    query = Task.query

    # Filter by difficulty if specified
    if difficulty in ["Easy", "Medium", "Hard"]:
        query = query.filter_by(difficulty=difficulty)

    tasks = query.all()

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
        current_difficulty=difficulty,  # Pass the current filter to template
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

@app.route("/completed")
def completed_tasks():
    difficulty = request.args.get('difficulty', None)
    
    if "user_id" not in session:
        flash("Please login to view completed tasks", "danger")
        return redirect(url_for("login"))
    
    # Base query for completed tasks
    query = db.session.query(Task).join(UserProgress).filter(
        UserProgress.user_id == session["user_id"],
        UserProgress.completed == True
    )
    
    # Filter by difficulty if specified
    if difficulty in ['Easy', 'Medium', 'Hard']:
        query = query.filter(Task.difficulty == difficulty)
    
    tasks = query.all()
    
    return render_template(
        "completed.html",
        logged_in=True,
        username=session.get("username"),
        tasks=tasks,
        current_difficulty=difficulty
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

    # Initialize tester and add test cases
    tester = PythonTester()
    for case in test_cases:
        tester.add_test_case(case.input, case.output)

    # Check if a file was uploaded
    if "pythonFile" in request.files:
        file = request.files["pythonFile"]
        if file and file.filename.endswith(".py"):
            # Save the file temporarily
            temp_path = os.path.join(tempfile.gettempdir(), file.filename)
            file.save(temp_path)

            # Read the file content
            with open(temp_path, "r") as f:
                user_code = f.read()

            # Clean up
            os.remove(temp_path)
        else:
            flash("Please upload a valid Python (.py) file", "danger")
            return redirect(url_for("view_task", task_id=task_id))
    else:
        # Get code from textarea
        user_code = request.form["code"]

    # Test the code
    all_passed = tester.test_python_code(user_code)
    test_results = tester.get_test_results()

    if all_passed:
        # Update user progress if all tests passed
        progress = UserProgress.query.filter_by(
            user_id=session["user_id"], task_id=task_id
        ).first()

        if progress and not progress.completed:
            progress.completed = True
            progress.completion_date = datetime.utcnow()
            db.session.commit()

        flash("All tests passed! Solution accepted.", "success")
    else:
        error_messages = []
        for result in test_results:
            if result["status"] != "Passed":
                msg = f"Test Case {result['test_case']} {result['status']}:\n"
                msg += f"Input: {result['input']}\n"
                msg += f"Expected: {result['expected']}\n"
                if result["status"] == "Error":
                    msg += f"Error: {result['actual']}"
                else:
                    msg += f"Got: {result['actual']}"
                error_messages.append(msg)

        flash("\n\n".join(error_messages), "danger")

    return redirect(url_for("view_task", task_id=task_id))


if __name__ == "__main__":
    app.run(debug=True)
