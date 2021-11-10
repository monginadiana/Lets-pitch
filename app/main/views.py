from flask import render_template, request, redirect, url_for, abort, flash
from . import main
from ..models import Comment, User, Pitch, Upvote, Downvote
from flask_login import login_required, current_user
from .. import db, photos
from .forms import UpdateProfile, pitchForm, CommentForm


@main.route('/')
def index():
    pitches = Pitch.query.all()
    twitter = Pitch.query.filter_by(category = 'Twitter').all()
    business = Pitch.query.filter_by(category = 'Business').all()
    competition = Pitch.query.filter_by(category = 'Competition').all()
    investor = Pitch.query.filter_by(category = 'Investor').all()
    
    return render_template('index.html', pitches = pitches, twitter = twitter, business = business, competition = competition, investor =investor)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)
    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)
    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile', uname=user.username))
    return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))


@main.route('/comment', methods=['GET', 'POST'])
@login_required
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(name=form.name.data)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully.')
        return redirect(url_for('.index'))
    return render_template('comments.html', form=form)


@main.route('/pitch', methods=['GET', 'POST'])
@login_required
def new_pitch():
    pitch_form = pitchForm()
    if pitch_form.validate_on_submit():
        
        title = pitch_form.title.data
        category = pitch_form.category.data
        description = pitch_form.description.data
        new_pitch = Pitch(title=title, description=description,
                        user=current_user, category=category)
        new_pitch.save_pitch()
        # db.session.add(new_pitch)
        # db.session.commit()
        return redirect(url_for('main.index'))

    # else:
    #     all_pitches = Pitch.query.order_by(Pitch.date_posted).all()

    return render_template('Pitch.html', pitch_form=pitch_form)


@main.route('/pitch/<id>', methods=['GET', 'POST'])
@login_required
def pitch_details(id):
    comments = Comment.query.filter_by(pitch_id=id).all()
    pitch = Pitch.query.get(id)
    if pitch is None:
        abort(404)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            comment=form.comment.data,
            pitch_id=id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        form.comment.data = ''
        flash('Your comment has been posted successfully!')
    return render_template('comments.html', pitch=pitch, comment=comments, comment_form=form)


@main.route('/like/<int:id>', methods=['GET', 'POST'])
@login_required
def like(id):
    pitch = Pitch.query.get(id)
    if pitch is None:
        abort(404)
    like = Upvote.query.filter_by(user_id=current_user.id, pitch_id=id).first()
    if like is not None:
        db.session.delete(like)
        db.session.commit()
        flash('You have successfully unupvoted the pitch!')
        return redirect(url_for('main.index'))
    new_like = Upvote(
        user_id=current_user.id,
        pitch_id=id
    )
    db.session.add(new_like)
    db.session.commit()
    flash('You have successfully upvoted the pitch!')
    return redirect(url_for('main.index'))


@main.route('/dislike/<int:id>', methods=['GET', 'POST'])
@login_required
def dislike(id):
    pitch = Pitch.query.get(id)
    if pitch is None:
        abort(404)
    
    dislike = Downvote.query.filter_by(
        user_id=current_user.id, pitch_id=id).first()
    if dislike is not None:
       
        db.session.delete(dislike)
        db.session.commit()
        flash('You have successfully undownvoted the pitch!')
        return redirect(url_for('.index'))

    new_dislike = Downvote(
        user_id=current_user.id,
        pitch_id=id
    )
    db.session.add(new_dislike)
    db.session.commit()
    flash('You have successfully downvoted the pitch!')
    return redirect(url_for('.index'))