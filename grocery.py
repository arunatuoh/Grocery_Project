from email.policy import strict
from itertools import product
from attr import fields
from flask import Flask, request, jsonify
from flask_restplus import Resource, Api
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String


app = Flask(__name__)
app.config["SECRET_KEY"] = "arunkumarsingh"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://arunsingh:emppassword@localhost/dummydb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


class Products(db.Model):
    __tablename__ = "products"
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    uom_id = db.Column(db.Integer, db.ForeignKey('uom.uom_id'))
    uom = db.relationship("Uom", backref="uom")
    price_per_unit = db.Column(db.Integer)


class Uom(db.Model):
    __tablename__ = "uom"
    uom_id = db.Column(db.Integer, primary_key = True)
    name_of_uom = db.Column(db.String(50))
     
     
class Orders(db.Model):
    __tablename__ = "orders"
    order_id =db.Column(db.Integer, primary_key=True)
    costomer_name = db.Column(db.String(50))
    total = db.Column(db.Integer)
    datetime = db.Column(db.String(50))


class Details_Order(db.Model):
    __tablename__ = "order_details"
    order_details_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    quantites = db.Column(db.Integer)
    Total_price =db.Column(db.Integer)
    
#here is the Schema of all the table 
class ProductsSchema(ma.ModelSchema):
    class Meta:
        model = Products


class UomSchema(ma.ModelSchema):
    class Meta:
        model = Uom


class  OrdersSchema(ma.ModelSchema):
    class Meta:
        model = Orders
        

class Details_OrdersSchema(ma.ModelSchema):
    class Meta:
        model = Details_Order


# this function will display all the products from the database
@api.route("/products")
class Products_(Resource):
    def get(self):
        all_prod = Products.query.all()
        prod_schema = ProductsSchema(many=True).dump(all_prod)
        return prod_schema
    
    
    # this function will post a product data into database
    def post(self):
        products = Products(
            product_id = request.json["product_id"],
            name = request.json["name"],
            uom_id = request.json["uom_id"],
            price_per_unit = request.json["price_per_unit"]
        )
        db.session.add(products)
        db.session.commit()
        return "add succesfullly" 

# this route will display the single products from the database
@api.route("/single_prod/<int:id>")
class  Product_(Resource):
    def get(self,id):
        data_ = Products.query.get(id)
        data_schema = ProductsSchema().dump(data_)
        return (data_schema)
    
    
    # this function will delete the single product from the database
    def delete(self, id):
        """this function is used to delete a single employee details"""
        products = Products.query.get_or_404(id)
        db.session.delete(products)
        db.session.commit()
        return "product deleted"
    
    
    # this function will update the existing products details from database
    def patch(self, id):
        """this function is used to update an employee details"""
        product = Products.query.get_or_404(id)
        if "product_id" in request.json:
            product.product_id = request.json["product_id"]
        if "name" in request.json:
            product.name = request.json["name"]
        if "uom_id" in request.json:
            product.uom_id = request.json["uom_id"]
        if "price_per_unit" in request.json:
            product.price_per_unit = request.json["price_per_unit"]
        db.session.commit()
        return ProductsSchema().dump(product)
        

# this route will display the all unit of measurement from the database
@api.route("/units")
class  Uom_(Resource):
    def get(self):
        all_uom = Uom.query.all()
        uom_schema = UomSchema(many=True).dump(all_uom)
        return uom_schema

    
    # this function will post the unit of measurment into database
    def post(self):
        um = Uom(
            uom_id = request.json["uom_id"],
            name_of_uom = request.json["name_of_uom"]
        )        
        db.session.add(um)
        db.session.commit()
        return UomSchema().dump(um)


# this route will display the single Unit of measurement from database
@api.route("/single_uom/<int:id>")
class  Uom_(Resource):
    def get(self,id):
        data_ = Uom.query.get(id)
        data_schema = UomSchema().dump(data_)
        return (data_schema)
    
    
    # this function will delete the single UOM from the database
    def delete(self, id):
        """this function is used to delete a single employee details"""
        uom = Uom.query.get_or_404(id)
        db.session.delete(uom)
        db.session.commit()
        return "Uom deleted"


# this route will display the all order form the database
@api.route("/orders")
class Orders_(Resource):
    def get(self):
        all_orders = Orders.query.all()
        order_schema = OrdersSchema(many=True).dump(all_orders)
        return order_schema
    
    
    # this function will post a order into database
    def post(self):
        order = Orders(
            order_id = request.json["order_id"],
            costomer_name = request.json["costomer_name"],
            total = request.json["total"],
            datetime = request.json["datetime"]
        )        
        db.session.add(order)
        db.session.commit()
        return UomSchema().dump(order)


# this route will display the single order data from database
@api.route("/single_ord/<int:id>")
class  Order_(Resource):
    def get(self,id):
        data_ = Orders.query.get(id)
        data_schema = OrdersSchema().dump(data_)
        return (data_schema)
    
    
    # this function will delete the single ORDERS from the database
    def delete(self, id):
        """this function is used to delete a single employee details"""
        ord = Orders.query.get_or_404(id)
        db.session.delete(ord)
        db.session.commit()
        return "Orders deleted"


# this route will display the all order_details from the databse 
@api.route("/order_details")
class Order_details(Resource):
    def ord_details(self):
        all_od = Details_Order.query.all()
        od_schema = Details_OrdersSchema(many=True).dump(all_od)
        return od_schema
    
    
    # this function will post the order details into database
    def post(self):
        od = Details_Order(
            order_details_id = request.json["order_details_id"],
            order_id = request.json["order_id"],
            product_id = request.json["product_id"],
            quantites = request.json["quantites"],
            Total_price = request.json["Total_price"]
            
        )
        db.session.add(od)
        db.session.commit()
        return Details_OrdersSchema().dump(od)    


# this route will display the single order details from database
@api.route("/single_ord_details/<int:id>")
class  Details_order_(Resource):
    def get(self,id):
        data_ = Details_Order.query.get(id)
        data_schema = Details_OrdersSchema().dump(data_)
        return (data_schema)
    
    
    # this function will delete the single order_details from the database
    def delete(self, id):
        """this function is used to delete a single employee details"""
        od = Orders.query.get_or_404(id)
        db.session.delete(od)
        db.session.commit()
        return "Orders details deleted"


# From there we will see the funtion baesd on join query join Query 
# this route will return the all data from both of the table products and order
@api.route("/prod_ord")
class Prod_ord(Resource):
    def get(self):
        all_data = Products.query.add_columns(Products.name, Products.price_per_unit, Products.product_id,
                                            Uom.name_of_uom, Uom.uom_id) \
                                            .join(Uom, Uom.uom_id == Products.uom_id) \
                                            .all()
        prod_schema = ProductsSchema(many=True).dump(all_data)
        uom_schema = UomSchema(many=True).dump(all_data)
        for (prod, uom) in zip(prod_schema.data, uom_schema.data):
            prod.update(uom)
        return prod_schema
    
if __name__ == "__main__":
    app.run(debug=True)