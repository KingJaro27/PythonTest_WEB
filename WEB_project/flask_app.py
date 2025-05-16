from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from tester import PythonTester, TestCase

username = "K1ngPython"
hostname = "K1ngPython.mysql.pythonanywhere-services.com"
databasename = "K1ngPython$database_web"
password = "j7GN_6kk£88."


app = Flask(__name__)
app.secret_key = "9515d755178ad60074008112b4f06acf74e810389559766c047f53f189718679"
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqldb://{username}:{password}@{hostname}/{databasename}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120))
    last_login = db.Column(db.DateTime)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    progress = db.relationship("UserProgress", backref="user", lazy=True)
    logo_color = db.Column(db.String(7), default='#FFD700')


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

class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    code = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    passed = db.Column(db.Boolean, nullable=False)
    execution_time = db.Column(db.Float)
    test_results = db.Column(db.Text)

def init_db():
    with app.app_context():
        db.create_all()

        if Task.query.count() == 0:
            sample_tasks = [
                #EASY TASKS
                {
                    "title": "Sum Two Numbers",
                    "description": "Write a function that takes two numbers from input and returns their sum.",
                    "difficulty": "Easy",
                    "test_cases": [
                        {"input": "2 3", "output": "5"},
                        {"input": "10 -5", "output": "5"},
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
                        {"input": "hello", "output": "olleh"},
                        {"input": "Python", "output": "nohtyP"},
                        {"input": "a", "output": "a"},
                    ],
                },
                {
                    "title": "Count Vowels",
                    "description": "Write a function that counts the number of vowels in a string (a, e, i, o, u).",
                    "difficulty": "Easy",
                    "test_cases": [
                        {"input": "hello", "output": "2"},
                        {"input": "Python is awesome", "output": "6"},
                        {"input": "xyz", "output": "0"},
                    ],
                },
                {
                    "title": "Find Maximum",
                    "description": "Write a function that takes three numbers and returns the largest one.",
                    "difficulty": "Easy",
                    "test_cases": [
                        {"input": "1 2 3", "output": "3"},
                        {"input": "-5 -1 -10", "output": "-1"},
                        {"input": "0 0 0", "output": "0"},
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
                {
                    "title": "Count Words in String",
                    "description": "Write a function that counts the number of words in a given string. A word is defined as a sequence of non-space characters.",
                    "difficulty": "Easy",
                    "test_cases": [
                        {"input": "Hello world", "output": "2"},
                        {"input": "This is a test", "output": "4"}
                    ]
                },
                {
                    "title": "Find Minimum Number",
                    "description": "Write a function that takes a list of numbers and returns the smallest number in the list.",
                    "difficulty": "Easy",
                    "test_cases": [
                        {"input": "[4, 2, 9, 7]", "output": "2"},
                        {"input": "[-5, -1, -10]", "output": "-10"},
                        {"input": "[5]", "output": "5"}
                    ]
                },
                {
                    "title": "Check Palindrome Number",
                    "description": "Write a function that checks if a number is a palindrome (reads the same backward as forward).",
                    "difficulty": "Easy",
                    "test_cases": [
                        {"input": "121", "output": "True"},
                        {"input": "123", "output": "False"},
                        {"input": "5", "output": "True"}
                    ]
                },
                #MEDIUM TASKS
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
                        {"input": "racecar", "output": "True"},
                        {"input": "hello", "output": "False"},
                        {"input": "A man a plan a canal Panama", "output": "True"},
                    ],
                },
                {
                    "title": "Anagram Checker",
                    "description": "Write a function that checks if two strings are anagrams of each other.",
                    "difficulty": "Medium",
                    "test_cases": [
                        {"input": "listen, silent", "output": "True"},
                        {"input": "hello, world", "output": "False"},
                        {
                            "input": "Tom Marvolo Riddle, I am Lord Voldemort",
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
                {
                    "title": "Roman to Integer",
                    "description": "Convert a Roman numeral to an integer. Values range from 1 to 3999.",
                    "difficulty": "Medium",
                    "test_cases": [
                        {"input": "III", "output": "3"},
                        {"input": "LVIII", "output": "58"},
                        {"input": "MCMXCIV", "output": "1994"}
                    ]
                },
                {
                    "title": "Group Anagrams",
                    "description": "Given a list of strings, group anagrams together. An anagram is a word formed by rearranging letters of another.",
                    "difficulty": "Medium",
                    "test_cases": [
                        {"input": "['eat','tea','tan','ate','nat','bat']", "output": "[['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]"},
                        {"input": "['']", "output": "[['']]"},
                        {"input": "['a']", "output": "[['a']]"}
                    ]
                },
                {
                    "title": "Binary Tree Level Order Traversal",
                    "description": "Given the root of a binary tree, return the level order traversal of its nodes' values (from left to right, level by level). Represent the tree as a list where None indicates no node.",
                    "difficulty": "Medium",
                    "test_cases": [
                        {"input": "[3,9,20,None,None,15,7]", "output": "[[3], [9, 20], [15, 7]]"},
                        {"input": "[1]", "output": "[[1]]"},
                        {"input": "[]", "output": "[]"}
                    ]
                },
                #HARD TASKS
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
                        {"input": "()[]{}", "output": "True"},
                        {"input": "(]", "output": "False"},
                        {"input": "([{}])", "output": "True"},
                    ],
                },
                {
                    "title": "Longest Substring Without Repeating Characters",
                    "description": "Find the length of the longest substring without repeating characters.",
                    "difficulty": "Hard",
                    "test_cases": [
                        {"input": "abcabcbb", "output": "3"},
                        {"input": "bbbbb", "output": "1"},
                        {"input": "pwwkew", "output": "3"},
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
                        {"input": "leetcode, ['leet', 'code']", "output": "True"},
                        {
                            "input": "applepenapple, ['apple', 'pen']",
                            "output": "True",
                        },
                        {
                            "input": "catsandog, ['cats', 'dog', 'sand', 'and', 'cat']",
                            "output": "False",
                        },
                    ],
                },
                {
                    "title": "Matrix Diagonal Sum",
                    "description": "Calculate the sum of both diagonals in an N×N matrix. Input format: First line - size N, next N lines - space-separated numbers for each row.",
                    "difficulty": "Hard",
                    "test_cases": [
                        {"input": "3\n1 2 3\n4 5 6\n7 8 9", "output": "25"},
                        {"input": "2\n1 1\n1 1", "output": "4"}
                    ]
                },
                {
                    "title": "Word Frequency Counter",
                    "description": "Count how many times each word appears in text (case-insensitive). Input format: First line - number of sentences, following lines - sentences.",
                    "difficulty": "Hard",
                    "test_cases": [
                        {"input": "2\nHello world\nWorld says hello", "output": "hello: 2\nworld: 2\nsays: 1"},
                        {"input": "1\na a a b", "output": "a: 3\nb: 1"}
                    ]
                },
                {
                    "title": "Binary Converter",
                    "description": "Convert numbers to binary, concatenate, and count 1s. Input format: First line - count N, next line - space-separated numbers.",
                    "difficulty": "Hard",
                    "test_cases": [
                        {"input": "3\n5 10 15", "output": "8"},
                        {"input": "2\n0 1", "output": "1"}
                    ]
                },
                #Beserk tasks
                {
                    "title": "Unique Differences Calculator",
                    "description": "Given a set of numbers, find all unique pairwise differences (including each number minus itself) sorted in ascending order. Input format: First line - count N, next N lines - numbers.",
                    "difficulty": "Beserk",
                    "test_cases": [
                        {"input": "3\n-1\n3\n7", "output": "-8\n-4\n0\n4\n8"},
                        {"input": "2\n5\n10", "output": "-5\n0\n5"}
                    ]
                },
                {
                    "title": "Fraction Sum Simplifier",
                    "description": "Calculate the sum of fractions and return as an irreducible fraction (a/b format). Input format: First line - count N, then N pairs of numerator/denominator.",
                    "difficulty": "Beserk",
                    "test_cases": [
                        {"input": "3\n1\n60\n1\n30\n1\n100", "output": "3/50"},
                        {"input": "2\n1\n4\n3\n8", "output": "5/8"}
                    ]
                },
                {
                    "title": "Prime Number Generator",
                    "description": "Generate all prime numbers between two given numbers (inclusive). Input format: Two space-separated numbers a and b (a ≤ b).",
                    "difficulty": "Beserk",
                    "test_cases": [
                        {"input": "10 20", "output": "11 13 17 19"},
                        {"input": "1 5", "output": "2 3 5"}
                    ]
                },
                {
                    "title": "Trapping Rain Water",
                    "description": "Given an array representing elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
                    "difficulty": "Beserk",
                    "test_cases": [
                        {"input": "[0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6"},
                        {"input": "[4,2,0,3,2,5]", "output": "9"},
                        {"input": "[4,2,3]", "output": "1"}
                    ]
                },
                {
                    "title": "Sliding Window Maximum",
                    "description": "Given an array of integers and a window size k, find the maximum in each sliding window as it moves from left to right.",
                    "difficulty": "Beserk",
                    "test_cases": [
                        {"input": "[1,3,-1,-3,5,3,6,7], 3", "output": "[3, 3, 5, 5, 6, 7]"},
                        {"input": "[1], 1", "output": "[1]"},
                        {"input": "[9,11], 2", "output": "[11]"}
                    ]
                },
                {
                    "title": "Minimum Window Substring",
                    "description": "Given two strings s and t, return the minimum window in s which will contain all characters in t.",
                    "difficulty": "Beserk",
                    "test_cases": [
                        {"input": "ADOBECODEBANC, ABC", "output": "BANC"},
                        {"input": "a, a", "output": "a"},
                        {"input": "a, aa", "output": ""}
                    ]
                },

            ]

            for task_data in sample_tasks:
                task = Task(
                    title=task_data["title"],
                    description=task_data["description"],
                    difficulty=task_data["difficulty"],
                )
                db.session.add(task)
                db.session.flush()

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
    query = Task.query
    completed_task_ids = []
    if "user_id" in session:
        completed_progress = UserProgress.query.filter_by(
            user_id=session["user_id"],
            completed=True
        ).all()
        completed_task_ids = [progress.task_id for progress in completed_progress]

    beserk_unlocked = False
    if "user_id" in session:
        total_completed = len(completed_task_ids)
        hard_completed = UserProgress.query.join(Task).filter(
            UserProgress.user_id == session["user_id"],
            UserProgress.completed == True,
            Task.difficulty == 'Hard'
        ).count()
        beserk_unlocked = total_completed >= 10 and hard_completed >= 3

    if difficulty == 'Beserk':
        query = query.filter_by(difficulty='Beserk')
    elif difficulty in ['Easy', 'Medium', 'Hard']:
        query = query.filter_by(difficulty=difficulty)

    tasks = query.all()

    return render_template(
        "index.html",
        tasks=tasks,
        completed_tasks=completed_task_ids,
        beserk_unlocked=beserk_unlocked,
        current_difficulty=difficulty,
        logged_in="user_id" in session,
        username=session.get("username")
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
            db.session.flush()
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

            user.last_login = datetime.utcnow()
            db.session.commit()

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

@app.route('/toggle_theme', methods=['POST'])
def toggle_theme():
    current_theme = session.get('theme', 'light')
    session['theme'] = 'dark' if current_theme == 'light' else 'light'
    return redirect(request.referrer or url_for('index'))

@app.route('/update_logo_color', methods=['POST'])
def update_logo_color():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 403

    user = User.query.get(session['user_id'])
    user.logo_color = request.json.get('color', '#FFD700')
    db.session.commit()
    return jsonify({'success': True})

@app.route("/profile")
def profile():
    if "user_id" not in session:
        flash("Please login to view your profile", "danger")
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    difficulties = ['Easy', 'Medium', 'Hard', 'Beserk']
    counts = {}

    for diff in difficulties:
        counts[f'total_{diff.lower()}'] = Task.query.filter_by(difficulty=diff).count()
        counts[f'completed_{diff.lower()}'] = UserProgress.query.join(Task).filter(
            UserProgress.user_id == session["user_id"],
            UserProgress.completed == True,
            Task.difficulty == diff
        ).count()

    recent_tasks = db.session.query(Task, UserProgress.completion_date).join(
        UserProgress, UserProgress.task_id == Task.id
    ).filter(
        UserProgress.user_id == session["user_id"],
        UserProgress.completed == True
    ).order_by(
        UserProgress.completion_date.desc()
    ).limit(5).all()

    total_easy = Task.query.filter_by(difficulty='Easy').count()
    total_medium = Task.query.filter_by(difficulty='Medium').count()
    total_hard = Task.query.filter_by(difficulty='Hard').count()
    total_beserk = Task.query.filter_by(difficulty='Beserk').count()

    completed_easy = UserProgress.query.join(Task).filter(
        UserProgress.user_id == session["user_id"],
        UserProgress.completed == True,
        Task.difficulty == 'Easy'
    ).count()

    completed_medium = UserProgress.query.join(Task).filter(
        UserProgress.user_id == session["user_id"],
        UserProgress.completed == True,
        Task.difficulty == 'Medium'
    ).count()


    completed_hard = UserProgress.query.join(Task).filter(
        UserProgress.user_id == session["user_id"],
        UserProgress.completed == True,
        Task.difficulty == 'Hard'
    ).count()

    completed_beserk = UserProgress.query.join(Task).filter(
        UserProgress.user_id == session["user_id"],
        UserProgress.completed == True,
        Task.difficulty == 'Beserk'
    ).count()

    total_completed = sum(counts[f'completed_{diff.lower()}'] for diff in difficulties)
    hard_completed = counts['completed_hard']
    beserk_unlocked = total_completed >= 10 and hard_completed >= 3
    total_tasks = total_easy + total_medium + total_hard + total_beserk
    completed_tasks = completed_easy + completed_medium + completed_hard + completed_beserk

    return render_template(
        "profile.html",
        user=user,
        recent_tasks=recent_tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        beserk_unlocked=beserk_unlocked,
        logged_in=True,
        username=session.get("username"),
        **counts
    )

@app.route("/completed")
def completed_tasks():
    difficulty = request.args.get('difficulty', None)

    if "user_id" not in session:
        flash("Please login to view completed tasks", "danger")
        return redirect(url_for("login"))

    query = db.session.query(Task).join(UserProgress).filter(
        UserProgress.user_id == session["user_id"],
        UserProgress.completed == True
    )

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
    submissions = []
    test_cases = TestCase.query.filter_by(task_id=task_id).all()
    completed = False
    test_results = None  # Add this line

    if "user_id" in session:
        # Get latest submission
        submissions = Submission.query.filter_by(
            user_id=session["user_id"],
            task_id=task_id
        ).order_by(Submission.timestamp.desc()).limit(10).all()

        # Check if any submission exists
        if submissions:
            # Get the latest submission's test results
            latest_submission = submissions[0]
            test_results = eval(latest_submission.test_results) if latest_submission.test_results else None

            # Check completion status
            progress = UserProgress.query.filter_by(
                user_id=session["user_id"],
                task_id=task_id
            ).first()
            completed = progress.completed if progress else False

    return render_template(
        "task.html",
        task=task,
        submissions=submissions,
        test_cases=test_cases,
        logged_in="user_id" in session,
        completed=completed,
        test_results=test_results,  # Add this
        latest_submission=submissions[0] if submissions else None  # Add this
    )


@app.route("/ranking")
def ranking():
    if "user_id" not in session:
        flash("Please login to view the ranking", "danger")
        return redirect(url_for("login"))

    top_users = db.session.query(
        User.username,
        db.func.count(UserProgress.task_id).label('total_completed'),
        db.func.max(User.last_login).label('last_login'),
        db.func.sum(db.case((Task.difficulty == 'Beserk', 1), else_=0)).label('beserk_completed')
    ).join(
        UserProgress, User.id == UserProgress.user_id
    ).join(
        Task, UserProgress.task_id == Task.id
    ).filter(
        UserProgress.completed == True
    ).group_by(
        User.id
    ).order_by(
        db.desc('total_completed'),
        db.desc('beserk_completed')
    ).limit(10).all()

    current_user_stats = db.session.query(
        User.username,
        db.func.count(UserProgress.task_id).label('total_completed'),
        db.func.sum(db.case((Task.difficulty == 'Beserk', 1), else_=0)).label('beserk_completed')
    ).join(
        UserProgress, User.id == UserProgress.user_id
    ).join(
        Task, UserProgress.task_id == Task.id
    ).filter(
        UserProgress.user_id == session["user_id"],
        UserProgress.completed == True
    ).group_by(
        User.id
    ).first()

    user_rank = None
    if current_user_stats:
        all_users_ranked = db.session.query(
            User.id,
            db.func.count(UserProgress.task_id).label('total_completed'),
            db.func.sum(db.case((Task.difficulty == 'Beserk', 1), else_=0)).label('beserk_completed')
        ).join(
            UserProgress, User.id == UserProgress.user_id
        ).join(
            Task, UserProgress.task_id == Task.id
        ).filter(
            UserProgress.completed == True
        ).group_by(
            User.id
        ).order_by(
            db.desc('total_completed'),
            db.desc('beserk_completed')
        ).all()

        for idx, (user_id, total, beserk) in enumerate(all_users_ranked, 1):
            if user_id == session["user_id"]:
                user_rank = idx
                break

    return render_template(
        "ranking.html",
        top_users=top_users,
        current_user_stats=current_user_stats,
        user_rank=user_rank,
        logged_in=True,
        username=session.get("username")
    )

@app.route("/submit_solution/<int:task_id>", methods=["POST"])
def submit_solution(task_id):
    if "user_id" not in session:
        flash("Please login to submit solutions", "danger")
        return redirect(url_for("login"))

    try:
        user_code = request.form.get("code", "")
        if not user_code and "pythonFile" in request.files:
            file = request.files["pythonFile"]
            if file and file.filename.endswith(".py"):
                user_code = file.read().decode('utf-8')

        if not user_code:
            flash("No code submitted", "danger")
            return redirect(url_for("view_task", task_id=task_id))

        task = Task.query.get_or_404(task_id)
        test_cases = TestCase.query.filter_by(task_id=task_id).all()

        tester = PythonTester()
        for case in test_cases:
            tester.add_test_case(case.input, case.output)

        all_passed = tester.test_python_code(user_code)
        test_results = tester.get_test_results()

        submission = Submission(
            user_id=session["user_id"],
            task_id=task_id,
            code=user_code,
            passed=all_passed,
            execution_time=0.0,  # You can calculate this if needed
            test_results=str(test_results)  # Store as string
        )

        if all_passed:
            progress = UserProgress.query.filter_by(
                user_id=session["user_id"],
                task_id=task_id
            ).first()
            if not progress:
                progress = UserProgress(
                    user_id=session["user_id"],
                    task_id=task_id
                )
                db.session.add(progress)
            progress.completed = True
            progress.completion_date = datetime.utcnow()

        db.session.add(submission)
        db.session.commit()

        if all_passed:
            flash("All tests passed! Solution accepted.", "success")
        else:
            flash("Some tests failed. Please check your solution.", "danger")
            session["last_test_results"] = test_results  # Store for display

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error in submit_solution: {str(e)}", exc_info=True)
        flash("An error occurred while processing your submission", "danger")

    return redirect(url_for("view_task", task_id=task_id))

@app.errorhandler(500)
def handle_500(error):
    import traceback
    tb = traceback.format_exc()
    app.logger.error(f"500 Error: {tb}")
    return "Internal Server Error", 500

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

@app.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    if "user_id" not in session:
        flash("Please login to delete your account", "danger")
        return redirect(url_for("login"))

    if request.method == "POST":
        # Confirm deletion
        user = User.query.get(session["user_id"])
        if user:
            # Delete all user progress and submissions first
            UserProgress.query.filter_by(user_id=user.id).delete()
            Submission.query.filter_by(user_id=user.id).delete()
            
            # Then delete the user
            db.session.delete(user)
            db.session.commit()
            
            # Clear session and redirect
            session.clear()
            flash("Your account has been deleted successfully", "info")
            return redirect(url_for("index"))
    
    # For GET requests, show confirmation page
    return render_template("delete_account_confirm.html", 
                         logged_in=True,
                         username=session.get("username"))