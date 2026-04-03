from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

# DB connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="dataforge"
)
cursor = db.cursor(dictionary=True)


# ---------------- LOGIN ----------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            session['user'] = user['username']
            return redirect('/dashboard')
        else:
            return "Invalid Login ❌"

    return render_template('login.html')


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')

    # Total customers
    cursor.execute("SELECT COUNT(*) as count FROM customers")
    total_customers = cursor.fetchone()['count']

    # Total products
    cursor.execute("SELECT COUNT(*) as count FROM products")
    total_products = cursor.fetchone()['count']

    # Total orders
    cursor.execute("SELECT COUNT(*) as count FROM orders")
    total_orders = cursor.fetchone()['count']

    # Total revenue
    cursor.execute("SELECT IFNULL(SUM(total_amount),0) as revenue FROM orders")
    total_revenue = cursor.fetchone()['revenue']

    return render_template(
        'dashboard.html',
        total_customers=total_customers,
        total_products=total_products,
        total_orders=total_orders,
        total_revenue=total_revenue
    )


# ---------------- CUSTOMERS ----------------
@app.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cursor.execute(
            "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)",
            (name, email, phone)
        )
        db.commit()

    cursor.execute("SELECT * FROM customers")
    data = cursor.fetchall()
    return render_template('customers.html', customers=data)


# ---------------- PRODUCTS ----------------
@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        stock = request.form['stock']

        cursor.execute(
            "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)",
            (name, price, stock)
        )
        db.commit()

    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()
    return render_template('products.html', products=data)


# ---------------- CREATE ORDER ----------------
@app.route('/create_order', methods=['GET', 'POST'])
def create_order():
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])

        # Get product price
        cursor.execute("SELECT price, stock FROM products WHERE id=%s", (product_id,))
        product = cursor.fetchone()

        if product['stock'] < quantity:
            return "Not enough stock ❌"

        total = product['price'] * quantity

        # Create order
        cursor.execute(
            "INSERT INTO orders (customer_id, total_amount) VALUES (%s, %s)",
            (customer_id, total)
        )
        db.commit()

        order_id = cursor.lastrowid

        # Insert order item
        cursor.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
            (order_id, product_id, quantity, product['price'])
        )

        # Update stock
        cursor.execute(
            "UPDATE products SET stock = stock - %s WHERE id=%s",
            (quantity, product_id)
        )

        db.commit()

        return redirect('/orders')

    return render_template('orders.html', customers=customers, products=products)


# ---------------- VIEW ORDERS ----------------
@app.route('/orders')
def orders():
    query = """
    SELECT o.id, c.name as customer, o.total_amount, o.order_date
    FROM orders o
    JOIN customers c ON o.customer_id = c.id
    ORDER BY o.order_date DESC
    """
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template('orders.html', orders=data)


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)