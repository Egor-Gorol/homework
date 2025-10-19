from flask import Flask
from models import db, Customer, MenuItem, Order
from decimal import Decimal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


with app.app_context():
    db.create_all()

def add_customer(name, phone_number):
    new_customer = Customer(name=name, phone_number=phone_number)
    db.session.add(new_customer)
    db.session.commit()
    return new_customer


def add_menu_item(name, price):
    item = MenuItem(name=name, price=Decimal(price))
    db.session.add(item)
    db.session.commit()
    return item


def create_order(customer_id, item_ids):
    items = MenuItem.query.filter(MenuItem.id.in_(item_ids)).all()
    if not items:
        return None

    total = sum(item.price for item in items)
    order = Order(customer_id=customer_id, total_price=total)
    order.items = items
    db.session.add(order)
    db.session.commit()
    return order


def get_orders_by_customer(customer_id):
    orders = Order.query.filter_by(customer_id=customer_id).all()
    result = []
    for order in orders:
        result.append({
            'order_id': order.id,
            'total_price': float(order.total_price),
            'items': [item.name for item in order.items]
        })
    return result


if __name__ == '__main__':
    with app.app_context():

        if not Customer.query.first():
            c1 = add_customer("Іван Петренко", "380931112233")
            c2 = add_customer("Олена Коваленко", "380501234567")

            p1 = add_menu_item("Маргарита", 180)
            p2 = add_menu_item("Пепероні", 210)
            p3 = add_menu_item("4 Сири", 240)

            create_order(c1.id, [p1.id, p2.id])
            create_order(c2.id, [p3.id])


        print("Замовлення Івана:")
        orders = get_orders_by_customer(1)
        for o in orders:
            print(o)
