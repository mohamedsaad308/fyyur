from fyyur import db
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    genres = db.Column(db.String(120))
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website =  db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # past_shows_count = db.Column(db.Integer, nullable=False)
    # upcoming_shows_count = db.Column(db.Integer, nullable=False)
    # Done: implement any missing fields, as a database migration using Flask-Migrate
    shows_venue = db.relationship('Show', backref='venue', lazy=True)
    def __repr__(self):
      return f"Venue ID: {self.id} Venue name: {self.name}"

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    genres = db.Column(db.String(120))
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    website =  db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # past_shows_count = db.Column(db.Integer, nullable=False)
    # upcoming_shows_count = db.Column(db.Integer, nullable=False)

    # Done: implement any missing fields, as a database migration using Flask-Migrate
    shows_artist = db.relationship('Show', backref='artist', lazy=True)
    def __repr__(self):
      return f"Artist ID: {self.id} Artist name: {self.name}"
# Done Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime(), nullable = False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable = False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable = False)
  def __repr__(self):
    return f'{self.id}: Show starts at {self.start_time}'