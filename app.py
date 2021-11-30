# My own Library
# from course import get_course_all, get_course_no_repeat, get_course_section, get_course_detail

# Library from Flask

from datetime import datetime
from logging import StringTemplateStyle
from os import name
from google.cloud import bigquery
from google.cloud.bigquery import client, dbapi, query
from bigquery import GetUserName
from flask import * #Flask, render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint, randrange
import smtplib
from flask import jsonify
from flask import json
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from tkinter import *  
  
from tkinter import messagebox
from tkinter import messagebox  
from datetime import datetime,timedelta
import uuid
from json import dumps 
import random
import string  
  




"""
==================================================================================================
||        Data Base Setup                                                                       ||
==================================================================================================
"""

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://mzqzzqbbqshuyu:8dac9f5ddbfbc9f7556554c9d4d7b101acc45c7b2d8bce1c9ae90931f464c22f@ec2-54-205-61-191.compute-1.amazonaws.com:5432/d55vjv88et7bmh"
# app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

# db = SQLAlchemy(app)

# class users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     studentID = db.Column(db.String(10), nullable=False, unique=True)
#     phash = db.Column(db.String(120), nullable=False)

# class registers(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     studentID = db.Column(db.String(10), nullable=False)
#     courseID = db.Column(db.String(10), nullable=False)
#     section = db.Column(db.Integer, nullable=False)


"""
==================================================================================================
||        App Route                                                                             ||
==================================================================================================
"""
@app.route('/')



@app.route('/login', methods=['GET', 'POST'])
def login():    
    if request.method == "GET":
        return render_template('pages-login.html')

    else:
        client =bigquery.Client()
        cust_table_id='bookit-court-booking-system.main.Customer'
        username = request.form['username']
        password = request.form['passwword']

        user_result=False

        query="""
            SELECT * FROM main.Customer
        """
        query_job = client.query(query)
        for row in query_job:
            if username == row['username'] and password==row['password']:
                usertype=row['UserType']
                name=row['name']
                email=row['email']
                phoneNum=row['PhoneNumber']
                blockNum=row['BlockNumber']
                unitNum=row['UnitNumber']
                
                user_result=True

        if user_result:
            session['loggedIn'] = TRUE
            session['username'] = username
            session['UserType'] = usertype
            session['name']= name
            session['email']= email
            session['PhoneNumber']=phoneNum
            session['BlockNumber']=blockNum
            session['UnitNumber']=unitNum
            session['password']=password
            
            if usertype=="ADMIN":
                return redirect("/IndexAdmin")
            elif usertype=="USER":
                return redirect("/IndexResident")
        else:
            #messagebox.showinfo("Fail log in","Fail to log in")
            
            return redirect('/login')


@app.route('/forgetPassword')
def forgetPassword():
    return render_template('forget-password.html')

@app.route('/checkAccount',methods=['GET','POST'])
def checkAccount():
    
    userExist = False
    email = request.form['email'];
    client = bigquery.Client();
    query = """ 
        SELECT email 
        FROM `bookit-court-booking-system.main.Customer`
        WHERE email=\'""" + email + """\'
    """
    
    queryjob = client.query(query)
    
    for row in queryjob:
        if row["email"] == email:
            userExist = True
    
    if(userExist):
        return redirect(url_for('.sendOTP', email=email))
    
    else:
        return redirect('/register')

@app.route('/sendOTP')
def sendOTP():

    email = request.args['email']
    otp = randint(100000,999999)
    message = "Your OTP Code is " + str(otp) + "."
    myEmail = "bookitappdev@gmail.com"
    password = "@ppDev123"
    
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    
    server.login(myEmail,password)
    server.sendmail(myEmail,email,message)

    return render_template('otp.html',trueOTP = otp, email=email)

@app.route('/verifyOTP', methods=['GET','POST'])
def verifyOTP():
    trueOTP = request.form['trueOTP']
    enteredOTP = request.form['enteredOTP']
    email = request.form['email']
    
    if enteredOTP == trueOTP:
        return render_template('resetPassword.html',email=email)
    else:
        return redirect('/forgetPassword')

