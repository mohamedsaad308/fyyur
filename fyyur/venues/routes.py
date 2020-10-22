from flask import Blueprint, render_template, request, Response, flash, redirect, url_for
from fyyur.models import Venue, Artist, Show
from fyyur.venues.forms import VenueForm
from fyyur import db
import psycopg2
import sys
from datetime import datetime

venues_bluebrint = Blueprint('venues', __name__)

@venues_bluebrint.route('/venues', methods=['GET'])
def venues():
  # Done: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  locals = []
  venues = Venue.query.all()
  for place in Venue.query.distinct(Venue.city, Venue.state).all():
      locals.append({
          'city': place.city,
          'state': place.state,
          'venues': [{
              'id': venue.id,
              'name': venue.name,
          } for venue in venues if
              venue.city == place.city and venue.state == place.state]
      })
  return render_template('pages/venues.html', areas=locals)


@venues_bluebrint.route('/venues/search', methods=['POST'])
def search_venues():
  # Done: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  data = []
  search_term = request.form.get('search_term', '')
  results = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))
  count = results.count()
  for result in results:
    data.append({'id':result.id, 'name':result.name})

  response={
    "count": count,
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@venues_bluebrint.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # Done: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.filter_by(id=venue_id).first_or_404()
  # For past_shows:
  venue_shows = {}
  past_shows = db.session.query(Venue, Show).join(Show, Venue.id==Show.venue_id).\
    filter(Venue.id == venue_id,
          Show.start_time < datetime.now()).all()
  # For upcoming_shows:
  upcoming_shows = db.session.query(Venue, Show).join(Show, Venue.id==Show.venue_id).\
    filter(Venue.id == venue_id,
          Show.start_time > datetime.now()).all()
  
  venue_shows = {'past_shows':[{
              'artist_id': show.artist.id,
              'artist_name': show.artist.name,
              'artist_image_link': show.artist.image_link,
              "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
          } for venue, show in past_shows],
          'upcoming_shows': [{
              'artist_id': show.artist.id,
              'artist_name': show.artist.name,
              'artist_image_link': show.artist.image_link,
              'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
          } for venue, show in upcoming_shows],
          'past_shows_count': len(past_shows),
          'upcoming_shows_count': len(upcoming_shows)
                }
  return render_template('pages/show_venue.html', venue=venue, venue_shows=venue_shows)

#  Create Venue
#  ----------------------------------------------------------------

@venues_bluebrint.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@venues_bluebrint.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # Done: insert form data as a new Venue record in the db, instead
  # Done: modify data to be the data object returned from db insertion
  form = VenueForm(request.form)
  try:
    # validate form 
    if form.validate_on_submit():
      # check if venue name existed 
      venue = Venue.query.filter_by(name = form.name.data).first()
      if venue:
        # print('existed')
        flash(venue.name + ' Alread exists!', 'warning')
        return redirect(url_for('venues.create_venue_form'))
      venue = Venue()
      form.populate_obj(venue)
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + venue.name + ' was successfully listed!', 'success')
      return redirect(url_for('venues.show_venue', venue_id=venue.id))
    else:
      flash("Edit the following errors:", 'warning')
      for error in form.errors.values():
        flash(error[0], 'warning')
  except:
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('venues.create_venue_form'))

  # on successful db insert, flash success
  
  # Done: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@venues_bluebrint.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # DONE: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    venue = Venue.query.get(id)
    venue.delte()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

@venues_bluebrint.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  
  #get the venue by id
  venue = Venue.query.first_or_404(venue_id)
  #fill the form with current venue data
  form = VenueForm(obj=venue)

  # Done: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@venues_bluebrint.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # Done: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  #Update venue with user input
  form = VenueForm()
  venue= Venue.query.get(venue_id)
  try:
    print('we are on try')
    if form.validate_on_submit():
      print('form is valid')
      venue.name = form.name.data
      venue.website  = form.website.data
      venue.city=form.city.data
      venue.state=form.state.data
      venue.address = form.address.data
      venue.phone = form.phone.data
      venue.image_link = form.image_link.data
      venue.genres=form.genres.data
      venue.facebook_link=form.facebook_link.data
      db.session.commit()
      flash('Venue ' + venue.name + ' was successfully edited!', 'success')
  except:
    print('except')
    print(sys.exc_info())
    db.session.rollback()
  finally:
    print(form.errors)
    print('finally')
    db.session.close()
  return redirect(url_for('venues.show_venue', venue_id=venue_id))