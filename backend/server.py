import flask
from flask_cors import CORS
import structure
from database import db

from CONFIG import *

app = flask.Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

def create_app():
	app = flask.Flask(__name__)#static_folder="../dist/assets", template_folder="../dist"
	#app.secret_key = os.urandom(24)
	CORS(app, resources={r"/api/*": {"origins": "*"}, r"/auth/*": {"origins": "*"}})

	app.config.from_pyfile('config.cfg')
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + FOLDER + '/fetula.db'

	db.init_app(app)

	from api import api
	app.register_blueprint(api)

	return app


if __name__ == "__main__":
	app = create_app()
	structure.update(app)
	app.run(debug=True, threaded=True)