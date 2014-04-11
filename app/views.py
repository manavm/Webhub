import sys
sys.path.append("..")
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, EditForm, InputForm, PopForm

from models import User, ROLE_USER, ROLE_ADMIN
from datetime import datetime
from test_repo import statBox as sb
# import scipy

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated():
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index(params = None):
	form = InputForm()
	user = g.user
	if form.validate_on_submit():
		return redirect(url_for('results'))
		# if form.queryType.data == "vin_query":
		# 	return redirect(url_for('results'))
		if form.queryType.data == "pop_query":
			form = PopForm()
			# return redirect(url_for('results'))
		# 	return render_template("index.html",
		# 		form = pop_form,
		# 		user = user)
	return render_template("index.html",
		form = form,
		user = user)

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
	return render_template('login.html', 
		form = form,
		providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email == "":
		flash('Invalid login. Please try again.')
		return redirect(url_for('login'))
	user = User.query.filter_by(email = resp.email).first()
	if user is None:
		nickname = resp.nickname
		if nickname is None or nickname == "":
			nickname = resp.email.split('@')[0]
		nickname = User.make_unique_nickname(nickname)
		user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
		db.session.add(user)
		db.session.commit()
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login_user(user, remember = remember_me)
	return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
	user = User.query.filter_by(nickname = nickname).first()
	if user == None:
		flash('User ' + nickname + ' not found.')
		return redirect(url_for('index'))
	posts = [
		{'author': user, 'body': 'Test post #1'},
		{'author': user, 'body': 'Test post #2'}
	]
	return render_template('user.html',
		user = user,
		posts = posts)

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
    return render_template('edit.html',
        form = form)

@app.route('/results', methods = ['GET', 'POST'])
@login_required
def results():
	# obj = scriptbox.queryBox.query("vinQuery", vid = request.form["vin_value"])
	# obj.df.to_csv("vin_results.csv", sep='\t', encoding = 'utf-8')
	# return "vin_results.csv"
	return "cool"

###########################################

#Error Handlers

###########################################
@app.errorhandler(400)
def bad_request_error(error):
	return render_template('results.html')

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500