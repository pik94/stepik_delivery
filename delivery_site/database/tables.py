class USERS:
    SELF_NAME = 'users'
    ID = 'id'
    EMAIL = 'email'
    PASSWORD = 'password'
    IS_LOGGED = 'is_logged'


class MEALS:
    SELF_NAME = 'meals'
    ID = 'id'
    TITLE = 'title'
    PRICE = 'price'
    DESCRIPTION = 'description'
    PICTURE = 'picture'
    CATEGORY_ID = 'category_id'


class CATEGORIES:
    SELF_NAME = 'categories'
    ID = 'id'
    TITLE = 'title'


class ORDERS:
    SELF_NAME = 'orders'
    ID = 'id'
    DATE = 'date'
    NAME = 'name'
    ORDER_PRICE = 'order_price'
    STATUS = 'status'
    EMAIL = 'email'
    PHONE = 'phone'
    ADDRESS = 'address'
    USER_ID = 'user_id'


class ORDERS_MEALS:
    SELF_NAME = 'orders_meals'
    ORDER_ID = 'order_id'
    MEAL_ID = 'meal_id'
