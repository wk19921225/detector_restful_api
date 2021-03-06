from flask import Flask, Blueprint
from werkzeug.middleware.proxy_fix import ProxyFix
from api.v1.endpoints import ns as v1
from api.restplus import api

from system import config


app = Flask(__name__)

# Middleware
app.wsgi_app = ProxyFix(app.wsgi_app)

# Initialize
blueprint = Blueprint("api", __name__, url_prefix="/api")
api.init_app(blueprint)

# Namespaces
api.add_namespace(v1)

# Blueprint Register
app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run(debug=config.FLASK_DEBUG, port=32123)
