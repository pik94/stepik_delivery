import datetime as dt
from typing import Dict, List, Union

from flask import redirect, render_template, request, session, url_for
from flask.views import View

from delivery_site import config as cfg
from delivery_site.database import db_model, Category, Meal, Order, User
from delivery_site.forms import LoginForm, RegisterForm, OrderSubmitForm


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


class CartPage(Base):
    methods = ['GET', 'POST']

    def dispatch_request(self) -> str:
        form = OrderSubmitForm()
        if request.method == 'POST' and form.validate_on_submit():
            name = form.name.data
            address = form.address.data
            email = form.email.data
            phone = form.phone.data
            order_price = form.order_price.data

            user = db_model.session.query(User).filter(User.email==email).first()
            if user:
                user_id = user.id
            else:
                user_id = 0

            order = Order(date=dt.datetime.utcnow().replace(microsecond=0),
                          order_price=order_price,
                          name=name,
                          email=email,
                          phone=phone,
                          address=address,
                          status=cfg.OrderStatus.in_progress,
                          user_id=user_id)

            db_model.session.add(order)
            db_model.session.commit()

            session['cart'] = []
            return redirect(url_for('ordered'))

        cart = session.get('cart', [])
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
        rows = db_model.session.query(Meal).filter(Meal.id.in_(meal_ids)).all()
        meals = {row.id: row for row in rows}
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


class AccountPage(Base):
    def dispatch_request(self) -> str:
        # TODO: handle exceptions

        user_id = session.get('id')
        if user_id is None:
            return redirect(url_for('login'))

        user = User.query.get(user_id)
        orders = user.orders

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
        if request.method == 'GET' or form.validate_on_submit():
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
        if request.method == 'GET' or form.validate_on_submit():
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
        session.pop('id')
        session.pop('email')
        return redirect(url_for('login'))


class OrderedPage(View):
    def dispatch_request(self) -> str:
        # TODO: handle exceptions

        return render_template(cfg.TEMPLATES_NAMES_MAPPING['ordered'],
                               session=session)
