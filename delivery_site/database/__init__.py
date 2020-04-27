from delivery_site.database.database import db, get_connection_string
from delivery_site.database.models import (
    Category, Meal, Order, OrdersMeals, User
    )


db_model = db
