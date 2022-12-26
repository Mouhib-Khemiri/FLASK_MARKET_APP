from flask import Flask, render_template 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///market.db'
db = SQLAlchemy(app)

#To stay into the application context 
'''with app.app_context():
    db.create_all()'''

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(length=30), nullable = False, unique = True)
    price =  db.Column(db.Integer(), nullable = False)
    barcode =  db.Column(db.String(length=12), nullable = False, unique = True)
    description = db.Column(db.String(length=1024) , nullable = False , unique=True)

#Whene you do query to display the items in Db it refers with name.
    def __repr__(self):
        return f'Item {self.name}'
    

@app.route("/")
def Home_page():
    return render_template('home.html')

@app.route("/market")
def market_page():
    with app.app_context():
        items = Item.query.all()
    return render_template('market.html', items = items)