import os
import uuid


TEMPLATES_NAMES_MAPPING = {
    'index': 'main.html',
    'cart': 'cart.html',
    'account': 'account.html',
    'auth': 'auth.html',
    'register': 'login.html',
    'login': 'login.html',
    'logout': 'login.html',
    'ordered': 'ordered.html',
}

# Database credentials
DB_TYPE = 'sqlite'
DB_TYPE = os.environ.get('DB_TYPE', DB_TYPE)
DB_HOST = 'localhost'
DB_HOST = os.environ.get('DB_HOST', DB_HOST)
DB_PORT = 5432
DB_PORT = os.environ.get('DB_PORT', DB_PORT)
DB_USER = 'pik'
DB_USER = os.environ.get('DB_USER', DB_USER)
DB_PASSWORD = '123'
DB_PASSWORD = os.environ.get('DB_PASSWORD', DB_PASSWORD)
DB_NAME = 'delivery.db'
DB_NAME = os.environ.get('DB_NAME', DB_NAME)

# Server credentials
SERVER_HOST = 'localhost'
SERVER_HOST = os.environ.get('SERVER_HOST', SERVER_HOST)
SERVER_PORT = 5000
SERVER_PORT = os.environ.get('SERVER_PORT', SERVER_PORT)

# Security
CSRF_TOKEN = str(uuid.uuid4())
CSRF_TOKEN = os.environ.get('CRSF_TOKEN', CSRF_TOKEN)

# Admin
ADMIN_LOGIN = 'admin@delivery.com'
ADMIN_LOGIN = os.environ.get('ADMIN_LOGIN', ADMIN_LOGIN)
ADMIN_PASSWORD = str(uuid.uuid4())
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', ADMIN_PASSWORD)


class OrderStatus:
    in_progress = 'in_progress'
    done = 'done'
    canceled = 'canceled'


DATETIME_TEMPLATE = '%d/%m/%y %H:%M:%S'
