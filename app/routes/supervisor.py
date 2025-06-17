from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.routes.reviews import pending_reviews

supervisor_bp = Blueprint('supervisor', __name__, url_prefix='/supervisor')

@supervisor_bp.route('/pending')
@login_required
def pending():
    if current_user.role != "supervisor":
        flash("You are not authorized to view this page.")
        return redirect(url_for('search.home'))
    unapproved = [r for r in pending_reviews if not r["approved"]]
    return render_template('pending_reviews.html', reviews=unapproved)

@supervisor_bp.route('/approve/<review_id>', methods=['POST'])
@login_required
def approve(review_id):
    if current_user.role != "supervisor":
        flash("You are not authorized to perform this action.")
        return redirect(url_for('search.home'))
    for r in pending_reviews:
        if r["id"] == review_id:
            r["approved"] = True
            flash("Review approved!")
            break
    return redirect(url_for('supervisor.pending'))