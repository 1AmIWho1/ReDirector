from flask import render_template, redirect, send_from_directory, flash, g
from flask import current_app as app
from hashids import Hashids
from datetime import datetime as dt
from time import time
import os

from .forms import AddForm, DeleteForm, RefreshForm
from .models import db, Alias


domen = 'http://localhost/'


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
    print(a)
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
                flash('Такой псевдоним уже существует, срок действия закончится через n ч., '
                      'введите другой', 'warning')
                return render_template('add.html', context=context)
        exp_time = form.exp_time.data
        if exp_time > 24 * 7:
            flash('Нельзя создать псевдоним со сроком действия больше чем 7 дней', 'warning')
            return render_template('add.html', context=context)
        new_alias = Alias(full=form.full.data, alias=alias, password=form.password.data, created=dt.now())
        db.session.add(new_alias)
        db.session.commit()
        flash('Успешно создано, короткая ссылка - {}{}, истекает через {}ч.'.format(domen, alias, exp_time), 'success')
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
        cur = g.db.execute('select password from entries where alias = (?)', (form.alias.data,))
        try:
            password = str(cur.fetchall()[0][0])
            if password == form.password.data:
                g.db.execute('delete from entries where alias = (?)', (form.alias.data,))
                cur_seq = g.db.execute('select seq from sqlite_sequence')
                ids = int(cur_seq.fetchall()[0][0]) - 1
                g.db.execute('update sqlite_sequence set seq = (?)', (ids,))
                g.db.commit()
                flash('Успешное удаление', 'success')
                return render_template('delete.html', context=context)
            else:
                flash('Неверный пароль', 'danger')
                return render_template('delete.html', context=context)
        except IndexError:
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
        cur = g.db.execute('select password from entries where alias = (?)', (form.alias.data,))
        try:
            password = str(cur.fetchall()[0][0])
            if password == form.password.data:
                cur = g.db.execute('select expiration from entries where alias = (?)', (form.alias.data,))
                exp = cur.fetchone()[0]
                if (exp - int(time()))//3600 > 24 * 7:
                    flash('Нельзя продлять ссылки больше чем на 7 дней', 'warning')
                    return render_template('refresh.html', context=context)
                exp += form.exp_time.data * 3600
                g.db.execute('update entries set expiration = (?) where alias = (?)', (exp, form.alias.data))
                g.db.commit()
                cur = g.db.execute('select expiration from entries where alias = (?)', (form.alias.data,))
                flash('Успешное обновлено, срок действия закончится через {}ч.'
                      .format((cur.fetchone()[0] - int(time()))//3600), 'success')
                return render_template('refresh.html', context=context)
            else:
                flash('Неверный пароль', 'danger')
                return render_template('refresh.html', context=context)
        except IndexError:
            flash('Несуществующая ссылка', 'danger')
            return render_template('refresh.html', context=context)
    return render_template('refresh.html', context=context)


@app.route('/' + path['favicon'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')
