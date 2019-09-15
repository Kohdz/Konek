from flask import Blueprint, render_template
from konek.search.forms import SearchForm
from konek.search.utils import search_database
from konek import db

search = Blueprint('search', __name__)


@search.route('/search', methods=['POST'])
def search_bar():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.text.data
        search_database(db, query)
        return render_template('search_results.html',
                               form=form,
                               results=search_database(db, query),
                               query=query)
