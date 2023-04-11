from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# set up app
app = Flask(__name__)
# initialize new database, db is an object
db = SQLAlchemy()
DB_NAME = "database.db"
# to secure/encrypt cookies data in our app
def readDetails(fileName):
    with open(fileName, 'r') as file:
        return [line for line in file]
    
def getDetails(fileName):
    with open(fileName) as file:
        return file.read()
    
secret_key = getDetails('secret_key.txt')
app.config['SECRET_KEY'] = secret_key
# telling our app where out database is located
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
# initialize database by giving it our flask app
db.init_app(app)
@app.before_first_request
def create_tables():
    db.create_all()



# creating a Model
class User(db.Model, UserMixin):
    '''userEmail, userFirstName, userLastName'''
    id = db.Column(db.Integer, primary_key = True)              # reference id of each entry
    userEmail = db.Column(db.String(300), unique = True)       # email of user
    userFirstName = db.Column(db.String(100))
    userLastName = db.Column(db.String(100))



# create home route
@app.route('/')
#define function for that route
def home():
    return render_template('home.html')

@app.route('/about', methods = ['GET', 'POST'])
def about():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        # variable to check if email inputed already exists in database
        userExist = User.query.filter_by(userEmail = email).first()
        if len(email) < 4:
            flash("Email must be longer than 3 characters.", category='error')
        elif userExist:
            flash(f"Your email is already in our database, {first_name}!", category='success')
        else:
            new_user = User(userEmail = email, userFirstName = first_name, userLastName = last_name)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Thank you for your interest, {first_name}! You will receive an email with more details.', category='success')
            return redirect('/about')
    return render_template('about.html')


@app.route('/rocky')
def rocky():
    details = readDetails('static/details.txt')
    return render_template('rocky.html', fileDetails = details)

@app.route('/lucas')
def lucas():
    Lucas_details = readDetails('static/details_lucas.txt')
    return render_template('lucas.html', LucasDetails = Lucas_details)

@app.route('/luna')
def luna():
    detailsLuna = readDetails('static/details_luna.txt')
    return render_template('luna.html', LunaDetails = detailsLuna)



# debug = True means any changes we make in code will be automatically updated live as we code
if __name__ == "__main__":
    app.run(debug = True, port=2000)