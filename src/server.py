from flask import Flask, render_template, request
from movie_reccon import cosine_sim, cosine_sim2, get_recommendations
from forms import GetData
app = Flask(__name__)


SECRET_KEY = b"5@\xa5\x8f\xd0'\x92N\x19~\x81\rh\xcb!~a\xb31\x012\xcd\x80(t5\xd2o\xadms\xe1"
# SECRET KEY to prevent modifying of cookies
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/',methods=['GET','POST'])
def home():
	data= list()
	form = GetData()
	if request.method == 'POST':
		movie_name = request.form['movie']
		try:
			try:
				request.form['tfidf'] == True
				data = get_recommendations(movie_name, cosine_sim)
			except:
				data = get_recommendations(movie_name, cosine_sim2)
			return render_template('home.html', data=data, form=form)	
		except:
			data = ["Sorry no recommendations available"]	
			return render_template('home.html', data=data, form=form)
	elif request.method == 'GET':
		return render_template('home.html', form=form, data=data)
	return render_template('home.html', form=form, data=data)



def contact():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Do Something':
            pass # do something
        elif request.form['submit_button'] == 'Do Something Else':
            pass # do something else
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('contact.html', form=form)	

if(__name__=='__main__'):  #This is so that we can run it directly in debug mode
	app.run(debug=True)

