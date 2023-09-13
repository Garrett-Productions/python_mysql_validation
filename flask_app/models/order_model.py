from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Order:
    DB = "cookie_orders_validation"
    def __init__( self, db_data ):
        self.id = db_data['id']
        self.customer_name = db_data['customer_name']
        self.cookie_type = db_data['cookie_type']
        self.num_of_boxes = db_data['num_of_boxes']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']


    @staticmethod
    def validate_order(order):
        is_valid = True # we assume this is true
        if len(order['customer_name']) < 2:
            flash("Name input is Mandatory")
            is_valid = False
        if len(order['cookie_type']) < 3:
            flash("Please insert the type of cookie")
            is_valid = False
        if len(order['num_of_boxes']) < 1:
            flash("How many did you order?")
            is_valid = False
        return is_valid


    @classmethod
    def save( cls , data ):
        query = "INSERT INTO Orders (customer_name, cookie_type, num_of_boxes, created_at, updated_at ) VALUES (%(customer_name)s, %(cookie_type)s, %(num_of_boxes)s,NOW(),NOW());"
        return connectToMySQL(cls.DB).query_db(query,data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM Orders;"
        cookie_orders_validation =  connectToMySQL(cls.DB).query_db(query)
        orders =[]
        for summary in cookie_orders_validation:
            orders.append(cls(summary))
        return orders


    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM Orders WHERE orders.id = %(id)s;"
        cookie_orders_validation = connectToMySQL(cls.DB).query_db(query,data)
        return cls(cookie_orders_validation[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE Orders SET customer_name=%(customer_name)s, cookie_type=%(cookie_type)s, num_of_boxes=%(num_of_boxes)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query,data)