@app.route('/resetPassword', methods=['GET','POST'])
def resetPassword():
    newPW = request.form['newPW']
    renewPW = request.form['renewPW']
    email = request.form['email']
    
    if not(newPW == renewPW):
        return render_template('resetPassword.html', email=email)
    
    else:
        client = bigquery.Client()
        
        query = """
            UPDATE `bookit-court-booking-system.main.Customer`
            SET password='""" + newPW + """'
            WHERE email='""" + email + """'
        """
        query_job = client.query(query)
        
        query_job.result()
        
        #prompt successful message
        return redirect('/login')

       
@app.route('/index')
def index():
    # branchCount = getBranchCount()
    # staffCount = getStaffCount()
    # day = getCurrentDay()
    # month = getCurrentMonth()
    # year = getCurrentYear()
    # currTotalCF = round(getTotalCFcurrMonth() * 0.001,3)
    # avgCurrTotalCF = round(currTotalCF/branchCount,3)
    # culTotalCFcurrMonth = round(getCulmulativeCFcurrMonth()*0.001,3)
    # avgCulTotal = round(culTotalCFcurrMonth/branchCount,3)
    # currMonthCFperCapita = round(currTotalCF/staffCount,3)
    # safePerCapita = round(4/12,3)
    # totSafe = round(staffCount*safePerCapita/branchCount,3)
    
    # kgRecycled = round(getTotalRecycledKG(),3)
    # treesPlanted = round(getTotalTreesPlanted(),3)
    # energySaved = round(getTotalEnergySaved(),3)
    #username = GetUserName()
    return render_template('index.html')#,energySaved=energySaved,treesPlanted=treesPlanted,kgRecycled=kgRecycled,branchCountHTML=branchCount,totSafe=totSafe,staffCount=staffCount,currMonth=month,currYear=year, totalCF=currTotalCF, avgCF=avgCurrTotalCF, culTotal=culTotalCFcurrMonth, avgCulTotal=avgCulTotal,currMonthCFperCapita=currMonthCFperCapita,safe=safePerCapita,currDay=day)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":    
           
        return render_template('pages-register.html')

    else:
        client=bigquery.Client()
        cust_table_id='bookit-court-booking-system.main.Customer'

        username = request.form['inputusername']
        password = request.form['inputpassword']
        retype =request.form['inputRetype']
        name=request.form['inputName']
        email=request.form['inputEmail']
        phoneNum=request.form['inputPhoneNumber']
        BlockNum=request.form['inputBlockNumber']
        UnitNum=request.form['inputUnitNumber']

         
        if password == retype:
            

            # Check student exist or not
            
            exist=False
            query = """
            SELECT username as L
            FROM main.Customer
             """
            query_job = client.query(query)
            for row in query_job:
                if username ==row["L"]:
                    exist=True


            if(exist):
                
                return render_template('pages-register.html')
            else:
                pass
        else:
                 
            return render_template('pages-register.html')

         
        # Create new user in database
        row = [{u'username':username,u'password':password,u'name':name,u'email':email,u'PhoneNumber':phoneNum,u'BlockNumber':BlockNum,u'UnitNumber':UnitNum,u'UserType':"USER"}]
        
        errors=client.insert_rows_json(cust_table_id,row)
        if errors==[]:
            print('asd')
            #messagebox.showinfo("Account Created","User have been register! Please SignIn to continue")
        else:
            print(f'encounter error : {errors}')

        
    return redirect('/login')

@app.route('/logout')
def logout():
    session['loggedIn'] = FALSE
    session.pop('LoggedIn', None)
    session.pop('username',None)
    session.pop('Usertype',None)
    return redirect('/login')

