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
    operation_status_list = Operation_Status.query.order_by(Operation_Status.id.desc())
    return render_template('operation_statuses/index.html', operation_statuses=operation_status_list)

@operation_statuses.route('/<int:id>')
@login_required
def operation_status(id):
    operation_status = Operation_Status.query.filter_by(id=id).first_or_404()
    return render_template('operation_statuses/operation_status.html', operation_status=operation_status)


@operation_statuses.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if not current_user.is_admin:
        abort(403)
    _last_operation_status_id = Operation_Status.query.first()
    id = 1
    if _last_operation_status_id is not None:
        id = _last_operation_status_id.id + 1

    form = Operation_StatusForm()
    if form.validate_on_submit():
        operation_status = Operation_Status(id)
        form.to_model(operation_status) # update operation_status object with form data
        db.session.add(operation_status)
        db.session.commit()
        flash(gettext(u'New operation_status: {operation_status} was added successfully.'.format(operation_status=operation_status.name)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % ( getattr(form, field).label.text, error))
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
        flash(gettext(u'operation_status with id: {operation_status} has been updated.'.format(operation_status=operation_status.id)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % ( getattr(form, field).label.text, error))
    form.from_model(operation_status)
    return render_template('operation_statuses/edit.html', operation_status=operation_status, form=form)


@operation_statuses.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    operation_status = Operation_Status.query.get_or_404(id)
    if current_user.is_admin:
        db.session.delete(operation_status)
        db.session.commit()
        flash(gettext(u'Operation_Status with id: {operation_status} has been deleted.'.format(operation_status=operation_status.id)))
        return redirect(url_for('.index'))
    else:
        flash(gettext(u'You have to be administrator to remove operation_statuses.'))
        return redirect(url_for('.index'))

    # should never get here
    return render_template('operation_statuses/index.html')
