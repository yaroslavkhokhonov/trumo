from flask import Flask, redirect, url_for, session, request, render_template
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer import oauth_authorized

from .store.users import UsersStore

app = Flask(__name__)
app.secret_key = 'your_secret_key'


github_bp = make_github_blueprint(
    client_id='111b595393642694d56d',
    client_secret='b8696bf51d9e8a20dd1edade732d19a78da223b6',
)

app.register_blueprint(github_bp, url_prefix='/github_login')

@app.route('/')
def index():
	if not github.authorized:
		return render_template('unauthorized.html')

	user = github.get('/user').json()
	return render_template(
		'home.html',
		users=UsersStore.getAll(),
		username=user.get('login')
	)

@oauth_authorized.connect_via(github_bp)
def github_logged_in(blueprint, token):
    if token:
        user = github.get("/user").json()
        UsersStore.upsert(user.get('login'), {
			'email': user.get('email'),
			'avatar_url': user.get('avatar_url'),
		})

@app.route('/logout')
def logout():
	del github_bp.token
	session.clear()
	return redirect(url_for('index'))

@app.route('/erase')
def erase():
	user = github.get('/user').json()
	UsersStore.delete(user.get('login'))
	return redirect(url_for('logout'))
