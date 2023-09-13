from flask import render_template,redirect,request
from flask_app import app
from flask_app.models.order_model import Order

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/cookies/', methods=['POST'])
def show_cookies():
    if not Order.validate_order(request.form):
        #if there are errors then redirect back to our form
        return redirect ('/')
        #no errors, capture info into a dictionary and save the data and redirect elsewhere
        
    data = {
        "customer_name": request.form['customer_name'],
        "cookie_type": request.form['cookie_type'],
        "num_of_boxes": request.form['num_of_boxes']
    }
    Order.save(data)
    return redirect('/show_orders') #redirect to a route that displays all_orders.html


@app.route('/show_orders')
def show_orders():
    return render_template("all_orders.html", orders = Order.get_all())

@app.route('/edit_order/<int:order_id>')
def edit_page(order_id):
    data = {
        'id': order_id
    }
    order = Order.get_one(data)
    return render_template("edit_order.html", order = order)


@app.route('/update/<int:order_id>', methods=['POST'])
def update(order_id):
    if not Order.validate_order(request.form):
        #if there are errors then redirect back to our form
        return redirect (f'/edit_order/{order_id}')
        #no errors, capture info into a dictionary and save the data and redirect elsewhere
    data = {
        'id': order_id,
        "customer_name":request.form['customer_name'],
        "cookie_type": request.form['cookie_type'],
        "num_of_boxes": request.form['num_of_boxes'],
    }
    Order.update(data)
    data2 = {
        'id': order_id
    }
    order = Order.get_one(data2)
    return redirect("/show_orders")