from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from tester import TestingSystem, TestCase

app = Flask(__name__)
app.secret_key = "9515d755178ad60074008112b4f06acf74e810389559766c047f53f189718679"
app.config["DATABASE"] = "database.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(app.config["DATABASE"])
        db.row_factory = sqlite3.Row
    return db


def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                solution TEXT NOT NULL
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS test_cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                input TEXT NOT NULL,
                output TEXT NOT NULL,
                FOREIGN KEY(task_id) REFERENCES tasks(id)
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_progress (
                user_id INTEGER,
                task_id INTEGER,
                completed BOOLEAN DEFAULT 0,
                completion_date TIMESTAMP,
                PRIMARY KEY(user_id, task_id),
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(task_id) REFERENCES tasks(id)
            )
        """
        )

        cursor.execute("SELECT COUNT(*) FROM tasks")
        if cursor.fetchone()[0] == 0:
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

            for task in sample_tasks:
                cursor.execute(
                    "INSERT INTO tasks (title, description, difficulty, solution) VALUES (?, ?, ?, ?)",
                    (
                        task["title"],
                        task["description"],
                        task["difficulty"],
                        task["solution"],
                    ),
                )
                task_id = cursor.lastrowid

                for case in task["test_cases"]:
                    cursor.execute(
                        "INSERT INTO test_cases (task_id, input, output) VALUES (?, ?, ?)",
                        (task_id, case["input"], case["output"]),
                    )

        db.commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


if not os.path.exists(app.config["DATABASE"]):
    init_db()


@app.route("/")
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = [dict(row) for row in cursor.fetchall()]

    completed_tasks = []
    if "user_id" in session:
        cursor.execute(
            "SELECT task_id FROM user_progress WHERE user_id = ? AND completed = 1",
            (session["user_id"],),
        )
        completed_tasks = [row["task_id"] for row in cursor.fetchall()]

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

        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                (username, generate_password_hash(password), email),
            )
            db.commit()

            cursor.execute("SELECT id FROM tasks")
            task_ids = [row[0] for row in cursor.fetchall()]

            for task_id in task_ids:
                cursor.execute(
                    "INSERT INTO user_progress (user_id, task_id) VALUES (?, ?)",
                    (cursor.lastrowid, task_id),
                )
            db.commit()

            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already taken", "danger")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
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

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],))
    user = cursor.fetchone()

    if not user:
        flash("User not found", "danger")
        return redirect(url_for("index"))

    cursor.execute("SELECT COUNT(*) as total_tasks FROM tasks")
    total_tasks = cursor.fetchone()["total_tasks"]

    cursor.execute(
        """
        SELECT COUNT(*) as completed_tasks FROM user_progress
        WHERE user_id = ? AND completed = 1
    """,
        (session["user_id"],),
    )
    completed_tasks = cursor.fetchone()["completed_tasks"]

    cursor.execute(
        """
        SELECT t.id, t.title, t.difficulty, up.completion_date
        FROM tasks t
        JOIN user_progress up ON t.id = up.task_id
        WHERE up.user_id = ? AND up.completed = 1
        ORDER BY up.completion_date DESC
        LIMIT 5
    """,
        (session["user_id"],),
    )
    recent_tasks = cursor.fetchall()

    return render_template(
        "profile.html",
        user=dict(user),
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        recent_tasks=recent_tasks,
        logged_in=True,
        username=session.get("username"),
    )


@app.route("/task/<int:task_id>")
def view_task(task_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

    if not task:
        flash("Task not found", "danger")
        return redirect(url_for("index"))

    cursor.execute("SELECT * FROM test_cases WHERE task_id = ?", (task_id,))
    test_cases = cursor.fetchall()

    completed = False
    if "user_id" in session:
        cursor.execute(
            """
            SELECT completed FROM user_progress
            WHERE user_id = ? AND task_id = ?
        """,
            (session["user_id"], task_id),
        )
        progress = cursor.fetchone()
        completed = progress["completed"] if progress else False

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

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

    if not task:
        flash("Task not found", "danger")
        return redirect(url_for("index"))


    cursor.execute("SELECT * FROM test_cases WHERE task_id = ?", (task_id,))
    test_cases = cursor.fetchall()

    user_code = request.form["code"]
    temp_file = f"user_solution_{session['user_id']}.py"
    with open(temp_file, "w") as f:
        f.write(user_code)

    tester = TestingSystem()
    for case in test_cases:
        tester.add_test_case(case["input"], case["output"])

    all_passed = tester.run_tests(temp_file)

    os.remove(temp_file)

    if all_passed:
        # Обновляем прогресс пользователя
        cursor.execute(
            """
            UPDATE user_progress
            SET completed = 1, completion_date = CURRENT_TIMESTAMP
            WHERE user_id = ? AND task_id = ?
            """,
            (session["user_id"], task_id),
        )
        db.commit()
        flash("All tests passed! Solution accepted.", "success")
    else:
        flash("Some tests failed. Check your solution.", "danger")

    return redirect(url_for("view_task", task_id=task_id))


if __name__ == "__main__":
    app.run(debug=True)
