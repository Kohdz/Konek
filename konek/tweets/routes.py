from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_user, login_required, current_user
from konek.tweets.forms import TweetForm, ReplyForm
from konek.models import Tweet, Reply
from konek import db
from datetime import datetime


tweets = Blueprint('tweets', __name__)


@tweets.route('/post_tweet', methods=['POST'])
@login_required
def post_tweet():
    form = TweetForm()
    if form.validate():
        tweet = Tweet(user_id=current_user.id,
                      text=form.text.data,
                      date_created=datetime.now())
        db.session.add(tweet)
        db.session.commit()
        return redirect(url_for('users.timeline'))
    flash('Something Went Wrong/Form Not Valid', 'danger')


@tweets.route('/tweet/<int:tweet_id>')
def view_tweet(tweet_id):
    form = ReplyForm()
    tweet = Tweet.query.get_or_404(tweet_id)
    replies = Reply.query.filter_by(tweet_id=tweet_id).order_by(
        Reply.date_created.desc()).all()
    image_file = url_for('static', filename='imgs/' + tweet.user.image)
    current_time = datetime.now()
    return render_template('view_tweet.html',
                           tweet=tweet,
                           current_time=current_time,
                           form=form,
                           replies=replies,
                           image_file=image_file)


@tweets.route('/tweet/<int:tweet_id>/delete', methods=['POST'])
@login_required
def delete_tweet(tweet_id):
    tweet = Tweet.query.get_or_404(tweet_id)
    if tweet.user_id != current_user.id:
        abort(403)
    tweet.text = 'This tweet has been deleted'
    db.session.commit()
    flash('Your tweet has been deleted!', 'success')
    return redirect(url_for('tweets.view_tweet', tweet_id=tweet.id))


@tweets.route('/tweet/<int:tweet_id>/reply', methods=['POST'])
@login_required
def replies(tweet_id):
    form = ReplyForm()
    tweet = Tweet.query.get_or_404(tweet_id)
    reply_user_image = url_for('static', filename='imgs/' + current_user.image)
    if form.validate():
        reply = Reply(text=form.reply.data,
                      name=current_user.name,
                      username=current_user.username,
                      image=reply_user_image,
                      tweet_id=tweet.id,
                      date_created=datetime.now())
        db.session.add(reply)
        db.session.commit()
        flash('reply posted!', 'success')
        return redirect(url_for('tweets.view_tweet', tweet_id=tweet_id))
    flash('Something Went Wrong/Form Not Valid', 'danger')


# write a new route that quries tweets that are not the last
# 
# 