from flask import Flask

from delivery_site import config as cfg
from delivery_site.database import db_model, get_connection_string


app = Flask(__name__, template_folder='templates')
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = get_connection_string()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = cfg.CSRF_TOKEN

db_model.init_app(app)
# app.app_context().push()
with app.app_context():
    db_model.create_all()