@app.route('/IndexResident')
def IndexResident():
    
    if session['loggedIn'] == FALSE or session['UserType']=="ADMIN":
        return redirect('/login')
    
    else:
        name = session['name']
        blockNum = session['BlockNumber']
        unitNum = session['UnitNumber']
        username = session['username']
        client =bigquery.Client()
        cust_table_id='bookit-court-booking-system.main.Court1'
        query = """
        SELECT Start_Time,Booking,Available
        FROM main.Court1
        ORDER BY Start_Time
        """
        stime=[]
        query_job = client.query(query)
        for row in query_job:
            if row['Booking']==False and row['Available']==True:
                stime.append(row['Start_Time'])
                    
            else:
                pass
                              
        query = """
        SELECT Start_Time,Booking,Available
        FROM main.Court2
        ORDER BY Start_Time
        """
        c2stime=[]
        
        query_job = client.query(query)
        for row in query_job:
            if row['Booking']==False and row['Available']==True:
                c2stime.append(row['Start_Time'])
                    

            else:
                pass

        query = """
        SELECT Start_Time,Booking,Available
        FROM main.Court3
        ORDER BY Start_Time
        """
        c3stime=[]
        query_job = client.query(query)
        for row in query_job:
            if row['Booking']==False and row['Available']==True:
                c3stime.append(row['Start_Time'])
                    
            else:
                pass
        query = """
        SELECT Start_Time,Booking,Available
        FROM main.Court4
        ORDER BY Start_Time
        """
        c4stime=[]
        query_job = client.query(query)
        for row in query_job:
            if row['Booking']==False and row['Available']==True:
                c4stime.append(row['Start_Time'])
            else:
                pass

        return render_template("indexResident.html",username=username,name=name, blockNum=blockNum,unitNum=unitNum,stime=stime,
        c2stime=c2stime,c3stime=c3stime,c4stime=c4stime)

@app.route('/IndexAdmin')
def IndexAdmin():
    
    if session['loggedIn'] == FALSE or session['UserType']=="USER":
        return redirect('/login')
    
    else:    
        name = session['name']
        username = session['username']
        return render_template('IndexAdmin.html',name=name, username=username)

@app.route('/viewReservation')
def viewReservation():
    
    if session['loggedIn'] == FALSE or session['UserType']=="ADMIN":
        return redirect('/login')
    
    else:
        name = session['name']
        blockNum = session['BlockNumber']
        unitNum = session['UnitNumber']
        username = session['username']
        client =bigquery.Client()
        cust_table_id='bookit-court-booking-system.main.Reservation'
        rlist=[]
        cust=name
        bid=[]

        
        # View today reservation of user
        query = """
        SELECT Court_ID, Customer_Name,Approve_Status, Start_Time, End_Time,Book_ID,
        FORMAT_TIMESTAMP("%b-%d-%Y",Reserve_Time) as rDate,FORMAT_TIME("%R",Start_Time) as stime,
        EXTRACT (DATE FROM CURRENT_TIMESTAMP()) as today,EXTRACT (DATE FROM Reserve_Time) as date
        FROM main.Reservation
        ORDER BY Reserve_Time DESC
        """
        query_job = client.query(query)
        for row in query_job:
            cust=row['Customer_Name']
            if cust==name:
                if row['date']==row['today']:
                    rlist.append("Court Number: "+row['Court_ID'])
                    rlist.append("Reservation Date: "+row['rDate'])
                    rlist.append("Reservation Time: "+row['stime'])                    
                    rlist.append("Booking Status: ")
                    rlist.append(row['Approve_Status'])
                    rlist.append("Booking ID: ")
                    rlist.append(row['Book_ID'])
                    bid.append(row['Book_ID'])

                   

        return render_template("viewReservation.html",name=name,blockNum=blockNum,unitNum=unitNum,username=username,
        cust=cust,rlist=rlist,bid=bid)
            

@app.route('/reservations')
def reservations():
    if session['loggedIn'] == FALSE or session['UserType']=="ADMIN":
        return redirect('/login')
    
    else:
        name = session['name']
        blockNum = session['BlockNumber']
        unitNum = session['UnitNumber']
        username = session['username']

    client =bigquery.Client()
    cust_table_id='bookit-court-booking-system.main.Reservation'
    rlist=[]
    cust=name
    bid=[]           
    # View reservation history of user
    query = """
    SELECT Court_ID, Customer_Name,Approve_Status,FORMAT_TIMESTAMP("%b-%d-%Y",Reserve_Time) as rDate,Book_ID,
    FORMAT_TIMESTAMP("%T",Start_Time) as stime
    FROM main.Reservation
    ORDER BY Reserve_Time DESC
    """
    query_job = client.query(query)
    for row in query_job:
        cust=row['Customer_Name']
        if cust==name:
            rlist.append("Court Number: "+row['Court_ID'])
            rlist.append("Reservation Date: "+row['rDate'])
            rlist.append("Reservation Time: "+row['stime'])                    
            rlist.append("Booking Status: ")
            rlist.append(row['Approve_Status'])
            rlist.append("Booking ID: ")
            rlist.append(row['Book_ID'])
            bid.append(row['Book_ID'])

            

    return render_template("reservations.html",name=name,blockNum=blockNum,unitNum=unitNum,username=username,
        cust=cust,rlist=rlist,bid=bid)


