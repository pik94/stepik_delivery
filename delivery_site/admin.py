from flask_admin.contrib.sqla import ModelView


class UserAdmin(ModelView):
    column_exclude_list = ['password', ]


class OrderAdmin(ModelView):
    pass


class MealAdmin(ModelView):
    pass
