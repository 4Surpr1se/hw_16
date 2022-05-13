from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

db = SQLAlchemy(app)


def user_add(users_list):
    list_to_add = []
    for user in users_list:
        list_to_add.append(User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role=user['role'],
            phone=user['phone']
        ))

    db.session.add_all(list_to_add)
    db.session.commit()


def user_dict_form(user_object):
    return {
        "id": user_object.id,
        "first_name": user_object.first_name,
        "last_name": user_object.last_name,
        "age": user_object.age,
        "email": user_object.email,
        "role": user_object.role,
        "phone": user_object.phone
    }


def order_add(orders_list):
    list_to_add = []
    for order in orders_list:
        list_to_add.append(Order(
            id=order['id'],
            name=order['name'],
            description=order['description'],
            start_date=order['start_date'],
            end_date=order['end_date'],
            address=order['address'],
            price=order['price'],
            customer_id=order['customer_id'],
            executor_id=order['executor_id']
        ))

    db.session.add_all(list_to_add)
    db.session.commit()


def order_dict_form(order_object):
    return {
        "id": order_object.id,
        "name": order_object.name,
        "description": order_object.description,
        "start_date": order_object.start_date,
        "end_date": order_object.end_date,
        "address": order_object.address,
        "price": order_object.price,
        "customer_id": order_object.customer_id,
        "executor_id": order_object.executor_id
    }


def offer_add(offers_list):
    list_to_add = []
    for offer in offers_list:
        list_to_add.append(Offer(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id']
        ))

    db.session.add_all(list_to_add)
    db.session.commit()


def offer_dict_form(offer_object):
    return {
        "id": offer_object.id,
        "order_id": offer_object.order_id,
        "executor_id": offer_object.executor_id
    }


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)


class Order(db.Model):
    """start_date и end_date не Date типа потому что выпадала ошибка
     sqlalchemy.exc.StatementError:
    (builtins.TypeError) SQLite DateTime type only accepts Python datetime and date objects as input.
    """
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.String)
    executor_id = db.Column(db.String)
    offer = db.relationship("Offer")


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship("Order")
    executor_id = db.Column(db.Integer)


db.create_all()


@app.route("/users")
def get_all_users():
    result = []
    users = User.query.all()
    for user in users:
        result.append(user_dict_form(user))
    return jsonify(result)


@app.route("/users/<int:gid>", methods=['GET'])
def get_one_user(gid):
    user = User.query.get(gid)
    return jsonify(user_dict_form(user))


@app.route("/users", methods=['POST'])
def create_user(data=None):
    if not data:
        data = request.json
    user = User(
        first_name=data.get('name'),
        last_name=data.get('last_name'),
        age=data.get('age'),
        email=data.get('email'),
        role=data.get('role'),
        phone=data.get('phone')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user_dict_form(user))


@app.route("/users/<int:gid>", methods=['PUT'])
def update_user(gid):
    data = request.get_json()
    user = User.query.get(gid)
    if user != None:
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.age = data.get('age')
        user.email = data.get('email')
        user.role = data.get('role')
        user.phone = data.get('phone')

        db.session.add(user)
        db.session.commit()

        return jsonify({"status": "updated"})
    create_user(data)
    return jsonify({"status": "created"})


@app.route("/users/<int:gid>", methods=['DELETE'])
def delete_user(gid):
    user = User.query.get(gid)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"status": "deleted"})


# ---------------------------------------------------------

@app.route("/orders")
def get_all_orders():
    result = []
    orders = Order.query.all()
    for order in orders:
        result.append(order_dict_form(order))
    return jsonify(result)


@app.route("/orders/<int:gid>", methods=['GET'])
def get_one_order(gid):
    order = Order.query.get(gid)
    return jsonify(order_dict_form(order))


@app.route("/orders", methods=['POST'])
def create_order(data=None):
    if not data:
        data = request.json
    order = Order(
        name=data.get('name'),
        description=data.get('description'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        address=data.get('address'),
        price=data.get('price'),
        customer_id=data.get('customer_id'),
        executor_id=data.get('executor_id')
    )
    db.session.add(order)
    db.session.commit()
    return jsonify(order_dict_form(order))


@app.route("/orders/<int:gid>", methods=['PUT'])
def update_order(gid):
    data = request.get_json()
    order = Order.query.get(gid)
    if order != None:
        order.name = data.get('name')
        order.description = data.get('description')
        order.start_date = data.get('start_date')
        order.end_date = data.get('end_date')
        order.address = data.get('address')
        order.price = data.get('price')
        order.customer_id = data.get('customer_id')
        order.executor_id = data.get('executor_id')

        db.session.add(order)
        db.session.commit()

        return jsonify({"status": "updated"})
    create_order(data)
    return jsonify({"status": "created"})


@app.route("/orders/<int:gid>", methods=['DELETE'])
def delete_order(gid):
    order = Order.query.get(gid)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"status": "deleted"})


# ---------------------------------------------------------

@app.route("/offers")
def get_all_offers():
    result = []
    offers = Offer.query.all()
    for offer in offers:
        result.append(offer_dict_form(offer))
    return jsonify(result)


@app.route("/offers/<int:gid>", methods=['GET'])
def get_one_offer(gid):
    offer = Offer.query.get(gid)
    return jsonify(offer_dict_form(offer))


@app.route("/offers", methods=['POST'])
def create_offer(data=None):
    if not data:
        data = request.json
    offer = Offer(
        order_id=data.get('order_id'),
        executor_id=data.get('executor_id'),
    )
    db.session.add(offer)
    db.session.commit()
    return jsonify(offer_dict_form(offer))


@app.route("/offers/<int:gid>", methods=['PUT'])
def update_offer(gid):
    data = request.get_json()
    offer = Offer.query.get(gid)
    if offer != None:
        offer.order_id = data.get('order_id')
        offer.executor_id = data.get('executor_id')

        db.session.add(offer)
        db.session.commit()

        return jsonify({"status": "updated"})
    create_offer(data=data)
    return jsonify({"status": "created"})


@app.route("/offers/<int:gid>", methods=['DELETE'])
def delete_offer(gid):
    offer = Offer.query.get(gid)
    db.session.delete(offer)
    db.session.commit()
    return jsonify({"status": "deleted"})


# ---------------------------------------------------------

if __name__ == '__main__':
    with open('users.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        user_add(data)

    with open('orders.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        order_add(data)

    with open('offers.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        offer_add(data)

    app.run()
