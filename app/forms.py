from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class AddForm(FlaskForm):
    full = StringField('full', validators=[DataRequired()],
                       description=['Введите ссылку, которую необходимо сократить', 'Полная ссылка'])
    alias = StringField('alias', description=['Введите псевдоним сокращенной ссылки (при желании)', 'Псевдоним'])
    password = StringField('password',
                           description=['Введите пароль (при желании), необходимый для удаления ссылки', 'Пароль'])
    button_text = 'Создать'


class DeleteForm(FlaskForm):
    alias = StringField('alias', validators=[DataRequired()], description=['Введите сокращенную ссылку', 'Ссылка'])
    password = StringField('password', description=['Введите пароль (при наличии)', 'Пароль'])
    button_text = 'Удалить'


class RefreshForm(FlaskForm):
    alias = StringField('alias', validators=[DataRequired()], description=['Введите сокращенную ссылку', 'Ссылка'])
    password = StringField('password', description=['Введите пароль (при наличии)', 'Пароль'])
    button_text = 'Обновить'
