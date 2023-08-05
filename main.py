
import dbm
from shelve import DbfilenameShelf
from sqlite3 import dbapi2
from flask import Flask, flash, g, redirect,render_template, request, url_for,session
import sqlite3
from werkzeug.utils import secure_filename
import os

from sqlitedb import get_mail

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



app = Flask(__name__)


app.config['SECRET_KEY'] = '123'

DATABASE = 'users.sqlite'
conn = sqlite3.connect('users.sqlite')
conn.commit()
conn.close()



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()

    for book in books:
        print(book)
    return render_template('index.html',books=books)
@app.route("/login")
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()

    for book in books:
        print(book)
    return render_template('home.html',books=books)

@app.route("/profile")
def profile():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM shipping ')
    profile = cursor.fetchall()

    for profiles in profile:
        print(profiles)
    return render_template('profile.html')

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        # Get the uploaded file from the form
        file = request.files['profile_picture']
        
        # Check if the file is allowed
        if file and allowed_file(file.filename):
            # Secure the filename to prevent directory traversal attacks
            filename = secure_filename(file.filename)
            
            # Save the file to the UPLOAD_FOLDER directory
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Update the user's profile picture URL in the database
            user_id = session['user_id']
            profile_picture_url = url_for('static', filename='uploads/' + filename)
            dbapi2.execute('UPDATE users SET profile_picture_url = ? WHERE id = ?', (profile_picture_url, user_id))
            DbfilenameShelf.commit()
            
            flash('Your profile picture has been updated.')
            return redirect(url_for('edit_profile'))
            
    # Render the edit profile page
    user_id = session['user_id']
    user = dbm.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    return render_template('edit_profile.html', user=user)

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/shipping")
def shipping():
    return render_template('shipping.html')

@app.route('/admin')
def admin():
    conn = sqlite3.connect('users.sqlite')
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM customer_order_details')
    rows = c.fetchall()
    conn.close()
    return render_template('admin.html', rows=rows)

@app.route('/cart')
def cart():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cart')
    cart_items = cursor.fetchall()
    conn.close()
    return render_template('cart.html', cart_items=cart_items)



@app.route('/payment')
def payment():
    username = session.get('username')
    print(username)
    email=get_mail(username)
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT address, state, postcode FROM shipping WHERE email")
    rows = cursor.fetchall()
    print(rows)
    return render_template('payment.html',rows=rows)

@app.route("/main")
def main():
    return render_template('main.css')

@app.route('/newlogin', methods=['POST'])
def newlogin():
    print(request.method)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        print(username,password)
        print(type(username),type(password))
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users_details WHERE username = ? AND password = ?', (username, password))
        user = cur.fetchone()
        print("user id s",user)
        conn.close()
        if username.lower()=='kstech' and password=='12345':
            return redirect(url_for('admin'))
        elif user  is not None:
             return redirect(url_for('home'))
        else:
            return render_template("login.html",error='Invaild username or password') 
    return redirect(url_for("login"))

@app.route("/newregister", methods=['POST'])
def newreg():
    firstname= request.form.get('firstname',None)
    lastname= request.form.get('lastname',None)
    username= request.form.get('username',None)
    email= request.form.get('email',None)
    password= request.form.get('password',None)
    confirmpassword= request.form.get('confirmpassword',None)
    check= request.form.get('check')

    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO users(firstname,lastname,username,email,password,confirmpassword) VALUES(?,?,?,?,?,?)',(firstname,lastname,username,email,password,confirmpassword))
    conn.commit()
    conn.close()
    print(firstname,lastname,username,email,password,confirmpassword,check)
   
    return redirect('/login')
    
@app.route("/shipping_details", methods=['POST'])
def shipping_details():
    fullname= request.form.get('fullname',None)
    phoneno= request.form.get('phoneno',None)
    email= request.form.get('email',None)
    address= request.form.get('address',None)
    state= request.form.get('state',None)
    postcode= request.form.get('postcode',None)
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO shipping(fullname,phoneno,email,address,state,postcode) VALUES(?,?,?,?,?,?)',(fullname,phoneno,email,address,state,postcode))
    conn.commit()
    conn.close()
    print(fullname,phoneno,email,address,state,postcode)
   
    return redirect('/payment')




if __name__ == '__main__':
    app.run()
