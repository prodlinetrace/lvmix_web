from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext
from .. import db
from ..models import Status
from . import statuses

@statuses.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Status.query.paginate(
        page, per_page=current_app.config['STATUSES_PAGE'],
        error_out=False)
    status_list = pagination.items
    return render_template('statuses/index.html', statuses=status_list, pagination=pagination)


@statuses.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    status = Status.query.get_or_404(id)
    if current_user.is_admin:
        db.session.delete(status)
        db.session.commit()
        flash(gettext(u'status: {status} has been deleted.'.format(status=status.id)))
        return redirect(url_for('.index'))
    else:
        flash(gettext(u'You have to be administrator to remove statuses.'))
        return redirect(url_for('.index'))

    # should never get here
    return render_template('statuses/index.html')