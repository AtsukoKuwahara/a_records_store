from flask import render_template, redirect, url_for, jsonify, request, session, flash
from .model import Product, User, Order, RecordOfTheWeek
from . import app, api
from .forms import LoginForm, RegisterForm
from flask_restx import Resource
from .shoppingcart import shoppingcart
import json

# Utility function to load coming soon products from a JSON file
def load_coming_soon_products():
    """
    Load coming soon products from a JSON file.
    :return: List of coming soon products
    """
    with open('data/coming_soon_products.json') as f:
        return json.load(f)

# User API Routes
@api.route('/users')
class UserGetAndPost(Resource):
    def get(self):
        """Get all users"""
        return jsonify(User.objects.all())

    def post(self):
        """Create a new user"""
        data = api.payload
        user = User(
            user_id=data['user_id'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        user.set_password(data['password'])
        user.save()
        return jsonify(User.objects(user_id=data['user_id']))

@api.route('/users/<idx>')
class UserGetUpdateDelete(Resource):
    def get(self, idx):
        """Get a user by ID"""
        return jsonify(User.objects(user_id=idx))

    def put(self, idx):
        """Update a user by ID"""
        data = api.payload
        User.objects(user_id=idx).update(**data)
        return jsonify(User.objects(user_id=idx))

    def delete(self, idx):
        """Delete a user by ID"""
        User.objects(user_id=idx).delete()
        return jsonify("User is deleted!")

# Product API Routes
@api.route('/products')
class ProductGetAndPost(Resource):
    def get(self):
        """Get all products"""
        return jsonify(Product.objects.all())

    def post(self):
        """Create a new product"""
        data = api.payload
        product = Product(
            product_id=data['product_id'],
            title=data['title'],
            artist=data['artist'],
            label=data['label'],
            price=data['price']
        )
        product.save()
        return jsonify(Product.objects(product_id=data['product_id']))

@api.route('/products/<idx>')
class ProductGetUpdateDelete(Resource):
    def get(self, idx):
        """Get a product by ID"""
        return jsonify(Product.objects(product_id=idx))

    def put(self, idx):
        """Update a product by ID"""
        data = api.payload
        Product.objects(product_id=idx).update(**data)
        return jsonify(Product.objects(product_id=idx))

    def delete(self, idx):
        """Delete a product by ID"""
        Product.objects(product_id=idx).delete()
        return jsonify("Product is deleted!")

# Web Routes
@app.route('/')
@app.route('/index')
def index():
    """
    Render the index page with the featured product and coming soon products.
    """
    # Fetch the most recent record of the week
    featured_product_entry = RecordOfTheWeek.objects.order_by('-created_at').first()
    featured_product = None
    if featured_product_entry:
        featured_product = Product.objects(product_id=featured_product_entry.product_id).first()
        if featured_product:
            featured_product.message = featured_product_entry.message

    coming_soon_products = load_coming_soon_products()
    return render_template('index.html', featured_product=featured_product, coming_soon_products=coming_soon_products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.objects(email=email).first()
        if user and user.get_password(password):
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            session['role'] = user.role  # Store the user role in the session
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration.
    """
    if session.get('username'):
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count() + 1
        user = User(
            user_id=user_id,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            role='admin' if user_id == 1 else 'user'  # Make the first user admin
        )
        user.set_password(form.password.data)
        user.save()
        flash('You are successfully registered!')
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            # Debugging information for form errors
            print("Form Errors:", form.errors)
            print("Form Data:", form.data)
            print("CSRF Token:", form.csrf_token.data)
            print("Request Method:", request.method)

    return render_template('register.html', form=form)

@app.route('/product', methods=['GET'])
def product():
    """
    Render the product list page.
    """
    products = Product.objects.order_by('-product_id')
    return render_template('product.html', products=products)

@app.route('/order', methods=['POST', 'GET'])
def order():
    """Handle the shopping cart and order process"""
    if not session.get('username'):
        flash('Please login first to see your shopping cart', 'error')
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    product_id = request.form.get('product_id')
    if product_id:
        order = Order.objects(user_id=user_id, product_id=product_id).first()
        if order:
            quantity = int(request.form.get('quantity', 1))
            if request.form.get('todo') == 'add':
                order.update(inc__quantity=1)
            elif request.form.get('todo') == 'subtract':
                if order.quantity == 1:
                    order.delete()
                else:
                    order.update(dec__quantity=1)
            elif request.form.get('todo') == 'delete':
                order.delete()
        else:
            Order(user_id=user_id, product_id=product_id, quantity=1).save()

    orders = shoppingcart(user_id)
    subtotal = sum(item['r1']['quantity'] * item['r2']['price'] for item in orders)
    return render_template('order.html', orders=orders, subtotal=subtotal)

@app.route('/logout')
def logout():
    """
    Handle user logout.
    """
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """
    Render the admin page and handle setting the record of the week.
    """
    if not session.get('username') or session.get('user_id') != 1:
        return redirect(url_for('index'))

    products = Product.objects.all()
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        message = request.form.get('message')

        # Get the selected product
        selected_product = Product.objects(product_id=product_id).first()

        if selected_product:
            # Save the record of the week
            record_of_the_week = RecordOfTheWeek(
                product_id=selected_product.product_id,
                message=message
            )
            record_of_the_week.save()
            flash("Record of the Week updated successfully!", "success")
        else:
            flash("Invalid product selection.", "error")

        return redirect(url_for('admin'))

    return render_template('admin.html', products=products)