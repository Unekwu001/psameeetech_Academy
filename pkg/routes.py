import json
import os,random,string
from flask import render_template, abort, flash, request,redirect, make_response, session,jsonify
from flask_mail import Message
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime,timedelta

from pkg import app
from pkg import db,mail
from pkg.models import States,Students,Courses,Olevel,Admin,Contactus,Jamb


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/',methods=['POST','GET'])
def messages():
    if request.method=='GET':
        return render_template('index.html')
    if request.method == 'POST':
        name=request.form.get('name')
        email=request.form.get('email')
        message=request.form.get('message')
        contactus=Contactus(name=name,email=email,message=message)
        db.session.add(contactus)
        db.session.commit()
        flash(f'Thank you for reaching out {name}. We will get in touch with you shortly.')
        return redirect('/')
        







@app.route('/psameeetech/user reg/',methods=['GET','POST'])
def user_reg():
    if request.method == "GET":
        return render_template("user-reg.html")
    if request.method == "POST":
        email=request.form.get("email")
        pwd=request.form.get('pwd')

        new_record = Students(email=email,pwd=pwd)
        record_exists = db.session.query(Students).filter(Students.email==email).all()
        if record_exists:
            flash('Email already in use. Try another.')
            return redirect('/psameeetech/user reg/')
        else:
            db.session.add(new_record)
            db.session.commit()
            message = Message('Welcome to Psameetech Academy', sender =  'unekwutheophilus@gmail.com', recipients = [email])
            message.html = f" Congratulations!.Your login details are as follows: email: {email}, password: {pwd}"
            mail.send(message)
            flash('Registration successful. Login here.')
            return redirect('/psameeetech/user login/')
         
            

@app.route('/psameeetech/user login/',methods=['GET','POST'])
def user_login():
    if request.method == 'GET':
        return render_template("user-login1.html")
    else:
        email= request.form.get('email')
        pwd = request.form.get('pwd')
        record_exists = db.session.query(Students).filter(Students.email==email,Students.pwd==pwd).first()
        if  record_exists:
            session['loggedin'] = email
            return redirect('/psameeetech/user dashboard/')
        else:
            flash('Invalid credentials')
            return redirect('/psameeetech/user login/')



@app.route('/psameeetech/user dashboard/')
def userdash():
    session_collected = session.get('loggedin')
    if session_collected:
        record = db.session.query(Students).filter(Students.email==session_collected).first()
        return render_template("user-dashboard.html",record=record)
    else:
        flash('Invalid credentials')
        return redirect('/psameeetech/user login/')







@app.route('/psameeetech/logout/')
def log_out():
        session_collected = session.get('loggedin')
        if session_collected:
            session.pop('loggedin')
            flash('You are logged out')
            return redirect("/psameeetech/user login/")
        else:
            return redirect("/psameeetech/user login/")
        




@app.route('/psameeetech/admin/logout/')
def admin_log_out():
        session_collected = session.get('loggedin')
        if session_collected:
            session.pop('loggedin')
            flash('You are logged out')
            return redirect("/psameeetech/admin login/")
        else:
            return redirect("/psameeetech/admin login/")




@app.route('/psameeetech/admin login/',methods=['GET','POST'])
def admin_login():
    if request.method == "GET":
        return render_template("admin-login.html")
    if request.method == "POST":
        email=request.form.get('email')
        pwd=request.form.get('pwd')
        record= db.session.query(Admin).filter(Admin.email==email,Admin.password==pwd).first()
        if record:
            session['loggedin']=email
            return redirect("/psameeetech/admin dashboard/")
        else:
            flash('Boss, Did you forget your credentials ?')
            return redirect("/psameeetech/admin login/")




@app.route('/psameeetech/user forgot password/',methods=['GET','POST'])
def forgotpwd():
    if request.method == 'GET':
        return render_template("forgot-password.html")
    else:
        email=request.form.get('email')
        valid_user = db.session.query(Students).filter(Students.email==email).first()
        if valid_user:
            email=valid_user.email
            message = Message('Psameetech Academy password reset', sender =  'unekwutheophilus@gmail.com', recipients = [email])
            message.html = f"Click  here to reset your password >> <a href='http://127.0.0.1:2020/psameetechacademy/newpwd/{email}'>Password reset Link</a>"
            mail.send(message)
            flash('Please kindly check your mail box')
            return redirect('/psameeetech/user forgot password/')
        else:
            flash('Oops. User does not exist')
            return redirect('/psameeetech/user forgot password/')




