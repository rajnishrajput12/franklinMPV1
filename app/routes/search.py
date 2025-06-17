from flask import Blueprint, render_template, current_app, request, jsonify
from flask_login import login_required

search_bp = Blueprint('search', __name__)

@search_bp.route('/')
@login_required
def home():
    return render_template('search.html')

@search_bp.route('/suggest', methods=['GET'])
@login_required
def suggest():
    query = request.args.get('q', '')
    suggestions = current_app.search_engine.suggest(query)
    return jsonify(suggestions)

@search_bp.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('q', '')
    results_df = current_app.search_engine.search(query)
    results = results_df.to_dict(orient='records')
    return render_template('results.html', results=results, query=query)