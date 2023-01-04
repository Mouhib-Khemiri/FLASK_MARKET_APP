from market import app
from flask import render_template,redirect,url_for,flash
from .models import Item,User
from .forms import RegisterForm , LoginForm ,  PurchaseItemForm
from market import db
from flask_login import login_user , logout_user , login_required

@app.route("/")
def Home_page():
    return render_template('home.html')

@app.route("/market")
@login_required # it related with login_view in the __init__ file it leads us to the specific route in the login_view
def market_page():
    purchase_form= PurchaseItemForm()
    with app.app_context():
        items = Item.query.all()
    return render_template('market.html', items = items , purchase_form = purchase_form)

@app.route("/register", methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():                                                                         #iT Was password_hash
        user_to_create = User(username = form.user_name.data , email_addresse = form.email_addresse.data , password = form.password1.data )
        
        with app.app_context():
            db.session.add(user_to_create)
            db.session.commit()
            
            login_user(user_to_create)
            flash(f"Account Created succesfully! You are logged in as {user_to_create.username}" , category= 'success')   
        
        return(redirect(url_for('market_page')))    
    
    if form.errors != {}:# If there is no errors in Validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form = form)



@app.route("/login", methods=["GET","POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        with app.app_context():
            attempted_user = User.query.filter_by(username = form.user_name.data).first()
            if attempted_user and attempted_user.check_password_correction(
                attempted_password= form.password.data
                ):
                login_user(attempted_user)
                flash(f'Success ! You are Logged in as {attempted_user.username}', category='success')
                return redirect(url_for('market_page'))
            else:
                flash('username and password are not match ! Please try again ', category='danger')
    return render_template('login.html', form = form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been Logged out!', category='info')
    return(redirect(url_for('Home_page')))