@app.route('/psameetechacademy/newpwd/<email>/',methods=['GET','POST'])
def reset_pwd(email):
    if request.method == 'GET':
        return render_template('resetpwd.html',email=email)
    else:
        pwd=request.form.get('pwd')
        db.session.execute(f"update students set pwd='{pwd}' where email='{email}'")
        db.session.commit()
        flash('Congratulations! Your password reset was successful.')
        message = Message('Psameetech Academy', sender =  'unekwutheophilus@gmail.com', recipients = [email])
        message.html = f"<h3 style='color:green'>Congratulations !.</h3> Your newly created password is {pwd}."
        mail.send(message)
        return redirect("/psameeetech/user login/")



@app.route('/sendmail/<email>/',methods=['GET','POST'])
def send_email(email):
    session_collected = session.get('loggedin')
    if session_collected:
        if request.method == "GET":
            student=db.session.query(Students).filter(Students.email==email).first()
            return render_template('admin-mail.html',student=student)
        else:
            msg= request.form.get('msg')
            message = Message('Psameetech Academy', sender =  'unekwutheophilus@gmail.com', recipients = [email])
            message.body = f"{msg}"
            mail.send(message)
            flash('Mail sent !')
            return redirect('/psameeetech/forms-received/')
    else:
        return redirect('/psameeetech/admin login/')









@app.get('/psameeetech/admin dashboard/')
def admindash():
    session_collected=session.get('loggedin')
    if session_collected:
        record=db.session.query(Admin).filter(Admin.email==session_collected).first()
        students=db.session.query(Students).all()
        submitted_forms=db.session.query(Students).filter(Students.fname!="").all()
        pending_forms=db.session.query(Students).filter(Students.fname!="",Students.status=="pending").all()
        processed_forms=db.session.query(Students).filter(Students.fname!="",Students.status=="processed").all()
        return render_template("admin-dashboard.html",record=record,students=students,pending_forms=pending_forms,processed_forms=processed_forms,submitted_forms=submitted_forms)
    else:
        flash('Your session has expired')
        return redirect('/psameeetech/admin login/')



@app.route('/admin/details/',methods=['GET','POST'])
def all():
    session_collected = session.get('loggedin')
    if session_collected:
        email = request.form.get('email')
        allstudents = db.session.query(Students).all()
        selectedstudent = db.session.query(Students).filter(Students.email==email).first()
        if  selectedstudent:
            date = selectedstudent.regdate.strftime('%a  %d  %b , %Y')
            oleveldetails = db.session.query(Olevel).filter(Olevel.email==email).limit(9).all()
            jambdetails = db.session.query(Jamb).filter(Jamb.email==email).limit(5).all()
            return render_template('all.html',allstudents=allstudents, selectedstudent=selectedstudent, oleveldetails=oleveldetails, jambdetails=jambdetails,date=date)
        else:
            oleveldetails = db.session.query(Olevel).filter(Olevel.email==email).limit(9).all()
            jambdetails = db.session.query(Jamb).filter(Jamb.email==email).limit(5).all()
            return render_template('all.html',allstudents=allstudents, selectedstudent=selectedstudent, oleveldetails=oleveldetails, jambdetails=jambdetails)
    else:
        return redirect('/psameeetech/admin login/')



@app.route('/details/<email>/',methods=['GET','POST'])
def more(email):
    session_collected = session.get('loggedin')
    if session_collected:
        student = db.session.query(Students).filter(Students.email==email).first()
        oleveldetails = db.session.query(Olevel).filter(Olevel.email==email).limit(9).all()
        jambdetails = db.session.query(Jamb).filter(Jamb.email==email).limit(5).all()
        return render_template('details2.html',student=student,oleveldetails=oleveldetails, jambdetails=jambdetails)
    else:
        return redirect('/psameeetech/admin login/')




