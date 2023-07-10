from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class RegistrationForm(FlaskForm):
    username = StringField('Nome',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                           validators=[DataRequired(), Email()])
    #password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Registre-se')