@app.route('/makereservation<int:court_id>', methods=['GET', 'POST'])
def zhixuen(court_id):   
    if session['loggedIn'] == FALSE or session['UserType']=="ADMIN":
        return redirect('/login')  
    else:
        client=bigquery.Client()
        cust_table_id='bookit-court-booking-system.main.Court{}'.format(court_id)
        query = """
        SELECT CURRENT_TIMESTAMP() as now,FORMAT_TIMESTAMP("%F",CURRENT_TIMESTAMP()) as stimestampfront,
        Start_Time,Booking,Available
        FROM main.Court{}
        ORDER BY Start_Time
        """.format(court_id)
        stime=[]
        query_job = client.query(query)
        for row in query_job:
            if row['Booking']==False and row['Available']==False:
                stime.append(row['Start_Time'])      
            else:
                pass
            letters = string.digits
            Book_ID = str(''.join(random.choice(letters) for i in range(16)))
            Customer_Name = session["name"]
            Court_ID = str(court_id)
            Customer_Phone_Number = session['PhoneNumber']
            #Reserve_Time =row['now']
        if request.method == "GET":
            return render_template('zhixuen-test.html',Customer_Name=Customer_Name,Book_ID=Book_ID,Court_ID=Court_ID, Customer_Phone_Number=Customer_Phone_Number,stime=stime)
        else:
            print("asd")
            Start_Time_Form = (str(request.form.get('Start_time')))
            date_object_start_time = datetime.strptime(Start_Time_Form, "%H:%M:%S")
            date_object_end_time = date_object_start_time + timedelta(hours=1)
            print(date_object_start_time.time())
            print(date_object_end_time.time())
            print(type(date_object_start_time.time()))
            print(type(date_object_end_time.time()))

            client=bigquery.Client()
            cust_table_id='bookit-court-booking-system.main.Reservation'
            """INSERT INTO bookit-court-booking-system.main.Reservation 
            (Customer_Name,Book_ID,Court_ID,Approve_Status,Customer_Phone_Number,Reserve_Time,Start_Time,End_Time) 
            VALUES 
            (bryan,7891150093213407,4,True,6131666166, CURRENT_TIMESTAMP(),TIME "01:00:00",TIME "02:00:00")"""

            query = """
            INSERT INTO bookit-court-booking-system.main.Reservation 
            (Customer_Name,Book_ID,Court_ID,Approve_Status,Customer_Phone_Number,Reserve_Time,Start_Time,End_Time) 
            VALUES 
            ('""" + Customer_Name +"""','"""+ Book_ID + """','""" + Court_ID + """',True,'""" + Customer_Phone_Number + """', CURRENT_TIMESTAMP(),TIME \"""" + str(date_object_start_time.time()) + """\",TIME \"""" + str(date_object_end_time.time()) + """\")"""

            query_job = client.query(query)

            print('success')
            return redirect("/viewReservation")

#Below this is not under AD project

#
# @app.route('/forgot-password')
# def forgotpassword():
#     return render_template('forgot-password.html')


@app.route('/charts-apexcharts')
def apexcharts():
    # month = getCurrentMonth()
    # year = getCurrentYear()
    return render_template('charts-apexcharts.html')#,currMonth = month,currYear=year)

@app.route('/charts-chartjs')
def chartsjs():
    return render_template('charts-chartjs.html')

@app.route('/charts-echarts')
def echarts():
    return render_template('charts-echarts.html')

@app.route('/tables-data')
def tablesdata():
    return render_template('tables-data.html')


@app.route('/tables-general')
def tablesgeneral():
    return render_template('tables-general.html')

@app.route('/contact')
def contact():
    return render_template('pages-contact.html')

@app.route('/404')
def four0four():
    return render_template('pages-error-404.html')


@app.route('/blank')
def blank():
    return render_template('pages-blank.html')

@app.route('/profile')
def profile():
    
    if session['loggedIn'] == FALSE or session['UserType']=="ADMIN":
        return redirect('/login')
    
    else: 
        username = session['username']
        usertype = session['UserType']
        name = session['name']
        email = session['email']
        phoneNum = session['PhoneNumber']
        blockNum = session['BlockNumber']
        unitNum = session['UnitNumber']
            
        return render_template('users-profile.html',username=username, usertype=usertype,name=name,email=email,phoneNum=phoneNum,blockNum=blockNum,unitNum=unitNum)