@app.route('/change status/<email>/',methods=['GET','POST'])
def change_status(email):
    session_collected = session.get('loggedin')
    if session_collected:
        student=db.session.query(Students).filter(Students.email==email).first()
        name=student.fname
        db.session.execute(f"update students set status='processed' where email='{email}'")
        db.session.commit()
        flash(f'{name} has been processed.')
        return redirect('/psameeetech/forms-received/')
    else:
        return redirect('/psameeetech/admin login/')










@app.route('/psameeetech/user_viewsubmission/')
def user_viewsubmission():
        session_collected = session.get('loggedin')
        if session_collected:
            record = db.session.query(Students).filter(Students.email==session_collected).first()
            orecord = db.session.query(Olevel).filter(Olevel.email==session_collected).all()
            jrecord = db.session.query( Jamb).filter(Jamb.email==session_collected).all()
            states=db.session.query(States).all()
            return render_template("user-viewsubmission.html",record=record,states=states,orecord=orecord,jrecord=jrecord)
        else:
            return redirect("/psameeetech/user login/")






@app.route('/psameeetech/contact the admin/')
def contactadmin():
    session_collected = session.get('loggedin')
    if session_collected:
        if request.method=="GET":
            record=db.session.query(Students).filter(Students.email==session_collected).first()
            return render_template('contactadmin.html',record=record)
    else:
        return redirect("/psameeetech/user login/")

    



@app.errorhandler(404)
def page_not_found(e):
    session_collected = session.get('loggedin')
    if session_collected:
        return render_template('error-page.html'),404
    else:
        return redirect("/psameeetech/user login/")







@app.route('/psameeetech/forms-received/')
def forms_received():
    session_collected = session.get('loggedin')
    if session_collected:
        submitted_forms=db.session.query(Students).filter(Students.fname!="").all()
        for i in submitted_forms:
            time = i.regdate.strftime('%a  %d  %b , %Y ,%H:%M:%S')
            dob = i.dob
        return render_template('forms-received.html',submitted_forms=submitted_forms,time=time,dob=dob)
    else:
        return redirect("/psameeetech/admin login/")
 



    
            
 

