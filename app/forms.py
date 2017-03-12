from flask.ext.wtf import Form
from wtforms import IntegerField
from wtforms.validators import DataRequired

class RatingForm(Form):
	rating = IntegerField('rating', validators=[DataRequired()])
	
