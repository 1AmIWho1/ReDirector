from flask import render_template, redirect, send_from_directory, flash, request
from flask import current_app as app
from hashids import Hashids
import datetime as dt
import os

from .forms import AddForm, DeleteForm, RefreshForm
from .models import db, Alias


path = {
    'favicon': 'favicon.ico',
    'index': '',
    'add': 'add',
    'delete': 'delete',
    'refresh': 'refresh'
}


@app.context_processor
def base_context():
    context = dict()
    context['menu'] = [
        {'link': '/' + path['add'], 'text': 'Создание'},
        {'link': '/' + path['delete'], 'text': 'Удаление'},
        {'link': '/' + path['refresh'], 'text': 'Обновление'},
    ]
    context['title'] = 'ReDirector'
    context['footer_text'] = '© Petr Kladov, 2021'
    return context


@app.errorhandler(404)
def page_not_found():
    context = dict()
    context['pagename'] = 'Ошибка 404'
    return render_template('404.html', context=context), 404


@app.route('/<alias>')
def direct(alias):
    a = Alias.query.filter(Alias.alias == alias).first()
    if a:
        return redirect(str(a))
    return page_not_found()


def check_alias_sym(alias):
    perm = '-._~:?#[]@!$&\'()*+,;='
    for sym in alias:
        if not sym.isalnum():
            if sym not in perm:
                return True
    return False


@app.route('/' + path['index'], methods=['GET', 'POST'])
@app.route('/' + path['add'], methods=['GET', 'POST'])
def add():
    form = AddForm(exp_time=24)
    context = dict()
    context['pagename'] = 'Создание новой ссылки'
    context['form'] = form
    if form.validate_on_submit():
        alias = form.alias.data.strip()
        if alias == '':
            i = 0
            hashid = Hashids(form.full.data)
            alias = hashid.encode(i)
            existing_alias = Alias.query.filter(Alias.alias == alias).first()
            while existing_alias:
                i += 1
                hashid = Hashids(form.full.data)
                alias = hashid.encode(i)
                existing_alias = Alias.query.filter(Alias.alias == alias).first()
        else:
            if len(alias) > 64:
                flash('Использовано слишком много символов, введите другой псевдоним', 'warning')
                return render_template('add.html', context=context)
            if check_alias_sym(alias):
                flash('Использованны запрещенные символы, введите другой псевдоним', 'warning')
                return render_template('add.html', context=context)
            existing_alias = Alias.query.filter(Alias.alias == alias).first()
            if existing_alias:
                flash('Такой псевдоним уже существует, срок действия закончится {}, '
                      'введите другой'.format(existing_alias.expiration), 'warning')
                return render_template('add.html', context=context)
        if form.exp_time.data > 24 * 7:
            flash('Нельзя создать псевдоним со сроком действия больше чем 7 дней', 'warning')
            return render_template('add.html', context=context)
        new_alias = Alias(full=form.full.data, alias=alias, password=form.password.data,
                          expiration=dt.datetime.now() + dt.timedelta(hours=form.exp_time.data))
        db.session.add(new_alias)
        db.session.commit()
        flash('Успешно создано, короткая ссылка - {}{}, '
              'истекает через {}ч.'.format(request.host_url, alias, form.exp_time.data), 'success')
    return render_template('add.html', context=context)


@app.route('/' + path['delete'], methods=['GET', 'POST'])
def delete():
    form = DeleteForm()
    context = dict()
    context['pagename'] = 'Удаление ссылки'
    context['form'] = form
    if form.validate_on_submit():
        if form.alias.data in path.values():
            flash('Нельзя удалить ссылку, необходимую для работы сайта', 'danger')
            return render_template('delete.html', context=context)
        res = db.session.query(Alias).filter(Alias.alias == form.alias.data)
        if res.first():
            a = res[0]
            password = a.password
            if password == form.password.data:
                db.session.delete(a)
                db.session.commit()
                flash('Успешное удаление', 'success')
                return render_template('delete.html', context=context)
            else:
                flash('Неверный пароль', 'danger')
                return render_template('delete.html', context=context)
        else:
            flash('Несуществующая ссылка', 'danger')
            return render_template('delete.html', context=context)
    return render_template('delete.html', context=context)


@app.route('/' + path['refresh'], methods=['GET', 'POST'])
def refresh():
    form = RefreshForm(exp_time=24)
    context = dict()
    context['pagename'] = 'Обновление времени действия ссылки'
    context['form'] = form
    if form.validate_on_submit():
        if form.alias.data in path.values():
            flash('Нельзя обновить ссылку, необходимую для работы сайта', 'danger')
            return render_template('refresh.html', context=context)
        if form.exp_time.data > 24 * 7:
            flash('Нельзя продлять ссылки больше чем на 7 дней', 'warning')
            return render_template('refresh.html', context=context)
        res = db.session.query(Alias).filter(Alias.alias == form.alias.data)
        if res.first():
            a = res[0]
            if a.password == form.password.data:
                tmp = dt.timedelta(hours=form.exp_time.data)
                if form.exp_time.data > 24 * 7 or (a.expiration + tmp - dt.datetime.now()).days > 7:
                    flash('Нельзя продлять ссылки больше чем на 7 дней', 'warning')
                    return render_template('refresh.html', context=context)
                a.expiration += tmp
                db.session.commit()
                flash('Успешное обновлено, срок действия закончится {}'.format(a.expiration), 'success')
                return render_template('refresh.html', context=context)
            else:
                flash('Неверный пароль', 'danger')
                return render_template('refresh.html', context=context)
        else:
            flash('Несуществующая ссылка', 'danger')
            return render_template('refresh.html', context=context)
    return render_template('refresh.html', context=context)


@app.route('/' + path['favicon'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')
