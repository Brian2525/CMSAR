import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_bootstrap import Bootstrap4
from forms import LoginForm, RegisterForm, Models
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import MetaData, Table, Column, Integer,String, Boolean, DateTime, Select, insert, BLOB, VARBINARY
from sqlalchemy.orm import Session, sessionmaker
from werkzeug.utils import secure_filename
from flask_uploads import configure_uploads, UploadSet, IMAGES
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, DateTimeField, FileField,SelectField
from wtforms.validators import InputRequired, Email, Length


app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = "thisisasecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///AR.db'
app.config['UPLOADED_IMAGES_DEST'] = 'static/gallery/poster'
app.config['UPLOADED_GLBS_DEST'] = 'static/gallery/glb'
app.config['UPLOADED_GLB_ALLOW']= '.glb'
app.config['UPLOADED_USDZ_DEST'] = 'static/gallery/usdz'
app.config['UPLOADED_USDZ_ALLOW']= '.usdz'

db = SQLAlchemy(app)
bootstrap = Bootstrap4(app)


img = UploadSet('images', IMAGES)
configure_uploads(app,img)


format_glb = UploadSet("glbs", extensions='.glb')
configure_uploads(app, format_glb)

format_usdz = UploadSet("usdz", extensions='.usdz')
configure_uploads(app, format_usdz)


#creación de base de datos del usuario, contenido (assets 3D), contenido (RAs creadas)
# La base de datos se compone de una tabla que tiene, para cada usuario; id (primary key), name, email y password
#Creación de base de datos del contenido


class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(30))
    company=db.Column(db.String(30))
    position=db.Column(db.String(30))
    email=db.Column(db.String(30))
    password=db.Column(db.String(30))
    spaces_for_ar=db.Column(db.Integer)
    date_account_created=db.Column(db.DateTime)

class ArExperiences(db.Model):
    __tablename__= "arexperiences"
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30))
    model=db.Column(db.String(30))
    description=db.Column(db.String(30))
    qr_code=db.Column(db.String(30))
    category=db.Column(db.String(30))
    ar_status=db.Column(db.Boolean)
    expiration_date=db.Column(db.String(30))
    views=db.Column(db.Integer)


class Content(db.Model):
    __tablename = "content"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    image = db.Column(db.String(30))
    version = db.Column(db.String(30))
    category = db.Column(db.String(30))
    user_asociated = db.Column(db.Integer)
    glb = db.Column(db.String(30))
    usdz = db.Column(db.String(30))






'''

meta=MetaData()
User=Table("users", meta,
        Column("id", Integer, primary_key=True),
        Column("username", String(30)),
        Column("company", String(30)),
        Column("position", String(30)),
        Column("email", String(30)),
        Column("password", String(30)),
        Column("spaces_for_ar", Integer),
        Column("date_account_created", DateTime)

           )

ArExperiences = Table(
    "arexperiences", meta,
    Column("id", Integer, primary_key=True),
    Column("url_experience", String(30)),
    Column("Embedded", String(30)),
    Column("ar_status", Boolean),
    Column ("expiration_date", DateTime),
    Column("views", Integer)

)

Content = Table(
    "content", meta, 
    Column("id", Integer, primary_key=True), 
    Column("name", String(30), unique=True),
    Column("image", String(30)),
    Column("description", String(30)),
    Column("version", Integer),
    Column("category", String(30)),
    Column("user_asociated", Integer),
    Column("glb", String(20)),
    Column("usdz", String(20))
    
)

'''


#db.create_all()
engine = sa.engine.create_engine('sqlite:///AR.db', echo=True)

#meta.create_all(engine)

engine = sa.engine.create_engine('sqlite:///AR.db')
Session=sessionmaker(engine)
session=Session()



#if not database_exists(engine.url):
#    create_database(engine.url)
#print(database_exists(engine.url))


'''   
class Content(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(5))
    name=db.Column(db.String(5))


  
class Content
    id 
    name 
    image
    description
    User_asociated (public or private)
    category
    version 
    glb 
    usdz
    obj
    fbx 
    .unity
        
class CreatorContent
    id 
    num_items- total of content created
    
    
    
    
'''



