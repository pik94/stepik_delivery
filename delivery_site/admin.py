from flask import url_for, redirect
from flask_admin import expose, BaseView
from flask_admin.contrib.sqla import ModelView


class UserAdmin(ModelView):
    column_exclude_list = ['password', ]


class OrderAdmin(ModelView):
    pass


class MealAdmin(ModelView):
    pass
