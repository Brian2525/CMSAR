from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, DateTimeField, FileField,SelectField
from wtforms.validators import InputRequired, Email, Length
import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker




class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=15)])
    remember = BooleanField("Remember me")
    submit = SubmitField()


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    company = StringField("Company", validators=[InputRequired()])
    position = StringField("Position", validators=[InputRequired()])
    email = StringField("email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    #   confirm_password=PasswordField("Confirm Password", validators=[InputRequired()])
    submit = SubmitField()




class Models(FlaskForm):
    name = StringField("Name of 3D object", validators=[InputRequired()])
    imagen = FileField("Agrega la imagen principal tu archivo", validators=[InputRequired()])
    category = SelectMultipleField("A que categoría corresponde",
                                   choices=["Autos", "Edificios", "Eventos", "Muebles", "Artesanias", "Electronicos",
                                            "Personajes", "Otro"])
    archivo_glb = FileField("Agrega tu archivo glb")
    archivo_usdz = FileField("Agrega tu archivo usdz")
    submit = SubmitField()

