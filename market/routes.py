from market import app 
from flask import render_template,redirect,url_for,flash, request
from .models import Item,User
from .forms import RegisterForm , LoginForm , purchaseForm , SellForm
from market import db
from flask_login import login_user , logout_user , login_required , current_user
from math import*

@app.route("/")
def Home_page():
    return render_template('home.html')

@app.route("/market", methods=['GET','POST'])
@login_required # it related with login_view in the __init__ file it leads us to the specific route in the login_view
def market_page():
    purchase_form = purchaseForm()
    selling_form = SellForm()
    if request.method =='POST':
        # Purchase Item Logic
        purchased_item_name = request.form.get("purchased_item")
        with app.app_context():
            p_item_obj = Item.query.filter_by(name = purchased_item_name).first()
            if p_item_obj : 
                if current_user.can_purchase(p_item_obj):
                    try:
                        p_item_obj.buy(current_user)                                    
                        #p_item_obj.owner = current_user.id                             {
                        #                                                               I replaced all the commentary 
                        #                                                               instuctions with Buy() Function , 
                        #                                                               i created in the Item class                                                                                        
                        #print(current_user.budget)                                      } 
                        #current_user.budget -= p_item_obj.price
                        #print(current_user.budget)
                        #rec_user = User.query.filter_by(id = current_user.id).first()
                        #rec_user.budget -= p_item_obj.price
                        #db.session.commit()
                        #print(f'Success ! You bouth the {purchased_item_name} with {p_item_obj.price} $')
                        flash(f'Congratulations You bougth the {p_item_obj.name} with {p_item_obj.price} $', category='Success')
                    except:
                        print('Error')
                else:
                    flash(f"Unfortunately ! You dont have enough money to buy this {p_item_obj.name} at {p_item_obj.price} $", category='danger')
        # Sell Item Logic
            sold_item_name = request.form.get("sold_item")
            s_item_obj = Item.query.filter_by(name = sold_item_name).first()
            if s_item_obj:
                #if s_item_obj in current_user.items:
                try:
                    s_item_obj.owner = None # it will returnS without owner cause it sold and puted on the market 
                    rec_user = User.query.filter_by(id = current_user.id).first()                                 
                    rec_user.budget += s_item_obj.price
                    db.session.commit()
                    flash(f"Congratulations ! You Sold the {s_item_obj.name}",category='Success')
                except:
                        print('Error')
                #else:
                    #flash("SomeThings wrong with selling this Item !",category='danger')        
        return redirect(url_for("market_page"))
        
    if request.method=='GET':
        with app.app_context():# to stay in the Application context    
            items = Item.query.filter_by(owner  =  None)# the item variable Contains all the Objects located in the data base form The class Item 
            owned_items = Item.query.filter_by(owner = current_user.id)
        return render_template('market.html', items = items , purchase_form = purchase_form, owned_items = owned_items , selling_form = selling_form)

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