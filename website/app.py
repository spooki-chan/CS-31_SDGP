from flask import Flask, render_template, redirect, url_for,request,jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from sympy import Q 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import json


import pickle
from pyexpat import model
from sys import api_version
from this import d

cosine_sim = pickle.load(open('./cosine_sim.pickle','rb'))
df = pickle.load(open('df.pickle','rb'))
svd = pickle.load(open('svd.pickle', 'rb'))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret'

file_path = os.path.abspath(os.getcwd())+"\database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path


bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.before_first_request
def create_tables():
    db.create_all()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/Recipe1')
def recipe1():
    return render_template('1.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/hybrid', methods=['GET'])
def hybrid():
    title = request.args.get('title')
    userId = int(request.args.get('userId'))
    idx = df[df.title==title].index.values[0]
    tfdbId = df[df.title==title]['tfdbId'].values[0]
    recipe_id = df[df.title==title]['recipeId'].values[0]
    sim_scores = list(enumerate(cosine_sim[int(idx)]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    recipe_indices = [i[0] for i in sim_scores]
    temp_df = df.iloc[recipe_indices][['title','ingredients','id','recipeId','image']]
    temp_df['est'] = temp_df['recipeId'].apply(lambda x: svd.predict(userId, x).est)
    
    temp_df = temp_df.sort_values('est',ascending=False)
    return temp_df.head(10).to_json(orient='records')
    
    # recipes = df.iloc[recipe_indices][['title','ingredients','id','recipeId','image']]

    # recipes['est'] = recipes['recipeId'].apply(lambda x: svd.predict(userId, x).est)

    # recipes = recipes.sort_values('est', ascending=False)
    # return jsonify(recipes.head(10)) 
    # temp_df['est'] = temp_df['recipeId'].apply(lambda x: svd.predict(userId, x).est)
 #   temp_df = temp_df.head(10)
  #  result = temp_df.to_json(orient="records")
   # parsed = json.loads(result)
   
    # return jsonify(message="My name is " + title + " and I am " + str(userId) + " years old")

# def hybrid(userId,title):
    # title = request.args.get('title')
    # userId = int(request.args.get('userId'))
    # return jsonify(message="My name is " + userId + " and I am " + title + " years old")
    


if __name__ == '__main__':
    app.run(debug=True)