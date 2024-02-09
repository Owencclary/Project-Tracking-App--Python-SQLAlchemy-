from flask import Flask, render_template, redirect, url_for
from forms import TeamForm, ProjectForm
from model import db, User, Team, Project, connect_to_db

app = Flask(__name__) 
app.secret_key = "keep this secret" 
user_id = 1 # makes global user id for incrementation

@app.route("/")
def home(): 
    # gets the wtform classes for input field
    team_form = TeamForm()
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)

    # loads homepage with the form data
    return render_template("home.html", team_form = team_form, project_form = project_form)

# Takes in a post request for adding team
@app.route("/add-team", methods=["POST"])
def add_team():
    team_form = TeamForm() # get the wtform input data as saves it to team_form

    # if wtform fields are valid set upack the team_form input data and insert it to the SQL db Team class
    if team_form.validate_on_submit():
        team_name = team_form.team_name.data 
        new_team = Team(team_name, user_id)
        db.session.add(new_team) 
        db.session.commit()  
        return redirect(url_for("home")) # reloads homepage
    else:
        return redirect(url_for("home")) # reloads homepage if validator are not met 

# Takes in a post request and adds projects to the SQL db
@app.route("/add-project", methods=["POST"])
def add_project():
    project_form = ProjectForm() # gets the wtform project input data
    project_form.update_teams(User.query.get(user_id).teams) # sets the wtform user_id for the team as the user id?

     # if wtform validation is is successful upack the wtform input data and insert it into the SQL db with the project class
    if project_form.validate_on_submit():
        project_name = project_form.project_name.data 
        description = project_form.description.data
        completed = project_form.completed.data
        team_id = project_form.team_selection.data

        # makes a new SQL row for project with the attributes and adds it to the database
        new_project = Project(project_name, description, completed, team_id)
        db.session.add(new_project)
        db.session.commit()
         
        return redirect(url_for("home")) # Reloads homepage
    else:
        return redirect(url_for("home")) # reloads homepage is validators are not met

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug = True)