@app.route('/update-profile', methods=['GET', 'POST'])
def updateProfile():
    
    if request.method == "GET":
        return render_template('users-profile.html')

    else: 
        
        username = session['username']
        
        newName = request.form['fullName']
        newUsername = request.form['username']
        newEmail = request.form['email']
        newPhoneNum = request.form['phoneNum']
        newBlockNum = request.form['blockNum']
        newUnitNum = request.form['unitNum']
        
        usertype = session['UserType']
        # name = session['name']
        # email = session['email']
        # phoneNum = session['PhoneNumber']
        # blockNum = session['BlockNumber']
        # unitNum = session['UnitNumber']
        
        client = bigquery.Client()
        
        query = """
            UPDATE `bookit-court-booking-system.main.Customer`
            SET username='""" + newUsername + """', name='""" + newName + """', email='"""+ newEmail + """', PhoneNumber='""" + newPhoneNum + """',BlockNumber='""" + newBlockNum + """',UnitNumber='""" + newUnitNum + """'
            WHERE username='""" + username + """'
        """
        query_job = client.query(query)
        
        query_job.result()

        # print(f"DML query modified {query_job.num_dml_affected_rows} rows.")
        # return query_job.num_dml_affected_rows
        
        session['username'] = newUsername
        session['UserType'] = usertype
        session['name']= newName
        session['email']= newEmail
        session['PhoneNumber']=newPhoneNum
        session['BlockNumber']=newBlockNum
        session['UnitNumber']=newUnitNum
        
        if usertype == "USER":
            return redirect('/profile')

        else:
            return redirect('/profile-admin')
    #return render_template('users-profile.html',username=newUsername, usertype=usertype,name=newName,email=newEmail,phoneNum=newPhoneNum,blockNum=newBlockNum,unitNum=newUnitNum)


@app.route('/update-password', methods=['GET', 'POST'])
def updatePassword():
    
    if request.method == "GET":
        return render_template('users-profile.html')

    else: 
        
        username = session['username']
        
        password = request.form['password']
        newPassword = request.form['newpassword']
        renewPassword = request.form['renewpassword']
        # newUsername = request.form['username']
        # newEmail = request.form['email']
        # newPhoneNum = request.form['phoneNum']
        # newBlockNum = request.form['blockNum']
        # newUnitNum = request.form['unitNum']
        
        usertype = session['UserType']
        oripassword = session['password'];
        # name = session['name']
        # email = session['email']
        # phoneNum = session['PhoneNumber']
        # blockNum = session['BlockNumber']
        # unitNum = session['UnitNumber']
        
        if not (newPassword == renewPassword and password == oripassword):
            #prompt wrong renewpassword message
            if usertype == "USER":
                return redirect('/profile')
            else:
                return redirect('/profile-admin')
        
        else:
        
            client = bigquery.Client()
            
            query = """
                UPDATE `bookit-court-booking-system.main.Customer`
                SET password='""" + newPassword + """'
                WHERE username='""" + username + """'
            """
            query_job = client.query(query)
            
            query_job.result()
            
            #prompt successful message
            
            return redirect('/logout')


@app.route('/profile-admin')
def profileAdmin():
    
    if session['loggedIn'] == FALSE or session['UserType']=="USER":
        return redirect('/login')
    
    else:      
        username = session['username']
        usertype = session['UserType']
        name = session['name']
        email = session['email']
        phoneNum = session['PhoneNumber']
        blockNum = session['BlockNumber']
        unitNum = session['UnitNumber']    
        return render_template('admin-profile.html',username=username, usertype=usertype,name=name,email=email,phoneNum=phoneNum,blockNum=blockNum,unitNum=unitNum)


@app.route('/faq')
def faq():
    return render_template('pages-faq.html')

# @app.route('/buttons')
# def buttons():
#     return render_template('buttons.html')

# @app.route('/cards')
# def cards():
#     return render_template('cards.html')

# @app.route('/layout')
# def layout():
#     return render_template('layout.html')


# @app.route('/utilities-animation')
# def utilitiesAnimation():
#     return render_template('utilities-animation.html')

# @app.route('/utilities-border')
# def utilitiesBorder():
#     return render_template('utilities-border.html')

