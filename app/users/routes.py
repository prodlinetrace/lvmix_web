from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask.ext.login import login_required, current_user
from .. import db
from ..models import User, Comment
from . import users
from .forms import ProfileForm, UserForm, EditUserForm


@users.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.paginate(
        page, per_page=current_app.config['USERS_PER_PAGE'],
        error_out=False)
    user_list = pagination.items
    return render_template('users/index.html', users=user_list, pagination=pagination)


@users.route('/<username>')
@login_required
def user(username):
    user = User.query.filter_by(login=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.comments.paginate(
        page, per_page=current_app.config['USERS_PER_PAGE'],
        error_out=False)
    comment_list = pagination.items
    return render_template('users/user.html', user=user, comments=comment_list, pagination=pagination)


@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.bio = form.bio.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('{user}, you have updated your profile successfully.'.format(user=current_user.name))
        return redirect(url_for('users.user', username=current_user.login))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.bio.data = current_user.bio
    return render_template('users/profile.html', form=form)


@users.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if not current_user.is_admin:
        abort(403)
    form = UserForm()
    if form.validate_on_submit():
        user = User(login=form.login.data, name=form.name.data, password=form.password.data, is_admin=form.admin.data)
        db.session.add(user)
        db.session.commit()
        flash('New user: {user} was added successfully.'.format(user=user.name))
        return redirect(url_for('.index'))
    return render_template('users/new_user.html', form=form)


@users.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    user = User.query.get_or_404(id)
    if not current_user.is_admin and user.id != current_user.id:
        abort(403)
    form = EditUserForm()
    if not current_user.is_admin:
        del form.admin
    if form.validate_on_submit():
        form.to_model(user)
        db.session.add(user)
        db.session.commit()
        flash('User profile for: {user} has been updated.'.format(user=user.name))
        return redirect(url_for('.index'))
    form.from_model(user)
    return render_template('users/profile.html', form=form)


@users.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    user = User.query.get_or_404(id)
    if current_user.is_admin: 
        if user.id == current_user.id:
            flash('Unable to remove currently logged user: {user}.'.format(user=user.name))
            return redirect(url_for('.index'))

        db.session.delete(user)
        db.session.commit()
        flash('User profile for: {user} has been deleted.'.format(user=user.name))
        return redirect(url_for('.index'))
    else:
        flash('You have to be adminstrator to remove users.'.format(user=user.name))
        return redirect(url_for('.index'))

    # should never get here
    return render_template('users/index.html')
