from flask import Blueprint, render_template, request, Response, flash, redirect, url_for
from fyyur.models import Venue
from fyyur.venues.forms import VenueForm
from fyyur import db
import psycopg2
from datetime import datetime

venues_bluebrint = Blueprint('venues', __name__)

@venues_bluebrint.route('/venues', methods=['GET'])
def venues():
  # Done: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  conn = psycopg2.connect(dbname='fyyur', user='postgres', password='2941')
  cur = conn.cursor()
  cur.execute('SELECT state, city From "Venue" GROUP BY (state, city);')
  state_city = cur.fetchall()
  data = []
  venues = []
  for state_city in state_city:
    city = state_city[1]
    state = state_city[0]
    cur.execute(f'''SELECT id, name from "Venue" where state='{state_city[0]}' AND city='{state_city[1]}';''')
    places = cur.fetchall()
    for place in places:
      id = place[0]
      name = place[1]
      venues.append({'id' : id, 'name' : name})
    data.append({'city': state_city[1],
                  'state' : state_city[0],
                  'venues' : venues})
    venues = []
  # print(data)
  conn.commit()
  cur.close()
  conn.close()
  return render_template('pages/venues.html', areas=data)


@venues_bluebrint.route('/venues/search', methods=['POST'])
def search_venues():
  # Done: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  data = []
  search_term = request.form.get('search_term', '')
  search_term_sql = f'%{search_term}%'
  conn = psycopg2.connect(dbname='fyyur', user='postgres', password='2941')
  cur = conn.cursor()
  cur.execute('SELECT id, name from "Venue" WHERE name ILIKE %s;', [search_term_sql])
  results = cur.fetchall()
  count = len(results)
  for result in results:
    data.append({'id':result[0], 'name':result[1]})
  conn.commit()
  cur.close()
  conn.close()

  response={
    "count": count,
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@venues_bluebrint.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # Done: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  venue_shows = {}
  
  venue_shows['past_shows_count'] = 0
  venue_shows['upcoming_shows_count'] = 0
  venue_shows['upcoming_shows'] = []
  venue_shows['past_shows'] = []
  for show in venue.shows_venue:
    if show.start_time > datetime.now():
      venue_shows['upcoming_shows_count'] += 1
      venue_shows['upcoming_shows'].append({'artist_name': show.artist.name,
                                            'start_time':show.start_time,
                                            'artist_image_link':  show.artist.image_link,
                                            'artist_id' : show.artist.id})
    else:
      venue_shows['past_shows_count'] += 1
      venue_shows['past_shows'].append({'artist_name': show.artist.name,
                                            'start_time':show.start_time,
                                            'artist_image_link':  show.artist.image_link,
                                            'artist_id' : show.artist.id})
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
  form = VenueForm()
  
  try:
    # validate form 
    if form.validate_on_submit():
      # check if venue name existed 
      venue = Venue.query.filter_by(name = form.name.data).first()
      if venue:
        # print('existed')
        flash(venue.name + ' Alread exists!', 'warning')
        return redirect(url_for('venues.create_venue_form'))
      new_venue = Venue(name=form.name.data,
                      city=form.city.data,
                      state=form.state.data,
                      address=form.address.data,
                      phone=form.phone.data,
                      image_link=form.image_link.data,
                      genres=form.genres.data,
                      facebook_link=form.facebook_link.data,
                      )
  
      db.session.add(new_venue)
      db.session.commit()
      flash('Venue ' + new_venue.name + ' was successfully listed!', 'success')
      return redirect(url_for('venues.show_venue', venue_id=new_venue.id))
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
  form = VenueForm()
  #get the venue by id
  venue= Venue.query.get(venue_id)
  #fill the form with current venue data 
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.genres.data = venue.genres
  form.facebook_link.data = venue.facebook_link
  form.image_link.data = venue.image_link
  form.website.data = venue.website

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