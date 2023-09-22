from flask import Blueprint, render_template, request, redirect, url_for, session
import games.game_info.services as services
import games.adapters.repository as repo

from games.authentication.authentication_bp import login_required

from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

game_info_bp = Blueprint('game_info_bp', __name__)


@game_info_bp.route('/game_info')
def game_info():

    game_id = int(request.args.get('game_id'))
    game = services.get_game_by_id(game_id, repo.repo_instance)

    average_rating = 'N/A'
    if len(game.reviews) > 0:
        all_ratings = [review.rating for review in game.reviews]
        average_rating = str(round(sum(all_ratings) / len(all_ratings), 3))

    return render_template('game_view/game_info.html', game=game, average_rating=average_rating)


@game_info_bp.route('/game_info/review_game', methods=['GET', 'POST'])
@login_required
def review_game():
    # Obtain the username of the currently logged-in user.
    username = session['user_name']

    game_id = int(request.args.get('game_id'))
    game = services.get_game_by_id(game_id, repo.repo_instance)

    average_rating = 'N/A'
    if len(game.reviews) > 0:
        all_ratings = [review.rating for review in game.reviews]
        average_rating = str(round(sum(all_ratings) / len(all_ratings), 3))

    # Implementation below of user can only review once

    # user = services.get_user(username, repo.repo_instance)
    # for review in game.reviews:
    #     if review.user == user:
    #         return redirect(url_for('game_info_bp.game_info', game_id=game_id))

    # Create form
    form = ReviewForm()

    if form.validate_on_submit():

        form.rating.data = int(form.rating.data)
        services.add_review(game_id, form.rating.data, form.comment.data, username, repo.repo_instance)

        return redirect(url_for('game_info_bp.game_info', game_id=game_id))

    return render_template('game_view/review.html', game=game, average_rating=average_rating, form=form)


class ReviewForm(FlaskForm):
    comment = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short')])
    rating = SelectField('Rating', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    submit = SubmitField('Submit')
