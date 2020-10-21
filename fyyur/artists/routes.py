from flask import Blueprint, render_template, request, Response, flash, redirect, url_for
from fyyur.models import Artist
from fyyur.artists.forms import ArtistForm
from fyyur import db
from datetime import datetime

artists_blueprint = Blueprint('artists', __name__)

@artists_blueprint.route('/artists')
def artists():
  # DONE: replace with real data returned from querying the database
  artist = Artist.query.all()
  return render_template('pages/artists.html', artists=artist)


@artists_blueprint.route('/artists/search', methods=['POST'])
def search_artists():
  # Done: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  data = []
  search_term = request.form.get('search_term', '')
  results = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))
  count = results.count()
  for result in results:
    data.append({'id':result.id, 'name':result.name})

  response={
    "count": count,
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@artists_blueprint.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # Done: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.get(artist_id)
  artist_shows = {}
  
  artist_shows['past_shows_count'] = 0
  artist_shows['upcoming_shows_count'] = 0
  artist_shows['upcoming_shows'] = []
  artist_shows['past_shows'] = []
  for show in artist.shows_artist:
    if show.start_time > datetime.now():
      artist_shows['upcoming_shows_count'] += 1
      artist_shows['upcoming_shows'].append({'venue_name': show.venue.name,
                                             'start_time':show.start_time,
                                              'venue_image_link':  show.venue.image_link,
                                              'venue_id' : show.venue.id})
    else:
      artist_shows['past_shows_count'] += 1
      artist_shows['past_shows'].append({'venue_name': show.venue.name,
                                             'start_time':show.start_time,
                                              'venue_image_link':  show.venue.image_link,
                                              'venue_id' : show.venue.id})
  return render_template('pages/show_artist.html', artist=artist, artist_shows = artist_shows)

#  Update
#  ----------------------------------------------------------------
@artists_blueprint.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  artist = Artist.query.get(artist_id)
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.facebook_link.data = artist.facebook_link
  form.image_link.data = artist.image_link
  form.website.data = artist.website
  
  # Done: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@artists_blueprint.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # Done: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  try:
    if form.validate_on_submit():
      artist.name = form.name.data
      artist.website  = form.website.data
      artist.city=form.city.data
      artist.state=form.state.data
      artist.image_link = form.image_link.data
      artist.phone = form.phone.data
      artist.image_link=form.image_link.data
      artist.genres=form.genres.data
      artist.facebook_link=form.facebook_link.data
      db.session.commit()
      flash('Artist ' + artist.name + ' was successfully edited!', 'success')
  except:
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('artists.show_artist', artist_id=artist_id))
#  Create Artist
#  ----------------------------------------------------------------

@artists_blueprint.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@artists_blueprint.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # Done: insert form data as a new Venue record in the db, instead
  # Done: modify data to be the data object returned from db insertion
  form = ArtistForm()
  try:
    # validate form 
    if form.validate_on_submit():
      # check if venue name existed 
      artist = Artist.query.filter_by(name = form.name.data).first()
      if artist:
        print('existed')
        flash(artist.name + ' Alread exists!', 'warning')
        return redirect(url_for('artists.create_artist_form'))
      new_artist = Artist(name=form.name.data,
                      city=form.city.data,
                      state=form.state.data,
                      # address=form.address.data,
                      phone=form.phone.data,
                      image_link=form.image_link.data,
                      genres=form.genres.data,
                      facebook_link=form.facebook_link.data,
                      website = form.website.data
                      )
  
      db.session.add(new_artist)
      db.session.commit()
      flash('Artist ' + new_artist.name + ' was successfully listed!', 'success')
      return redirect(url_for('artists.show_artist', artist_id = new_artist.id))
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
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # Done: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')