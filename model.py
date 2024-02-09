import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model): # Creates a database called users

    __tablename__ = "users"

    # Creates collums for db 
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(255), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)

    teams = db.relationship("Team", backref = "user", lazy = True)

    # Function to create a new user more easily
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Team(db.Model): # Creates a database for teams

    __tablename__ = "teams"

    # Creates collums for teams and connects to users as a one to many relationship
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    team_name = db.Column(db.String(255), unique = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    def __init__(self, team_name, user_id):
        self.team_name = team_name
        self.user_id = user_id

class Project(db.Model): # Creates a database for projects

    __tablename__ = "projects"

    # Creates columns for projects and connects to teams as a one to one relationship
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    project_name = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255), nullable = True)
    completed = db.Column(db.Boolean, default = False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable = False)

    def __init__(self, project_name, description, completed, team_id):
        self.project_name = project_name
        self.team_name = project_name
        self.description = description
        self.completed = completed
        self.team_id = team_id

# Connects to the db URI with the flask app
def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"] # Searches the enviorment for a variable called POSTGRES_URI then sets it to the app.config
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to db...")
