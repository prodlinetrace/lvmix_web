from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext
from .. import db
from ..models import Operation_Status
from . import operation_statuses
from .forms import Operation_StatusForm


@operation_statuses.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Operation_Status.query.paginate(
        page, per_page=current_app.config['OPERATION_STATUSES_PER_PAGE'],
        error_out=False)
    operation_status_list = pagination.items
    return render_template('operation_statuses/index.html', operation_statuses=operation_status_list, pagination=pagination)


@operation_statuses.route('/<int:id>')
@login_required
def operation_status(id):
    operation_status = Operation_Status.query.filter_by(id=id).first_or_404()
    page = request.args.get('page', 1, type=int)
    return render_template('operation_statuses/operation_status.html', operation_status=operation_status)


@operation_statuses.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if not current_user.is_admin:
        abort(403)
    _last_operation_status_id = Operation_Status.query.first()
    if _last_operation_status_id is None:
        id = 0
    else:
        id = _last_operation_status_id.id
    id = id + 1
    form = Operation_StatusForm()
    if form.validate_on_submit():
        operation_status = Operation_Status(id)
        form.to_model(operation_status) # update operation_status object with form data
        db.session.add(operation_status)
        db.session.commit()
        flash(gettext('New operation_status: {operation_status} was added successfully.'.format(operation_status=operation_status.name)))
        return redirect(url_for('.index'))
    else:
        flash(gettext("Validation failed"))
    return render_template('operation_statuses/new.html', form=form)


@operation_statuses.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    operation_status = Operation_Status.query.get_or_404(id)
    if not current_user.is_admin:
        abort(403)
    form = Operation_StatusForm()
    if form.validate_on_submit():
        form.to_model(operation_status)
        db.session.add(operation_status)
        db.session.commit()
        flash(gettext('operation_status profile for: {operation_status} has been updated.'.format(operation_status=operation_status.name)))
        return redirect(url_for('.index'))
    else:
        flash(gettext("Validation failed"))
    form.from_model(operation_status)
    return render_template('operation_statuses/edit.html', operation_status=operation_status, form=form)


@operation_statuses.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    operation_status = Operation_Status.query.get_or_404(id)
    if current_user.is_admin:
        db.session.delete(operation_status)
        db.session.commit()
        flash(gettext('Operation_Status for: {operation_status} has been deleted.'.format(operation_status=operation_status.name)))
        return redirect(url_for('.index'))
    else:
        flash(gettext('You have to be administrator to remove operation_statuses.'.format(operation_status=operation_status.name)))
        return redirect(url_for('.index'))

    # should never get here
    return render_template('operation_statuses/index.html')