#La base de datos se del contenido se compone de una tabla que tiene id (primary key), nombre, contenido (),
#Creación de base de datos de los assets
#La creación de la base de datos del contenido; este contenido tendrá un nombre y dos tipos diferentes de archivos (.usdz y .glb), una versión (que se irá subiendo cada que se realice una nueva actualización), una imagen que será la descriptiva, un autor, y una fecha de subida.

all_categories=session.query(Content).all()



@app.route("/")
def index():
    return render_template("index.html")


#Dashboard for view AR Experiences
@app.route("/dashboard")
def dashboard():
    all_assets=session.query(ArExperiences).all()
    #en el dashboard estarán todas las experiencias que cada uno de los usuarios generó
    #Quiero saber la fecha en que se publicó el contenido
    return render_template("dashboard.html", ar_all=all_assets)


#Dashboard for view Uploaded Content(3D models for augmented reality)
@app.route("/dashboard_models")
def dashboard_models():
    all_assets=session.query(Content).all()
    #en el dashboard estarán todas las experiencias que cada uno de los usuarios generó
    #Quiero saber la fecha en que se publicó el contenido
    return render_template("dashboard_models.html", all_models=all_assets)






class CreateAr(FlaskForm):
    all_models = session.query(Content).all()
    list_of_models = []
    for model in all_models:
        list_of_models.append(model.name)
    name = StringField("name", validators=[InputRequired()])
    description = StringField("Descripción", validators=[InputRequired()])
    ar = SelectMultipleField("Choose your 3D object for AR", choices=list_of_models)

    submit = SubmitField()



#Create content in AR - Create experiences
@app.route("/create", methods=["GET", "POST"])
def create():
    all_models = session.query(Content).all()
    list_of_models = []
    for model in all_models:
        list_of_models.append(model.name)
    form = CreateAr()
    if form.validate_on_submit():
        name = request.form['name']
        ar=request.form['ar']
        description = request.form['description']
        version=1
        ar_status = True
        expiration_date = "Hello"
        views = 2
        print(name, description, ar)
#        new_experience = ArExperiences(name=name, model=ar, description=description,category=category, ar_status=ar_status, expiration_date=expiration_date, views=views)
#        session.add(new_experience)
#        session.commit()

        return redirect(url_for('dashboard'))
    #redirigirá hacia el dashboard para poder visualizar el contenido
    return render_template("create.html", form=form)



#Delete AR Experiences from DB
@app.route("/delete")
def delete():
    ar_id= request.args.get("ar_id")
    element_to_delete=session.query(ArExperiences).filter_by(id=ar_id).first()
    session.delete(element_to_delete)
    session.commit()
    return redirect('dashboard')


#Link for view in augmented reality

@app.route("/viewar")
def viewar():
    id_ar = request.args.get("ar_id")
    chosen_ar = session.query(ArExperiences).filter_by(id=id_ar).first()
    return render_template("viewAR.html", ar=chosen_ar)


#login
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)
        return "Hello"

    return render_template("login.html", form=form)

#Register
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.name.data
        email = form.email.data
        password = form.password.data
        company = form.company.data
        position = form.position.data
        # CREATE NEW USER
        new_user = User(username=username, email=email, password=password, position=position, company=company, spaces_for_ar=1)
        # ADD USER TO DATA BASE
        session.add(new_user)
        session.commit()


    return render_template("register.html", form=form)


#Form to uploard 3D Content in DB
@app.route("/creators", methods=["GET", "POST"])
def creators():
    form = Models()
    if form.validate_on_submit():
        name = form.name.data
        images = img.save(form.imagen.data)
        version = 1
        glb = format_glb.save(form.archivo_glb.data)
        usdz = format_usdz.save(form.archivo_usdz.data)
        category = form.category.data[0]
        new_asset = Content(name=name,
                          image=f"/static/gallery/poster/{images}",
                          version=version,
                          category=category,
                          glb=f"/static/gallery/glb/{glb}",
                          usdz=f"/static/gallery/glb/{usdz}")
        session.add(new_asset)
        session.commit()
        return redirect(url_for('dashboard_models'))

    return render_template("creators_studio.html", form=form)


@app.route("/delete_3d")
def delete_3d():
    id= request.args.get("model_id")
    element_to_delete=session.query(Content).filter_by(id=id).first()
    session.delete(element_to_delete)
    session.commit()
    return redirect('dashboard_models')



if __name__=='__main__':
    app.run(debug=True)