from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, FloatField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	password = PasswordField('Enter Administrator Password', validators=[DataRequired()])
	submit = SubmitField('Login')
	
class DumpsterForm(FlaskForm):
	location = StringField('Location Name', validators=[DataRequired()])
	lat = FloatField('Lattitude', validators=[DataRequired()])
	lng = FloatField('Longitude', validators=[DataRequired()])
	submit = SubmitField('Create Dumpster')
	
class UpdateDumpsterForm(FlaskForm):
	location = StringField('Location Name', validators=[DataRequired()])
	lat = FloatField('Lattitude', validators=[DataRequired()])
	lng = FloatField('Longitude', validators=[DataRequired()])
	full = BooleanField('Full')
	submit = SubmitField('Update Dumpster')