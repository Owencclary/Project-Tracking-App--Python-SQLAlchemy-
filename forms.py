from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length

# team form class to take in team name
class TeamForm(FlaskForm):
    team_name = StringField('team name', validators=[DataRequired(), Length(min=4, max=255)])
    submit = SubmitField("submit")

# project form class to take in project name, desc, the team and completion
class ProjectForm(FlaskForm):
    project_name = StringField('project name', validators=[DataRequired(), Length(min=4, max=255)])
    description = TextAreaField('description')
    completed = BooleanField("completed?")
    team_selection = SelectField("team")
    submit = SubmitField("submit")

    # function to select which team the rpoject belongs to
    def update_teams(self, teams):
        self.team_selection.choices = [ (team.id, team.team_name) for team in teams ]