# @app.route('/utilities-color')
# def utilitiesColor():
#     return render_template('utilities-color.html')

# @app.route('/utilities-other')
# def utilitiesOther():
#     return render_template('utilities-other.html')

# @app.route('/update-consumption',methods=['GET','POST']) 
# def updateConsumption():
#     day = getCurrentDay()
#     month = getCurrentMonth()
#     year = getCurrentYear()
    
#     if request.method == 'POST':
#         form = request.form.get(exampleFirstName)
#         flask(f"update {form}")
#         return redirect(url_for("index"))
    
#     return render_template('update-consumption.html',currMonth=month,currYear=year)


# @app.route('/home')
# def home():
#     studentID = None
#     course_registered = []
#     if 'user' in session:
#         studentID = session['user']

#         user_course = registers.query.filter_by(studentID=studentID).all()
#         for course in user_course:
#             course_registered.append(get_course_detail(course.courseID, str(course.section)))

#     return render_template('home.html', studentID=studentID, courses=course_registered)

# @app.route('/course')
# def course():
#     list_courses = get_course_no_repeat()
#     return render_template('course.html', courses=list_courses)

# @app.route('/section')
# def section():
#     # Get Method
#     courseID = request.args.get('courseID')
#     section_list = get_course_section(courseID)
    
#     return render_template('section.html', sections=section_list, courseID=courseID)

# @app.route('/enrollment')
# def enrollment():
#     courseID = request.args.get('courseID')
#     section = request.args.get('section')

#     if not 'user' in session:
#         flash("Please Login to Enrol in the Course!")
#         return redirect(url_for('login'))

#     studentID = session['user']
#     course_registered = registers.query.filter_by(studentID=studentID).filter_by(courseID=courseID).first()

#     if course_registered:
#         flash(f"Error! {courseID} already registered!",)
#         return redirect(url_for('course'))

#     course = registers(studentID=studentID, courseID=courseID, section=section)
#     db.session.add(course)
#     db.session.commit()

#     flash(f"{courseID} register successfully.", "register")
#     return redirect(url_for('home'))

# @app.route('/remove', methods=['GET', 'POST'])
# def remove():
#     studentID = None
#     if 'user' in session:
#         studentID = session['user']

#     if request.method == "GET":
#         user_courses = []
#         db_user_courses = registers.query.filter_by(studentID=studentID).all()
#         for course in db_user_courses:
#             user_courses.append(course.courseID)
    
#         return render_template('remove.html', courses=user_courses)
    
#     else:
#         courseID = request.form.get('course')
         
#         course = registers.query.filter_by(studentID=studentID).filter_by(courseID=courseID).first()
#         db.session.delete(course)
#         db.session.commit()

#         flash(f"{courseID} removed.", "remove")
#         return redirect(url_for('home'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == "GET":
#         return render_template('login.html')

#     else:
#         studentID = request.form.get('inputStudentID')
#         password = request.form.get('inputPassword')

#         user_result = users.query.filter_by(studentID=studentID).first()

#         if not user_result:
#             flash('StudentID or Password incorrect!')
#             return redirect(url_for('login'))

#         elif check_password_hash(user_result.phash, password):
#             session['user'] = studentID
#             return redirect(url_for('home'))

#         else:
#             flash('StudentID or Password incorrect!')
#             return redirect(url_for('login'))

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == "GET":
#         return render_template('register.html')

#     else:
#        studentID = request.form.get('inputStudentID')
#         password = request.form.get('inputPassword')
#         retype = request.form.get('inputRetype')
#         phash = None

#         if password == retype:
#             phash = generate_password_hash(password)

#             # Check student used or not
#             user_result = users.query.filter_by(studentID=studentID).first()

#             if user_result:
#                 flash("Student ID have been register! Please SignIn")
#                 return redirect(url_for('register'))

#         elif len(studentID) > 9:
#             flash("Student ID Invalid! Please try again.")
#             return redirect(url_for('register'))

#         else:
#             flash("Password not same! Please try again.")
#             return redirect(url_for('register'))

#         # Create new user in database
#         user = users(studentID = studentID, phash = phash)
#         db.session.add(user)
#         db.session.commit()
        
#         # Update user in session
#         session['user'] = studentID

#         flash("Account Created", "register")
#         return redirect(url_for('home'))

# @app.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect(url_for('home'))