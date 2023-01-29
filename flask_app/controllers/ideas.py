from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import idea, user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Navigating the dashboard page tabs:
@app.route('/my_ideas')
def user_ideas():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        "id": session['user_id']
    }
    return render_template('my_ideas.html', user=user.User.get_user_id(data), all_ideas=idea.Idea.get_all_ideas())

# CRUD:
# CREATE
@app.route('/new_idea')
def add_new_idea():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    return render_template("new_idea.html", user= user.User.get_user_id(data))

# READ
@app.route("/idea/<int:id>/view")
def view_idea_details(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id
    }
    return render_template("view_idea.html", one_idea = idea.Idea.get_one_idea(data))

# UPDATE
@app.route("/idea/<int:id>/edit")
def edit_idea(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id
    }
    return render_template("edit_idea.html", edit_idea = idea.Idea.get_one_idea(data))

# DELETE
@app.route("/idea/<int:id>/delete")
def delete_idea(id):
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id
    }
    idea.Idea.delete_idea(data)
    return redirect ("/my_ideas")

# POST METHODS:
@app.route("/add_idea_to_db", methods=["POST"])
def add_idea_to_db():
    if "user_id" not in session:
        return redirect("/")
    if not idea.Idea.validate_idea(request.form):
        return redirect("/new_idea")
    data = {
        "name" : request.form["name"],
        "description" : request.form["description"],
        "user_id": session["user_id"],
    }
    idea.Idea.add_idea(data)
    return redirect("/dashboard")

@app.route("/ideas/<int:id>/edit_idea_in_db", methods=["POST"])
def edit_idea_in_db(id):
    if "user_id" not in session:
        return redirect("/")
    if not idea.Idea.validate_idea(request.form):
        return redirect(f"/idea/{id}/edit")
    data = {
        "name" : request.form["name"],
        "description" : request.form["description"],
        "id": id,
    }
    idea.Idea.update_idea_info(data)
    return redirect("/my_ideas")

# @app.route('/top_ideas')
# def top_ideas():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data ={
#         "id": session['user_id']
#     }
#     return render_template('top_ideas.html', user=user.User.get_user_id(data), all_ideas=idea.Idea.get_all_ideas())

# @app.route('/categories')
# def categories():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data ={
#         "id": session['user_id']
#     }
#     return render_template('categories.html', user=user.User.get_user_id(data), all_ideas=idea.Idea.get_all_ideas())

# @app.route('/ideas/<int:id>/category')
# def one_category():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data ={
#         "id": session['user_id']
#     }
#     return render_template('one_category.html', user=user.User.get_user_id(data), all_ideas=idea.Idea.get_all_ideas())

# @app.route('/favorites')
# def user_favorites():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data ={
#         "id": session['user_id']
#     }
#     return render_template('my_favorites.html', user=user.User.get_user_id(data), all_ideas=idea.Idea.get_all_ideas())