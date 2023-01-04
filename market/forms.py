from flask_wtf import FlaskForm
from wtforms import StringField ,PasswordField,SubmitField
from wtforms.validators import Length , EqualTo , Email , DataRequired , ValidationError
from market.models import User
from market import app

class RegisterForm(FlaskForm):

    def validate_username(self,user_name_to_check):#it checks if there is More than one objects has a same username.
        with app.app_context():
            user = User.query.filter_by(user_name = user_name_to_check.data).first()     
            if user:
                raise ValidationError("Username is already exists! please try with a diffrent Username")
    
    def validate_email_addresse(self,email_addresse_to_check):#it checks if there is More than one objects has a same email_addresse.
        with app.app_context():
            email = User.query.filter_by(email_addresse = email_addresse_to_check.data).first()
            if email:
                raise ValidationError("Email_addresse is already exists please try with an other email_addresse ")

    user_name = StringField(label='User Name :', validators  = [Length(min=3, max=30),DataRequired()])
    email_addresse = StringField(label='Email :', validators = [Email(),DataRequired()])
    password1 = PasswordField(label="Password :", validators = [Length(min=6),DataRequired()])
    password2 = PasswordField(label="Confirm Password:", validators=[EqualTo('password1'),DataRequired()])
    submit = SubmitField(label="Create Account ")
    
class LoginForm(FlaskForm):
    user_name = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit   = SubmitField(label="Sign in ")

class PurchaseItemForm(FlaskForm):
    submit  = SubmitField(label="Purchase item!")