@app.route('/psameeetech/admissionform/',methods=['POST','GET'])
def admission_form():
    session_collected = session.get('loggedin')
    if session_collected:
        if request.method=="GET":
            courses=db.session.query(Courses).all()
            states=db.session.query(States).all()
            record=db.session.query(Students).filter(Students.email==session_collected).first()
            return render_template('admissionform.html',record=record,states=states,courses=courses)
        else:
            record=db.session.query(Students).filter(Students.email==session_collected).first()
            if record.fname or record.lname or record.midname or record.phone or record.gender:
                flash('Attention!!!. You cannot fill this form twice. Kindly contact the admin to make desired changes.')
                return redirect('/psameeetech/contact the admin/',record=record)
            else:
                """Picture upload code. This code changes the file name to random numbers"""

                allowed = ['.jpg','.png','.jpeg']
                fileobj=request.files['pix']
                new_file=""
                if fileobj.filename != "":
                    original_name=fileobj.filename
                    filename,ext = os.path.splitext(original_name)
                    if ext.lower() in allowed:
                        xter_list=random.sample(string.ascii_letters,12)
                        new_file="".join(xter_list)+ext
                        fileobj.save(f'pkg/static/uploads/{new_file}')
                    else:
                        flash("Please upload a file with a valid format")
                """picture upload code ends"""

                fname=request.form.get('fname')
                lname=request.form.get('lname')
                midname=request.form.get('midname')
                phone=request.form.get('phone')           
                gender=request.form.get('gender')
                marital=request.form.get('marital')
                program=request.form.get('program')
                manualpro=request.form.get('manualpro')
                studymode=request.form.get('studymode')
                stateofres=request.form.get('stateofres')
                lgaofres=request.form.get('lgaofres')
                cityofres=request.form.get('cityofres')
                resaddress=request.form.get('resaddress')            
                dob=request.form.get('dob')
                placeofbirth=request.form.get('placeofbirth')
                nationality=request.form.get('nationality')
                stateoforigin=request.form.get('stateoforigin')
                originlga=request.form.get('originlga')
                hometown=request.form.get('hometown')
                nxtofkin=request.form.get('nxtofkin')
                nxtofkinphone=request.form.get('nxtofkinphone')
                relwithkin=request.form.get('relwithkin')
                scardexamtype=request.form.get('scardexamtype')
                cardyear=request.form.get('cardyear')
                cadserialnum=request.form.get('cadserialnum')
                cardpin=request.form.get('cardpin')
                resultcombo=request.form.get('resultcombo')
                record = db.session.query(Students).filter(Students.email==session_collected).first()
                record.fname=fname
                record.lname=lname
                record.midname=midname
                record.phone=phone
                record.gender=gender
                record.marital=marital
                record.program=program
                record.manualpro=manualpro
                record.studymode=studymode
                record.stateofres=stateofres
                record.lgaofres=lgaofres
                record.cityofres=cityofres
                record.resaddress=resaddress
                record.pic=new_file
                record.dob=dob
                record.nationality=nationality
                record.stateoforigin=stateoforigin
                record.originlga=originlga
                record.hometown=hometown
                record.nxtofkin=nxtofkin
                record.relwithkin=relwithkin
                record.placeofbirth=placeofbirth
                record.nxtofkinphone=nxtofkinphone
                record.scardexamtype=scardexamtype
                record.cardyear=cardyear
                record.cadserialnumber=cadserialnum
                record.cardpin=cardpin
                record.resultcombo=resultcombo
                record.status="pending"

                """collecting olevel data"""
                maths=request.form.get('maths')
                score1=request.form.get('score1')
                eng=request.form.get('eng')
                score2=request.form.get('score2')
                subject3=request.form.get('subject3')
                score3=request.form.get('score3')
                subject4=request.form.get('subject4')
                score4=request.form.get('score4')
                subject5=request.form.get('subject5')
                score5=request.form.get('score5')
                subject6=request.form.get('subject6')
                score6=request.form.get('score6')
                subject7=request.form.get('subject7')
                score7=request.form.get('score7')
                subject8=request.form.get('subject8')
                score8=request.form.get('score8')
                subject9=request.form.get('subject9')
                score9=request.form.get('score9')
                email=session_collected

                """collecting jamb data"""
                english = request.form.get('english')
                jambscore1=request.form.get('jamscore1')
                jambsub2=request.form.get('jamsub2')
                jambscore2=request.form.get('jamscore2')
                jambsub3=request.form.get('jamsub3')
                jambscore3=request.form.get('jamscore3')
                jambsub4=request.form.get('jamsub4')
                jambscore4=request.form.get('jamscore4')
                jambtotal=int(jambscore1) + int(jambscore2) + int(jambscore3) + int(jambscore4)
                
                """inserting all values collected to thheir respective tables"""
                query4olevel= f"insert into olevel(subject,score,email) values ('{maths}','{score1}','{email}'), ('{eng}','{score2}','{email}') ,('{subject3}','{score3}','{email}'), ('{subject4}','{score4}','{email}'), ('{subject5}','{score5}','{email}'),('{subject6}','{score6}','{email}'),('{subject7}','{score7}','{email}'), ('{subject8}','{score8}','{email}'), ('{subject9}','{score9}','{email}')"
                query4jamb=f"insert into jamb(subject,score,email) values ('{english}','{jambscore1}','{email}'),('{jambsub2}','{jambscore2}','{email}'),('{jambsub3}','{jambscore3}','{email}'),('{jambsub4}','{jambscore4}','{email}'),('jambtotal','{jambtotal}','{email}')"
                db.session.execute(query4olevel)
                db.session.execute(query4jamb)
                db.session.commit()
                
                flash(f'Congratulations {fname}, The Admin has received your details. It will be processed within the next 2 hours. Thank you!')
                return redirect('/psameeetech/user dashboard/')
    else:
        return redirect("/psameeetech/user login/")

 
stores = [
    {
        "name":"mystore", 
        "items":[ {"name":"chair","price":400} ]
    }
]

@app.route('/stores',methods=['POST','GET'])
def addstore():
    if request.method == "GET":
        return {"stores":stores}
    if request.method == "POST":
        c = request.get_json()
        if c:
            newstore_name = c["name"]
            k = {"name":newstore_name,"item":[]}
            stores.append(k)
            return {k}
        else:
            return "post has incorrect content. kindly check the api's documentation"
