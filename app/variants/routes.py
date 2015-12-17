from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext
from .. import db
from ..models import Variant
from . import variants
from .forms import VariantForm


@variants.route('/')
@login_required
def index():
    variant_list = Variant.query.order_by(Variant.id.desc())
    return render_template('variants/index.html', variants=variant_list)


@variants.route('/<int:id>')
@login_required
def variant(id):
    variant = Variant.query.filter_by(id=id).first_or_404()
    return render_template('variants/variant.html', variant=variant)


@variants.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if not current_user.is_admin:
        abort(403)
    _last_variant_id = Variant.query.first()
    id = 1
    if _last_variant_id is not None:
        id = _last_variant_id.id + 1
    form = VariantForm()
    if form.validate_on_submit():
        variant = Variant(id)
        form.to_model(variant)  # update variant object with form data
        db.session.add(variant)
        db.session.commit()
        flash(gettext(u'New variant: {variant} was added successfully.'.format(variant=variant.name)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (getattr(form, field).label.text, error))
    return render_template('variants/new.html', form=form)


@variants.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    variant = Variant.query.get_or_404(id)
    if not current_user.is_admin:
        abort(403)
    form = VariantForm()
    if form.validate_on_submit():
        form.to_model(variant)
        db.session.add(variant)
        db.session.commit()
        flash(gettext(u'Variant with id: {variant} has been updated.'.format(variant=variant.id)))
        return redirect(url_for('.index'))
    else:
        if form.errors:
            flash(gettext("Validation failed"))
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % ( getattr(form, field).label.text, error))
    form.from_model(variant)
    return render_template('variants/edit.html', variant=variant, form=form)


@variants.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    variant = Variant.query.get_or_404(id)
    if current_user.is_admin:
        db.session.delete(variant)
        db.session.commit()
        flash(gettext(u'Variant with id: {id} has been deleted.'.format(id=variant.id)))
        return redirect(url_for('.index'))
    else:
        flash(gettext(u'You have to be administrator to remove variants.'))
        return redirect(url_for('.index'))

    # should never get here
    return render_template('variants/index.html')
