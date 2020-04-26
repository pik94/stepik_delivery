from werkzeug.security import check_password_hash, generate_password_hash

from delivery_site.database.database import db
from delivery_site.database.tables import (
    CATEGORIES, MEALS, ORDERS, ORDERS_MEALS, USERS
    )


orders_meals_association = db.Table(
    ORDERS_MEALS.SELF_NAME,
    db.Column(ORDERS_MEALS.ORDER_ID, db.Integer,
              db.ForeignKey(f'{ORDERS.SELF_NAME}.{ORDERS.ID}')),
    db.Column(ORDERS_MEALS.MEAL_ID, db.Integer,
              db.ForeignKey(f'{MEALS.SELF_NAME}.{MEALS.ID}'))
)


class User(db.Model):
    __tablename__ = USERS.SELF_NAME

    id = db.Column(USERS.ID, db.Integer, primary_key=True)
    email = db.Column(USERS.EMAIL, db.String, unique=True, nullable=False)
    password = db.Column(USERS.PASSWORD, db.String, nullable=False)

    orders = db.relationship('Order', back_populates='user')

    @staticmethod
    def hash_password(password: str) -> str:
        return generate_password_hash(password)

    def is_valid_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)


class Meal(db.Model):
    __tablename__ = MEALS.SELF_NAME

    id = db.Column(MEALS.ID, db.Integer, primary_key=True)
    title = db.Column(MEALS.TITLE, db.String, nullable=False)
    price = db.Column(MEALS.PRICE, db.Float, nullable=False)
    description = db.Column(MEALS.DESCRIPTION, db.String, nullable=False)
    picture = db.Column(MEALS.PICTURE, db.String, nullable=False)
    category_id = db.Column(
        MEALS.CATEGORY_ID, db.Integer,
        db.ForeignKey(f'{CATEGORIES.SELF_NAME}.{CATEGORIES.ID}'))
    category = db.relationship('Category', uselist=False,
                               back_populates='meals')
    orders = db.relationship('Order', secondary=orders_meals_association,
                             back_populates='meals')


class Category(db.Model):
    __tablename__ = CATEGORIES.SELF_NAME

    id = db.Column(CATEGORIES.ID, db.Integer, primary_key=True)
    title = db.Column(CATEGORIES.TITLE, db.String, nullable=False)

    meals = db.relationship('Meal', back_populates='category')


class Order(db.Model):
    __tablename__ = ORDERS.SELF_NAME

    id = db.Column(ORDERS.ID, db.Integer, primary_key=True)
    date = db.Column(ORDERS.DATE, db.DateTime, nullable=False)
    name = db.Column(ORDERS.NAME, db.String, nullable=False)
    order_price = db.Column(ORDERS.ORDER_PRICE, db.Float, nullable=False)
    email = db.Column(ORDERS.EMAIL, db.String, nullable=False)
    phone = db.Column(ORDERS.PHONE, db.String, nullable=False)
    address = db.Column(ORDERS.ADDRESS, db.String, nullable=False)
    status = db.Column(ORDERS.STATUS, db.String, nullable=False)
    user_id = db.Column(ORDERS.USER_ID, db.Integer,
                        db.ForeignKey(f'{USERS.SELF_NAME}.{USERS.ID}'))

    user = db.relationship('User', uselist=False, back_populates='orders')
    meals = db.relationship('Meal', secondary=orders_meals_association,
                            back_populates='orders')



