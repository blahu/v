from flask import render_template, url_for, flash, g
from flask.ext.sqlalchemy import get_debug_queries
from flask.ext.login import current_user, login_required
from app import app, db, login_manager
from .models import Animals, Visits, Vets
from .models import (
     get_all_animals,
     get_all_species,
     get_all_breeds,
     get_all_owners,
     get_all_vets,
     get_all_users,
)


from config import ITEMS_PER_PAGE

@login_manager.user_loader
def load_user(id):
    return Vets.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
@login_required
def index():
    return "Hello, World to {} {}!".format(g.user.first_name, g.user.last_name)

@app.route('/animals')
@app.route('/animals/')
@app.route('/animals/<int:page>')
@login_required
def animals(page=1):
    animals = get_all_animals().paginate(page, ITEMS_PER_PAGE, False)
    for q in get_debug_queries():
	flash(q)
    return render_template("animals.html",
                           title='Animals',
                           animals=animals)

@app.route('/species/')
@app.route('/species/<int:page>')
@login_required
def species(page=1):
    species = get_all_species().paginate(page, ITEMS_PER_PAGE, False)
    for q in get_debug_queries():
	flash(q)
    return render_template("species.html",
                           title='Species',
                           species=species)

@app.route('/breeds/')
@app.route('/breeds/<int:page>')
@login_required
def breeds(page=1):
    breeds = get_all_breeds().paginate(page, ITEMS_PER_PAGE, False)
    for q in get_debug_queries():
	flash(q)
    return render_template("breeds.html",
                           title='Breeds',
                           breeds=breeds)

@app.route('/owners/')
@app.route('/owners/<int:page>')
@login_required
def owners(page=1):
    owners = get_all_owners().paginate(page, ITEMS_PER_PAGE, False)
    for q in get_debug_queries():
	flash(q)
    return render_template("owners.html",
                           title='Owners',
                           owners=owners)

@app.route('/visits/<int:animal>')
@login_required
def visits(animal=1):
    animal_data = Animals.get_animal_by_id(animal)
    visits = Visits.get_visits_by_animal(animal)
    for q in get_debug_queries():
	flash(q)
    flash(animal_data[0].name)
    return render_template("visits.html",
                           title='Visits by {}'.format((animal_data[0].name).encode('utf-8')),
                           visits=visits,
                           animal_data=animal_data,
    )


@app.route('/users/')
@app.route('/users/<int:page>')
@login_required
def users(page=1):
    users = get_all_users().paginate(page, ITEMS_PER_PAGE, False)
    for q in get_debug_queries():
	flash(q)
    return render_template("users.html",
                           title='Users',
                           users=users)

@app.route('/vets/')
@app.route('/vets/<int:page>')
@login_required
def vets(page=1):
    vets = get_all_vets().paginate(page, ITEMS_PER_PAGE, False)
    for q in get_debug_queries():
	flash(q)
    return render_template("vets.html",
                           title='Vets',
                           vets=vets)

## ===================================
## SNIPETS
## http://flask.pocoo.org/snippets/28/
## ===================================
import re
from jinja2 import evalcontextfilter, Markup, escape

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', Markup('<br>\n'))
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


@app.template_filter()
def decode_utf8(string):
    return string.decode('utf8')
