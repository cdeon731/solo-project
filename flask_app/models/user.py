from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
from flask_app import app
bcrypt = Bcrypt(app)
from flask_app.models import idea

class User:
    db_name = "solo_project_schema"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ideas = []
    
    @classmethod
    def register_user(cls, data):
        query = """
        INSERT INTO users
        (first_name, last_name, email, password)
        VALUES 
        (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_user_id(cls, data):
        query = """
        SELECT * FROM users
        WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            return cls(results[0])

    @classmethod
    def get_user_email(cls, data):
        query = """
        SELECT * FROM users
        WHERE email = %(email)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            return cls(results[0])
    
    @classmethod
    def get_all_users_ideas(cls, data):
        query = """
        SELECT * FROM users
        LEFT JOIN ideas
        ON users.id = ideas.user_id
        WHERE users.id = %(id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return []
        else:
            user_object = cls(results[0])
            for user_ideas in results:
                idea_dict = {
                    "id": user_ideas["ideas.id"],
                    "name": user_ideas["name"],
                    "description": user_ideas["description"],
                    "created_at": user_ideas["ideas.created_at"],
                    "updated_at": user_ideas["ideas.updated_at"],
                }
                idea_obj = idea.Idea(idea_dict)
                user_object.ideas.append(idea_obj)
            return user_object
    

    # Validations
    @staticmethod
    def validate_registration(form_data):
        is_valid = True
        if len(form_data["first_name"]) < 2:
            flash("First name must be 2 or more characters!", "register")
            is_valid = False
        if len(form_data["last_name"]) < 2:
            flash("Last name must be 2 or more characters!", "register")
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!", "register")
            is_valid = False
        data = {
            "email": form_data["email"]
        }
        found_user = User.get_user_email(data)
        if found_user != None:
            flash("Email already in use!", "register")
            is_valid = False
        if len(form_data["password"]) < 8:
            flash("Password must be 8 or more characters!", "register")
            is_valid = False
        if form_data["password"] != form_data["confirm"]:
            flash("Passwords don't match!", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(form_data):
        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid login", "login")
            return False
        data = {
            "email": form_data["email"]
        }
        found_user = User.get_user_email(data)
        if found_user == None:
            flash("Invalid login", "login")
            return False
        if not bcrypt.check_password_hash(found_user.password, form_data["password"]):
            flash("Invalid login", "login")
            return False
        return found_user