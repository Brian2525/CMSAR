'''
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
    description = db.Column(db.String(30))
    version = db.Column(db.String(30))
    category = db.Column(db.String(30))
    user_asociated = db.Column(db.Integer)
    glb = db.Column(db.String(30))
    usdz = db.Column(db.String(30))


#Tables


'''
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

