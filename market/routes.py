from market import app
from flask import render_template,redirect,url_for,flash, request
from .models import Item,User
from .forms import RegisterForm , LoginForm ,  PurchaseItemForm
from market import db
from flask_login import login_user , logout_user , login_required , current_user
from math import*

@app.route("/")
def Home_page():
    return render_template('home.html')

@app.route("/market", methods=['GET','POST'])
@login_required # it related with login_view in the __init__ file it leads us to the specific route in the login_view
def market_page():
    with app.app_context():# to stay in the Application context
        
        purchase_form = PurchaseItemForm() # a Class in forms.py file
        
        if request.method == "POST": # Whene request.methode == 'POST' request like Clicking on the submit field "Button"
            purchased_item = request.form.get('purchased_item') # The Purchased_item Variable Contains the name of the Object {{ item.name }}
            purchased_item_Object = Item.query.filter_by(name = purchased_item).first() # This is an object from the Item Class located in the Db whow have a name from the purchesed_item input , it returns as the {{ item.name }}
            
            if purchased_item_Object: # cheking if the object found in the db with his correct! name it means that he is not none : 
                purchased_item_Object.owner = current_user.id # Give an Owner from The Class User with the id attribute to the purchase_Item_Object
                current_user.budget -= purchased_item_Object.price #Decrease The Budget of the current_user whene he buy ana Item or article from the market 
                db.session.commit() 
        
        items = Item.query.filter_by(owner=None) # the item variable Contains all the Objects located in the data base form The class Item 
    return render_template('market.html', items = items , purchase_form = purchase_form)

@app.route("/register", methods=['GET','POST'])
def register_page():
    form = RegisterForm() # a Class in forms.py file
    if form.validate_on_submit(): # Whene request.methode == 'POST' request like Clicking on the submit field "Button"                                                                        #iT Was password_hash
        user_to_create = User(username = form.user_name.data , email_addresse = form.email_addresse.data , password = form.password1.data )
        
        with app.app_context(): # to stay in the application Context
            db.session.add(user_to_create) # Add the user_to_create Obbject into The Data base
            db.session.commit()
            
            login_user(user_to_create)
            flash(f"Account Created succesfully! You are logged in as {user_to_create.username}" , category= 'success')   
        
        return(redirect(url_for('market_page')))    
    
    if form.errors != {}: # If there is no errors in Validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form = form)



@app.route("/login", methods=["GET","POST"])
def login_page():
    form = LoginForm() # Class in form.py file 
    if form.validate_on_submit():
        with app.app_context(): # to stay in application context 
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