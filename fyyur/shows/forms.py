from flask_wtf import Form 
from wtforms.validators import DataRequired, AnyOf, URL, ValidationError
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, IntegerField
from fyyur.models import Show
from datetime import datetime

class ShowForm(Form):
    artist_id = IntegerField(
        'artist_id'
    )
    venue_id = IntegerField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )
    def validate_artist_id(self, artist_id):
        if not Artist.query.get(artist_id.data):
            raise ValidationError(f'Artist with ID = {artist_id.data} does not exist')
    def validate_venue_id(self, venue_id):
        if not Venue.query.get(venue_id.data):
            raise ValidationError(f'Venue with ID = {venue_id.data} does not exist ')
    def validate_start_time(self, start_time):
        if start_time.data <= datetime.now():
            raise ValidationError('Show should be in the future!')

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM