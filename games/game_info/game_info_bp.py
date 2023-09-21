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

    game_id = request.args.get('game_id')
    game = services.get_game_by_id(game_id, repo.repo_instance)

    return render_template('game_view/game_info.html', game=game)


@game_info_bp.route('/game_info/review_game', methods=['GET', 'POST'])
@login_required
def review_game():
    # Obtain the username of the currently logged in user.
    user_name = session['user_name']

    # Create form
    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the article id, representing the commented article, from the form.
        game_id = int(form.game_id.data)

        # Use the service layer to store the new comment.
        services.add_review(game_id, form.rating.data, form.review.data, user_name, repo.repo_instance)

        # Retrieve the article in dict form.
        article = services.get_game_by_id(game_id, repo.repo_instance)

        # Cause the web browser to display the page of all articles that have the same date as the commented article,
        # and display all comments, including the new comment.
        return redirect(url_for('news_bp.articles_by_date', date=article['date'], view_comments_for=game_id))

    game_id = request.args.get('game_id')
    game = services.get_game_by_id(game_id, repo.repo_instance)

    return render_template('game_view/review.html', game=game, form=form)


class ReviewForm(FlaskForm):
    review_game = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short')])
    rating = SelectField('Rating', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    game_id = HiddenField("Game id")
    submit = SubmitField('Submit')
