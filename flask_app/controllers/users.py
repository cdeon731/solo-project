from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import user, idea
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        "id": session['user_id']
    }
    return render_template('dashboard.html', user=user.User.get_user_id(data), all_ideas=idea.Idea.get_all_ideas())

# Post Routes:
@app.route("/register", methods=["POST"])
def register_user():
    if not user.User.validate_registration(request.form):
        return redirect("/register")
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
    }
    session["user_id"] = user.User.register_user(data)
    return redirect("/dashboard")

@app.route("/login", methods=["POST"])
def login_user():
    found_user = user.User.validate_login(request.form)
    if not found_user:
        return redirect("/login")
    session["user_id"] = found_user.id
    return redirect("/dashboard")