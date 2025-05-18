from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from models import db, Booking
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booking.db'
db.init_app(app)
USERS_FILE = 'users.json'



def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    title = request.form.get('title')
    price = request.form.get('price')

    
    cart = session.get('cart', [])
    cart.append({'title': title, 'price': price})
    
   
    session['cart'] = cart
    session.modified = True

    return redirect(url_for('menu'))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart=cart_items)

@app.route('/remove_from_cart/<int:item_index>', methods=['POST'])
def remove_from_cart(item_index):
    cart = session.get('cart', [])
    
    if 0 <= item_index < len(cart):
        cart.pop(item_index)

    session['cart'] = cart
    session.modified = True

    return redirect(url_for('cart'))

@app.route('/autorize', methods=['GET', 'POST'])
def autorize():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return "Неверный логин или пароль!"

    return render_template('authorize.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username in users:
            return "Пользователь уже существует!"

        users[username] = password
        save_users(users)
        return redirect(url_for('autorize'))

    return render_template('register.html')


@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('main.html', user=session['user'])


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        session['day'] = request.form.get('day')
        session['time'] = request.form.get('time')
        session['guests'] = request.form.get('guests')
        session['during'] = request.form.get('during')
        session['table'] = request.form.get('table')

        cart = session.get('cart', [])
        session['cart_items'] = json.dumps(cart)


        return redirect(url_for('contacts'))

    return render_template('booking.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/add_contacts', methods=['POST'])
def add_contacts():
    cart = session.get('cart', [])
    order = json.dumps(cart)

  
    booking = Booking(
        day=session.get('day'),
        time=session.get('time'),
        guests=int(session.get('guests')),
        during=session.get('during'),
        table=session.get('table'),
        name=request.form.get('name'),
        phone=request.form.get('tel'),
        email=request.form.get('email'),
        order=order
       
    )
    

    db.session.add(booking)
    db.session.commit()

   
    session.pop('day', None)
    session.pop('time', None)
    session.pop('guests', None)
    session.pop('during', None)
    session.pop('table', None)
    session.pop('cart', None)

    return redirect(url_for('show'))



@app.route('/show')
def show():
    reservations = Booking.query.all()
    for res in reservations:
        if res.order:
            res.order = json.loads(res.order) 
    return render_template('show.html', reservations=reservations)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
