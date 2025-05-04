from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Mock-Datenbank
users = {}
tasks = {
    1: {
        'id': 1,
        'title': 'Sum Two Numbers',
        'description': 'Write a function that takes two numbers from input and returns their sum.',
        'difficulty': 'Easy',
        'test_cases': [
            {'input': '2, 3', 'output': '5'},
            {'input': '10, -5', 'output': '5'}
        ],
        'solution': 'def sum_numbers(a, b):\n    return a + b'
    },
    2: {
        'id': 2,
        'title': 'Factorial Calculator',
        'description': 'Write a function that calculates the factorial of a number.',
        'difficulty': 'Medium',
        'test_cases': [
            {'input': '5', 'output': '120'},
            {'input': '0', 'output': '1'}
        ],
        'solution': 'def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)'
    },
    3: {
        'id': 3,
        'title': 'Prime Number Checker',
        'description': 'Write a function that checks if a number is prime.',
        'difficulty': 'Hard',
        'test_cases': [
            {'input': '7', 'output': 'True'},
            {'input': '4', 'output': 'False'}
        ],
        'solution': 'def is_prime(n):\n    if n <= 1:\n        return False\n    for i in range(2, int(n**0.5)+1):\n        if n % i == 0:\n            return False\n    return True'
    }
}

user_progress = {} 

@app.route('/')
def index():
    return render_template('index.html', 
                         logged_in='username' in session,
                         username=session.get('username'),
                         tasks=tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users:
            flash('Username already taken', 'danger')
        else:
            users[username] = generate_password_hash(password)
            user_progress[username] = {'completed_tasks': []}
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully', 'info')
    return redirect(url_for('index'))

@app.route('/task/<int:task_id>')
def view_task(task_id):
    if task_id not in tasks:
        flash('Task not found', 'danger')
        return redirect(url_for('index'))
    
    completed = False
    if 'username' in session:
        completed = task_id in user_progress[session['username']]['completed_tasks']
    
    return render_template('task.html',
                         task=tasks[task_id],
                         logged_in='username' in session,
                         completed=completed)

@app.route('/submit_solution/<int:task_id>', methods=['POST'])
def submit_solution(task_id):
    if 'username' not in session:
        flash('Please login to submit solutions', 'danger')
        return redirect(url_for('login'))
    
    if task_id not in tasks:
        flash('Task not found', 'danger')
        return redirect(url_for('index'))
    
    # In a real app, you would actually execute and test the code
    user_code = request.form['code']
    task = tasks[task_id]
    
    # Very simple check (in reality, you'd need a code execution environment)
    is_correct = user_code.strip() == task['solution'].strip()
    
    if is_correct:
        user_progress[session['username']]['completed_tasks'].append(task_id)
        flash('Correct solution!', 'success')
    else:
        flash('Incorrect solution. Try again!', 'danger')
    
    return redirect(url_for('view_task', task_id=task_id))

if __name__ == '__main__':
    app.run(debug=True)