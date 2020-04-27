from flask import Flask
from flask_migrate import Migrate

from delivery_site import config as cfg
from delivery_site.database import db_model, get_connection_string
from delivery_site.views import (
    AccountPage, AddToCart, CartPage, IndexPage, LoginPage, LogoutPage,
    OrderedPage, RegisterPage
    )


app = Flask(__name__, template_folder='templates')
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = get_connection_string()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = cfg.CSRF_TOKEN


db_model.init_app(app)

migrate = Migrate(app, db_model)

# index page
app.add_url_rule('/', view_func=IndexPage.as_view('index'))

# add to cart page
app.add_url_rule('/addtocart/<int:meal_id>',
                 view_func=AddToCart.as_view('addtocart'))

# cart page
app.add_url_rule('/cart', view_func=CartPage.as_view('cart'))

# account page
app.add_url_rule('/account', view_func=AccountPage.as_view('account'))

# login page
app.add_url_rule('/login', view_func=LoginPage.as_view('login'))

# register page
app.add_url_rule('/register', view_func=RegisterPage.as_view('register'))

# logout page
app.add_url_rule('/logout', view_func=LogoutPage.as_view('logout'))

# ordered page
app.add_url_rule('/ordered', view_func=OrderedPage.as_view('ordered'))
