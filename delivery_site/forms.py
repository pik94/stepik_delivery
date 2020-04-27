from flask import session
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField
from wtforms.validators import Email, InputRequired, Length


def check_order_price(form, field):
    if int(float(field.data)) == 0:
        raise ValueError('Вы ничего не заказали')


def check_user_email(form, field):
    """
    This method checks that a user writes his email when ordering.
    :param form:
    :param field:
    :return:
    """
    email = session.get('email')
    if email and email != field.data:
        raise ValueError('Используйте свой email')


class OrderSubmitForm(FlaskForm):
    name = StringField('Ваше имя', [InputRequired()],
                       render_kw={'placeholder': 'Иван'})
    address = StringField('Ваш адрес', [InputRequired()],
                          render_kw={'placeholder': 'Москва, ул. Моховая, 1'})
    email = StringField('Ваш e-mail',
                        [InputRequired(),
                         Email(message='Неверный формат email'),
                         check_user_email],
                        render_kw={'placeholder': 'ivan@ivan.com'})
    phone = StringField('Ваш номер', [InputRequired()],
                        render_kw={'placeholder': '+7(495)14234567'})
    order_price = HiddenField('order_price', validators=[check_order_price])
    submit = SubmitField('Оформить заказ')


class AuthForm(FlaskForm):
    email = StringField('Логин (email)',
                        [InputRequired(),
                         Email(message='Неверный формат email')])
    password = StringField('Пароль',
                           [InputRequired(),
                            Length(min=5, message=('В пароле должно быть '
                                                   'минимум 5 символов'))])


class LoginForm(AuthForm):
    submit = SubmitField('Войти')


class RegisterForm(AuthForm):
    submit = SubmitField('Зарегистрироваться')
