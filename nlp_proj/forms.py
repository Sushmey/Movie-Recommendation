from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import InputRequired

class GetData(FlaskForm):
	movie = StringField('Movie')
	tfidf = BooleanField('TF-IDF', default=False)

	submit = SubmitField('Get Reccs!')