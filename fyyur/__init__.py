from flask import Flask, render_template
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import logging
from logging import Formatter, FileHandler
import babel
from fyyur.config import Config
import dateutil.parser
# configuration of the app

app = Flask(__name__)
moment = Moment(app)
app.config.from_object(Config)
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')
#************************************************************************
# Handle my blueprints
#************************************************************************
# import my blueprints 
from fyyur.main.routes import main
from fyyur.venues.routes import venues_bluebrint
from fyyur.artists.routes import artists_blueprint
from fyyur.shows.routes import shows_blueprint
# register my blueprints 
app.register_blueprint(main)
app.register_blueprint(venues_bluebrint)
app.register_blueprint(artists_blueprint)
app.register_blueprint(shows_blueprint)