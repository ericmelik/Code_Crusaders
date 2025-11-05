from flask import Flask, render_template, redirect, url_for, request, session
import mysql.connector
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages & sessions

bcrypt = Bcrypt(app)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="flaskuser",
    password="mypassword123",
    database="flask_db"
)
cursor = db.cursor(dictionary=True)

# ---------- ROUTES ----------

# @app.route('/')
# def home():
#     if 'user_id' in session:
#         return f"Welcome, {session['username']}!"
#     return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        db.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password.", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

@app.route('/exam_menu')
def exam_menu():
    return render_template('exam_menu.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     return render_template('login.html')

if __name__ == '__main__':
     app.run(host = '0.0.0.0', port = 5001, debug=True)
     print("Server is running on http://localhost:5001") 