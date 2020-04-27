import datetime as dt
from itertools import groupby
from typing import Dict, List, Union

from flask import abort, redirect, render_template, request, session, url_for
from flask.views import View

from delivery_site import config as cfg
from delivery_site.database import db_model
from delivery_site.database.models import (
    Category, Meal, Order, OrdersMeals, User
    )
from delivery_site.forms import LoginForm, RegisterForm, OrderSubmitForm


class Admin(View):
    def dispatch_request(self) -> str:
        if session.get('id'):
            if session.get('is_admin'):
                return redirect('/admin_panel')
            else:
                abort(404)
        else:
            return redirect(url_for('login'))


class Base(View):
    def dispatch_request(self) -> str:
        pass

    def render_template(self, template: str, **kwargs) -> str:
        cart_size = len(session.get('cart', []))
        return render_template(cfg.TEMPLATES_NAMES_MAPPING[template],
                               n_meals=cart_size, session=session, **kwargs)


class IndexPage(Base):
    def dispatch_request(self) -> str:
        # TODO: handle exceptions

        data = Category.query.all()
        return self.render_template('index', data=data)


class AddToCart(View):
    def dispatch_request(self, meal_id: int) -> str:
        # TODO: handle exceptions
        cart = session.get('cart', [])
        cart.append(meal_id)
        session['cart'] = cart
        return redirect('/')


class DeleteFromCart(View):
    def dispatch_request(self, meal_id: int) -> str:
        cart = []
        removed = False
        for cart_meal_id in session.get('cart', []):
            if meal_id == cart_meal_id and not removed:
                removed = True
                continue
            cart.append(cart_meal_id)

        session['cart'] = cart

        return redirect(url_for('cart'))


class CartPage(Base):
    methods = ['GET', 'POST']

    def dispatch_request(self) -> str:
        cart = session.get('cart', [])
        form = OrderSubmitForm()

        if request.method == 'POST' and form.validate_on_submit():
            name = form.name.data
            address = form.address.data
            email = form.email.data
            phone = form.phone.data
            order_price = form.order_price.data

            user = db_model.session.query(User).filter(
                User.email == email).first()
            if user and session.get('id'):
                user_id = user.id
            else:
                user_id = None
                user = None

            meals = self.get_meals(cart)

            order_meal_list = [
                OrdersMeals(meal_quantity=len(list(id_group)),
                            meal=meals[meal_id])
                for meal_id, id_group in groupby(cart)
            ]

            order = Order(date=dt.datetime.utcnow().replace(microsecond=0),
                          order_price=order_price,
                          name=name,
                          email=email,
                          phone=phone,
                          address=address,
                          status=cfg.OrderStatus.in_progress,
                          user_id=user_id,
                          user=user,
                          meals=order_meal_list)

            db_model.session.add(order)
            db_model.session.commit()

            session['cart'] = []
            return redirect(url_for('ordered'))

        data = self.get_meal_data(cart)
        total_price = sum([datum['total_meal_price']
                           for datum in data.values()])

        return self.render_template('cart', form=form, data=data,
                                    order_price=total_price)

    def get_meal_data(self,
                      meal_ids: List[int]) -> \
            Dict[int, Dict[str, Union[int, float]]]:

        if not meal_ids:
            return {}

        # TODO: handle exceptions
        meals = self.get_meals(meal_ids)
        data = {}
        for meal_id in meal_ids:
            if meal_id not in data:
                data[meal_id] = {
                    'title': meals[meal_id].title,
                    'quantity': 1,
                    'total_meal_price': meals[meal_id].price
                }
            else:
                data[meal_id]['quantity'] += 1
                data[meal_id]['total_meal_price'] += meals[meal_id].price

        return data

    def get_meals(self, meal_ids: List[int]) -> Dict[int, Meal]:
        rows = db_model.session.query(Meal).filter(Meal.id.in_(meal_ids)).all()
        meals = {row.id: row for row in rows}
        return meals


class AccountPage(Base):
    def dispatch_request(self) -> str:
        # TODO: handle exceptions

        user_id = session.get('id')
        if user_id is None:
            return redirect(url_for('login'))

        orders = {}
        user = User.query.get(user_id)
        for order in user.orders:
            order_data = []
            total_order_price = 0
            for order_meal in order.meals:
                quantity = order_meal.meal_quantity
                data = {
                    'meal_title': order_meal.meal.title,
                    'meal_quantity': quantity,
                    'meal_total_price': quantity * order_meal.meal.price
                }
                total_order_price += quantity * order_meal.meal.price
                order_data.append(data)

            date = order.date.strftime(cfg.DATETIME_TEMPLATE)
            orders[(date, total_order_price)] = order_data

        return self.render_template('account', orders=orders)


class AuthBasePage(View):
    methods = ['GET', 'POST']

    template = ''
    title = ''

    def dispatch_request(self) -> str:
        pass

    def do_get(self, form: LoginForm, error: str) -> str:
        return render_template(cfg.TEMPLATES_NAMES_MAPPING[self.template],
                               title=self.title, template=self.template,
                               form=form, error=error)


class RegisterPage(AuthBasePage):
    methods = ['GET', 'POST']

    template = 'register'
    title = 'Создайте аккаунт'

    def dispatch_request(self) -> str:
        # TODO: handle exceptions
        form = RegisterForm()
        if request.method == 'GET' or not form.validate_on_submit():
            return self.do_get(form, '')

        else:
            email = form.email.data
            password = form.password.data

            user = db_model.session.query(User).filter(
                User.email == email).first()
            if user:
                error = 'Пользователь с таким email уже существует!'
            else:
                password = User.hash_password(password)
                user = User(email=email, password=password)
                db_model.session.add(user)
                db_model.session.commit()
                session['id'] = user.id
                session['email'] = email
                return redirect(url_for('account'))

            return self.do_get(form, error)


class LoginPage(AuthBasePage):
    methods = ['GET', 'POST']

    template = 'login'
    title = 'Войдите, чтобы управлять'

    def dispatch_request(self) -> str:
        # TODO: handle exceptions
        form = LoginForm()
        if request.method == 'GET' or not form.validate_on_submit():
            return self.do_get(form, '')

        else:
            email = form.email.data
            password = form.password.data

            user = db_model.session.query(User).filter(
                User.email == email).first()
            if user:
                if user.is_valid_password(password):
                    db_model.session.commit()
                    session['id'] = user.id
                    if user.email == cfg.ADMIN_LOGIN:
                        session['is_admin'] = True
                    session['email'] = email
                    return redirect(url_for('account'))
                else:
                    error = 'Неверный пароль'
            else:
                error = 'Нет такого пользователя'

            return self.do_get(form, error)


class LogoutPage(AuthBasePage):
    def dispatch_request(self) -> str:
        # TODO: handle exceptions
        for key in ['id', 'email', 'is_admin', 'cart']:
            if key in session:
                session.pop(key)
        return redirect(url_for('login'))


class OrderedPage(View):
    def dispatch_request(self) -> str:
        # TODO: handle exceptions

        return render_template(cfg.TEMPLATES_NAMES_MAPPING['ordered'],
                               session=session)
