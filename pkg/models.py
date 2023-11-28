import datetime
from pkg import db
 
class Students(db.Model): 
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    email= db.Column(db.String(100), nullable=True)
    pwd = db.Column(db.String(100), nullable=True)
    fname = db.Column(db.String(100), nullable=True)
    lname = db.Column(db.String(100), nullable=True)
    midname = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.String(100), nullable=True)
    marital = db.Column(db.String(100), nullable=True)
    program = db.Column(db.String(100), nullable= True)
    manualpro = db.Column(db.String(100), nullable=True)
    studymode = db.Column(db.String(100), nullable=True)
    stateofres = db.Column(db.String(100), nullable=True)
    lgaofres = db.Column(db.String(100), nullable=True)
    cityofres = db.Column(db.String(100), nullable=True)
    resaddress = db.Column(db.String(255), nullable=True)
    pic = db.Column(db.String(100), nullable=True)
    dob = db.Column(db.String(100), nullable=True)
    nationality = db.Column(db.String(100), nullable=True)
    stateoforigin = db.Column(db.String(100), nullable=True)
    originlga = db.Column(db.String(100), nullable=True)
    hometown = db.Column(db.String(100), nullable=True)
    nxtofkin = db.Column(db.String(100), nullable=True)
    relwithkin = db.Column(db.String(100), nullable=True)
    placeofbirth = db.Column(db.String(100), nullable=True)
    nxtofkinphone = db.Column(db.String(100), nullable=True)
    scardexamtype = db.Column(db.String(10), nullable=True)
    cardyear = db.Column(db.String(10), nullable=True)
    cadserialnumber = db.Column(db.String(100), nullable=True)
    cardpin = db.Column(db.String(100), nullable=True)
    resultcombo = db.Column(db.String(5), nullable=True)
    status = db.Column(db.String(100), nullable=True)
    regdate = db.Column(db.DateTime(), default=datetime.datetime.utcnow())




class Olevel(db.Model): 
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    subject = db.Column(db.String(100), nullable=True)
    score = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100),nullable=True)




class Jamb(db.Model):
    id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    subject = db.Column(db.String(100), nullable=True)
    score = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), primary_key=True)




class Admin(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    email = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(50), nullable=True)
    regdate = db.Column(db.DateTime(), default=datetime.datetime.utcnow())


class Contactus(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    message = db.Column(db.String(50), nullable=True)
    regdate = db.Column(db.DateTime(), default=datetime.datetime.utcnow())





class States(db.Model): 
    state_id = db.Column(db.Integer(), primary_key=True)
    state_name = db.Column(db.String(20), nullable=False)




class Courses(db.Model): 
    course_id = db.Column(db.Integer(), primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)

