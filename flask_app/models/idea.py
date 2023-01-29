from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Idea:
    db_name = "solo_project_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = None
    
    # Add a new idea to db
    @classmethod
    def add_idea(cls, data):
        query = """
        INSERT INTO ideas
        (name, description, user_id)
        VALUES
        (%(name)s, %(description)s, %(user_id)s);
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    # Grab all the ideas in db
    @classmethod
    def get_all_ideas(cls):
        query = """
        SELECT * FROM ideas
        JOIN users
        ON ideas.user_id = users.id
        ORDER BY ideas.created_at DESC;
        """
        results = connectToMySQL(cls.db_name).query_db(query)
        if len(results) == 0:
            return []
        else:
            all_ideas = []
            for idea_dict in results:
                idea_obj = cls(idea_dict)
                user_dict = {
                    "id" : idea_dict["users.id"],
                    "first_name" : idea_dict["first_name"],
                    "last_name" : idea_dict["last_name"],
                    "email" : idea_dict["email"],
                    "password" : idea_dict["password"],
                    "created_at" : idea_dict["users.created_at"],
                    "updated_at" : idea_dict["users.updated_at"],
                }
                user_obj = user.User(user_dict)
                idea_obj.user =user_obj
                all_ideas.append(idea_obj)
            return all_ideas
    
    # Grab one idea from db
    @classmethod
    def get_one_idea(cls, data):
        query = """
        SELECT * FROM ideas
        JOIN users
        ON ideas.user_id = users.id
        WHERE ideas.id = %(id)s;
        """
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            idea_dict = results[0]
            idea_obj = cls(idea_dict)
            user_dict = {
                "id" : idea_dict["users.id"],
                "first_name" : idea_dict["first_name"],
                "last_name" : idea_dict["last_name"],
                "email" : idea_dict["email"],
                "password" : idea_dict["password"],
                "created_at" : idea_dict["users.created_at"],
                "updated_at" : idea_dict["users.updated_at"],
            }
            user_obj = user.User(user_dict)
            idea_obj.user = user_obj
        return idea_obj
    
    # Update idea in db
    @classmethod
    def update_idea_info(cls,data):
        query = """
        UPDATE ideas SET
        name = %(name)s,
        description = %(description)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    # Delete idea in db
    @classmethod
    def delete_idea(cls,data):
        query = "DELETE FROM ideas WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    # Validations
    @staticmethod
    def validate_idea(form_data):
        is_valid = True
        print(form_data)
        if len(form_data["name"]) < 2:
            flash("Name must be at least 2 characters!")
            is_valid = False
        if len(form_data["description"]) < 10:
            flash("Description must be at least 10 characters!")
            is_valid = False
        # if "category" not in form_data  or int(form_data["category"]) == 0: #or int(form_data["category"]) > 10:
        #     flash("You must select a category!")
        #     is_valid = False
        return is_valid