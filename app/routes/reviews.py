from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from flask_login import login_required, current_user
import uuid

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

# In-memory pending reviews store
pending_reviews = []

@reviews_bp.route('/<app_name>')
@login_required
def app_reviews(app_name):
    df = current_app.apps_df
    app_info = df[df['App'] == app_name].iloc[0].to_dict()
    reviews_df = current_app.reviews_df
    reviews = reviews_df[(reviews_df['App'] == app_name)]['Translated_Review'].dropna().to_list()
    #approved = [r for r in pending_reviews if r['App'] == app_name and r['approved']]
    return render_template('app_reviews.html', app=app_info, reviews=reviews)

@reviews_bp.route('/submit/<app_name>', methods=['POST'])
@login_required
def submit_review(app_name):
    content = request.form['content']
    review = {
        "id": str(uuid.uuid4()),
        "App": app_name,
        "Review": content,
        "User": current_user.id,
        "approved": False
    }
    pending_reviews.append(review)
    flash("Review submitted for approval.")
    return redirect(url_for('reviews.app_reviews', app_name=app_name))