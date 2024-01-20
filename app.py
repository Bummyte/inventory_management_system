from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine, text
from models.models import *
import hashlib


app = Flask(__name__)
app.secret_key="somesupersecretkey"
app.config['SQLALCHEMY_DATABASE_URI']='mysql+mysqlconnector://root:bunmi123@localhost/invt_mang'
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)

Base.metadata.create_all(engine)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/register")
def register():
    msg =""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #get the form values
        username = request.form['username'].lower()
        confirm_username = request.form['confirm_username'].lower()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if username!=confirm_username:
            msg = "Usernames do not match"
            return render_template('register.html', msg=msg)
        if password!=confirm_password:
            msg = "Passwords do not match"
            return render_template('register.html', msg=msg)
        with engine.connect() as con:
            result = con.execute(text(f"Select * from user where username = '{username}'"))
            account = result.fetchone()
            con.commit()
        if account:
            msg = "Account already exists"
            return render_template('register.html', msg=msg)
        
        if not username or not password or not confirm_username or not confirm_password:
                msg = "Please fill out the form"
                return render_template('register.html', msg=msg)
        else:
            #encrypt the password
            hash = password + app.secret_key
            hash = hashlib.sha256(hash.encode())
            password = hash.hexdigest()
            #insert the user into the database
            with engine.connect() as con:
                con.execute(text(f"Insert into user (username, password) values ('{username}', '{password}')"))
                con.commit()
            msg = "Account created successfully"
            return redirect(url_for('login', msg=msg))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg =""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #get the form values
        username = request.form['username'].lower()
        password_entered = request.form['password']
        #decrypt the password
        hash = password_entered + app.secret_key
        hash = hashlib.sha256(hash.encode())
        password = hash.hexdigest()
        #check if the user exists in the database
        with engine.connect() as con:
            result = con.execute(text(f"Select * from user where username = '{username}' and password = '{password}'"))
            account = result.fetchone()
            con.commit()
        if account:
            session['loggedin'] = True
            session['id'] = account.id
            session['username'] = account.username
            msg = "Logged in successfully"
            return redirect(url_for('home', msg=msg))
        else:
            msg = "Incorrect username/password"
    return render_template('login.html', msg=msg)  

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('index'))  


@app.route ('/add_product', methods=['GET', 'POST'])
def add_product():
    msg = ""
    if request.method == 'POST':
        product_name = request.form['product_name']
        description = request.form['description']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        category = request.form['category']

        created_at = datetime.now()
        updated_at = datetime.now()
        created_by = session['username']
        updated_by = session['username']

        with engine.connect() as connection:
            connection.execute(text(f"INSERT INTO Product (created_by, created_at, updated_at, updated_by, "
                            f"product_name, description, price, quantity, category) "
                            f"VALUES ('{created_by}', '{created_at}', '{updated_at}', '{updated_by}', "
                            f"'{product_name}', '{description}', '{price}', '{quantity}', '{category}')"))
            
            connection.commit()
            msg = ('Product added successfully!', 'success')   
        return redirect(url_for('index'))

    return render_template('add_product.html')


@app.route('/record_transaction', methods=['POST'])
def record_transaction():
    product_id = request.form['product_id']
    transaction_type = request.form['transaction_type']
    quantity = int(request.form['quantity'])
    unit_price = float(request.form['unit_price'])
    transaction_date = request.form['transaction_date']
    payment_method = request.form['payment_method']
    customer_name = request.form['customer_name']
    shipping_address = request.form['shipping_address']

    engine = create_engine('sqlite:///site.db')
    with engine.connect() as connection:
        query = text(
            "INSERT INTO transaction "
            "(product_id, transaction_type, quantity, unit_price, transaction_date, payment_method, "
            "customer_name, shipping_address) "
            "VALUES (:product_id, :transaction_type, :quantity, :unit_price, :transaction_date, "
            ":payment_method, :customer_name, :shipping_address)"
        )
        connection.execute(query,
            product_id=product_id,
            transaction_type=transaction_type,
            quantity=quantity,
            unit_price=unit_price,
            transaction_date=transaction_date,
            payment_method=payment_method,
            customer_name=customer_name,
            shipping_address=shipping_address
        )
        msg = ('Product added successfully!', 'success')   
        return redirect(url_for('index'))
    
    return render_template('add_product.html')

if __name__ == '__main__':
    app.run(debug=True)
