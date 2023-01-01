from market import app
from flask import render_template,redirect,url_for,flash
from .models import Item,User
from .forms import RegisterForm , LoginForm
from market import db
from flask_login import login_user 

@app.route("/")
def Home_page():
    return render_template('home.html')

@app.route("/market")
def market_page():
    with app.app_context():
        items = Item.query.all()
    return render_template('market.html', items = items)

@app.route("/register", methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():                                                                         #iT Was password_hash
        user_to_create = User(username = form.user_name.data , email_addresse = form.email_addresse.data , password = form.password1.data )
        with app.app_context():
            db.session.add(user_to_create)
            db.session.commit()
        return(redirect(url_for('market_page')))    
    if form.errors != {}:# If there is no errors in Validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form = form)



@app.route("/login", methods=["GET","POST"])
def login_page():
    form = LoginForm()
    
    if form .validate_on_submit():
        
        with app.app_context():
            attempted_user = User.query.filter_by(username = form.user_name.data).first()
        
            if attempted_user and attempted_user.check_password_correction(attempted_password = form.password.data):
            
                login_user(attempted_user , remember= True)
                flash(f'succes you logged in as {attempted_user.username}', category='success')
                return( render_template('market.html') )
        
            else:
            
                flash(f'username and password dont much !', category='danger')    
                return render_template('login.html')

    return render_template('login.html', form = form)