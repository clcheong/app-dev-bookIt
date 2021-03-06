# Library from Flask

from google.cloud import bigquery
from google.cloud.bigquery import client, dbapi, query
from bigquery import GetUserName
from flask import * #Flask, render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint, randrange
import smtplib
import re
from flask import jsonify
from flask import json
# from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, session, flash, url_for
from datetime import date

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
  

# $env:FLASK_ENV = "development"
# $env:GOOGLE_APPLICATION_CREDENTIALS="D:\UTM DEGREE\year3\sem1\Application Development\Sport Booking System\bookit-court-booking-system-1-0983f119afe8.json"

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
        cust_table_id='bookit-court-booking-system-1.main.Customer'
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
        FROM `bookit-court-booking-system-1.main.Customer`
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
            UPDATE `bookit-court-booking-system-1.main.Customer`
            SET password='""" + newPW + """'
            WHERE email='""" + email + """'
        """
        query_job = client.query(query)
        
        query_job.result()
        
        #prompt successful message
        return redirect('/login')

       
@app.route('/index')
def index():
    return render_template('index.html')#,energySaved=energySaved,treesPlanted=treesPlanted,kgRecycled=kgRecycled,branchCountHTML=branchCount,totSafe=totSafe,staffCount=staffCount,currMonth=month,currYear=year, totalCF=currTotalCF, avgCF=avgCurrTotalCF, culTotal=culTotalCFcurrMonth, avgCulTotal=avgCulTotal,currMonthCFperCapita=currMonthCFperCapita,safe=safePerCapita,currDay=day)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":    
           
        return render_template('pages-register.html')

    else:
        client=bigquery.Client()
        cust_table_id='bookit-court-booking-system-1.main.Customer'

        username = request.form['inputusername']
        password = request.form['inputpassword']
        retype =request.form['inputRetype']
        name=request.form['inputName']
        email=request.form['inputEmail']
        phoneNum=request.form['inputPhoneNumber']
        BlockNum=request.form['inputBlockNumber']
        UnitNum=request.form['inputUnitNumber']

        #make sure name has no numbers
        x = re.findall("[0-9]",name)
        if x:
            return render_template('pages-register.html')
        
        #make sure blockNum has no numbers
        x = re.findall("[A-Z][A-Z]", BlockNum)
        if not (x and (len(BlockNum) == 2)):
            return render_template('pages-register.html')
        
        #make sure email is correct format
        x = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not (re.fullmatch(x,email)):
            return render_template('pages-register.html')
        
        #make sure phone is numbers only
        x = re.findall("^[0-9]*$",phoneNum)
        if not x:
            return render_template('pages-register.html')
        
        #make sure unitNum is numbers only
        x = re.findall("[0-9][0-9][0-9][0-9]",UnitNum)
        if not (x and (len(UnitNum) == 4)):
            return render_template('pages-register.html')
                 
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

        
    return redirect('/IndexAdmin')

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
        cust_table_id='bookit-court-booking-system-1.main.Court1'
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
        client = bigquery.Client()

        query="""
           SELECT *
           FROM `bookit-court-booking-system-1.main.Reservation`
           WHERE Reserve_Time>=TIMESTAMP(TIMESTAMP_TRUNC(CURRENT_DATETIME(),DAY))
           ORDER BY Court_ID ASC
        """

        query_job = client.query(query)
        # print("The query data:")
        name = session['name']
        username = session['username']

        today=date.today()
        d1 = today.strftime("%Y-%m-%d")
        query_feedback = """
        SELECT FeedbackDetails,FORMAT_DATETIME("%T",Time) as time,Status,EXTRACT (DATE FROM CURRENT_DATETIME()) as today, EXTRACT (DATE FROM Time) as date
        FROM main.Feedback WHERE Time>= DATETIME_TRUNC(CURRENT_DATE(),DAY)
        ORDER BY Time DESC
        """
        query_job_feedback = client.query(query_feedback)

        return render_template('IndexAdmin.html',name=name, username=username, bookingData=query_job,FeedbackData=query_job_feedback)

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
        cust_table_id='bookit-court-booking-system-1.main.Reservation'
        rlist=[]
        cust=name
        bid=[]
        startTime=[]
        oldCourtID = []
        
        # View today reservation of user
        query = """
        SELECT Court_ID, Customer_Name,Approve_Status, Start_Time, End_Time,Book_ID,
        FORMAT_TIMESTAMP("%b-%d-%Y",Reserve_Time) as rDate,FORMAT_TIME("%T",Start_Time) as stime,
        EXTRACT (DATE FROM CURRENT_TIMESTAMP()) as today,EXTRACT (DATE FROM Reserve_Time) as date
        FROM main.Reservation WHERE Approve_Status=True
        ORDER BY Reserve_Time DESC
        """
        query_job = client.query(query)
        for row in query_job:
            cust=row['Customer_Name']
            if cust==username:
                if row['date']==row['today']:
                    rlist.append("Court Number: "+row['Court_ID'])
                    rlist.append("Reservation Date: "+row['rDate'])
                    rlist.append("Reservation Time: "+row['stime'])                    
                    rlist.append("Booking Status: ")
                    rlist.append(row['Approve_Status'])
                    rlist.append("Booking ID: ")
                    rlist.append(row['Book_ID'])
                    bid.append(row['Book_ID'])
                    startTime.append(row['stime'])
                    oldCourtID.append(row['Court_ID'])

        return render_template("viewReservation.html",name=name,blockNum=blockNum,unitNum=unitNum,username=username,
        cust=cust,rlist=rlist,bid=bid,startTime=startTime,oldCourtID=oldCourtID)

@app.route('/AdminEditBooking<Booking_ID>',methods=['GET', 'POST'])
def AdminEditBooking(Booking_ID):
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

        client=bigquery.Client()
        
        query ="""
        SELECT * FROM main.Reservation 
        WHERE Book_ID = "{}"
        """.format(Booking_ID)
        
        query_job = client.query(query)

        
        for row in query_job:
            Customer_Name=row['Customer_Name']   
            Customer_Phone_Number=row['Customer_Phone_Number']
            Customer_initialTime =row['Start_Time']
            court_id=row['Court_ID']    


        query = """
        SELECT Start_Time,Booking,Available
        FROM main.Court{}
        ORDER BY Start_Time
        """.format(court_id)

        stime=[]
        query_job = client.query(query)
        for row in query_job:
            if row['Booking']==False and row['Available']==True:
                stime.append(row['Start_Time'])      
            else:
                pass
        
        

        if request.method == "GET":
            return render_template("AdminEditBooking.html",Customer_initialTime=str(Customer_initialTime),Customer_Name=Customer_Name,Book_ID=Booking_ID,Court_ID=court_id, Customer_Phone_Number=Customer_Phone_Number,stime=stime,username=username, usertype=usertype,name=name,email=email,phoneNum=phoneNum,blockNum=blockNum,unitNum=unitNum)
        else:
            Start_Time_Form = (str(request.form.get('Start_time'))) 
            date_object_start_time = datetime.strptime(Start_Time_Form, "%H:%M:%S")
            date_object_end_time = date_object_start_time + timedelta(hours=1)
            
            
            #Set reservation Time to new   (can use already )
            client=bigquery.Client()
            query = """
            UPDATE bookit-court-booking-system-1.main.Reservation 
            set Start_Time = TIME \"""" + str(date_object_start_time.time()) + """\",
            End_Time = TIME \"""" + str(date_object_end_time.time()) + """\"
            WHERE Book_ID = '{}'
            """.format(Booking_ID)


            query_job = client.query(query)

            #Change court old time to OPEN    (got problem)
            query1 = """
                UPDATE bookit-court-booking-system-1.main.Court"""+court_id+"""
                set Booking = False
                WHERE Start_Time=TIME \"""" + str(Customer_initialTime) + """\"
            """

            query_job = client.query(query1)

            #Change court new time to CLOSE    can use
            query2 = """
            UPDATE `bookit-court-booking-system-1.main.Court""" +court_id +"""`
            SET Booking=True
            WHERE Start_Time=TIME \"""" + str(date_object_start_time.time()) + """\"
            """
            query_job = client.query(query2)
            
            return redirect("/IndexAdmin")
    


@app.route('/IndexAdminPost', methods=['POST'])
def IndexAdminPost():
    client = bigquery.Client()
    app.logger.info('Info level log')
    if 'Booking_ID' in request.form:
        Booking_ID=request.form['Booking_ID'].replace("/","");
        app.logger.info(Booking_ID)
    if 'Booking_Status' in request.form:
        Booking_Status=request.form['Booking_Status'].replace("/","");
        app.logger.info(Booking_Status)
    if 'Start_Time' in request.form:
        Start_Time=request.form['Start_Time'].replace("/","");
        app.logger.info(Start_Time)
    if 'Start_Time' in request.form:
        Start_Time=request.form['Start_Time'].replace("/","");
        app.logger.info(Start_Time)        
    if 'Court_ID' in request.form:
        Court_ID=request.form['Court_ID'].replace("/","");
        app.logger.info(Court_ID)

    if Booking_Status=="Disapprove":
        query="""
        UPDATE `bookit-court-booking-system-1.main.Reservation` 
        SET Approve_Status = FALSE
        WHERE Book_ID = {}
        """.format('\"'+Booking_ID+'\"')
        app.logger.info(query)
        query_job = client.query(query)
        query="""
        UPDATE `bookit-court-booking-system-1.main.Court{}` 
        SET Booking = FALSE
        WHERE START_TIME = {}
        """.format(Court_ID,'\"'+Start_Time+'\"')
        app.logger.info(query)
        query_job = client.query(query)        

    if Booking_Status=="Approve":
        query="""
        UPDATE `bookit-court-booking-system-1.main.Reservation` 
        SET Approve_Status = TRUE
        WHERE Book_ID = {}
        """.format('\"'+Booking_ID+'\"')
        app.logger.info(query)    
        query_job = client.query(query)
        query="""
        UPDATE `bookit-court-booking-system-1.main.Court{}` 
        SET Booking = TRUE
        WHERE START_TIME = {}
        """.format(Court_ID,'\"'+Start_Time+'\"')
        app.logger.info(query)
        query_job = client.query(query)
    
    return redirect("/IndexAdmin")

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
        cust_table_id='bookit-court-booking-system-1.main.Reservation'
        rlist=[]
        cust=name
        bid=[]           
        # View reservation history of user
        query = """
        SELECT Court_ID, Customer_Name,Approve_Status,FORMAT_TIMESTAMP("%b-%d-%Y",Reserve_Time) as rDate,Book_ID,
        FORMAT_TIME("%T",Start_Time) as stime
        FROM main.Reservation
        ORDER BY Reserve_Time DESC
        """
        query_job = client.query(query)
        for row in query_job:
            cust=row['Customer_Name']
            if cust==username:
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
        cust_table_id='bookit-court-booking-system-1.main.Court{}'.format(court_id)
        query = """
        SELECT Start_Time,Booking,Available
        FROM main.Court{}
        ORDER BY Start_Time
        """.format(court_id)
        stime=[]
        query_job = client.query(query)
        for row in query_job:
            if row['Booking']==False and row['Available']==True:
                stime.append(row['Start_Time'])      
            else:
                pass
            letters = string.digits
            Book_ID = str(''.join(random.choice(letters) for i in range(16)))
            Customer_Name = session["username"]
            Court_ID = str(court_id)
            Customer_Phone_Number = session['PhoneNumber']
            

        if request.method == "GET":
            return render_template('makereservation.html',Customer_Name=Customer_Name,Book_ID=Book_ID,Court_ID=Court_ID, Customer_Phone_Number=Customer_Phone_Number,stime=stime)
        else:
            print("asd")
            Start_Time_Form = (str(request.form.get('Start_time')))
            date_object_start_time = datetime.strptime(Start_Time_Form, "%H:%M:%S")
            date_object_end_time = date_object_start_time + timedelta(hours=1)

            client=bigquery.Client()
            query = """
            INSERT INTO bookit-court-booking-system-1.main.Reservation 
            (Customer_Name,Book_ID,Court_ID,Approve_Status,Customer_Phone_Number,Reserve_Time,Start_Time,End_Time) 
            VALUES 
            ('""" + Customer_Name +"""','"""+ Book_ID + """','""" + Court_ID + """',True,'""" + Customer_Phone_Number + """', CURRENT_TIMESTAMP(),TIME \"""" + str(date_object_start_time.time()) + """\",TIME \"""" + str(date_object_end_time.time()) + """\")"""

            query_job = client.query(query)

            query1 = """
            UPDATE `bookit-court-booking-system-1.main.Court""" +Court_ID +"""`
            SET Booking=True
            WHERE Start_Time=TIME \"""" + str(date_object_start_time.time()) + """\"
        """.format(court_id)

            query_job = client.query(query1)
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

        #make sure name has no numbers
        x = re.findall("[0-9]",newName)
        if x:
            if usertype == "USER":
                return redirect('/profile')

            else:
                return redirect('/profile-admin')
        
        #make sure blockNum has no numbers
        x = re.findall("[A-Z][A-Z]", newBlockNum)
        if not (x and (len(newBlockNum) == 2)):
            if usertype == "USER":
                return redirect('/profile')

            else:
                return redirect('/profile-admin')
        
        #make sure email is correct format
        x = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not (re.fullmatch(x,newEmail)):
            if usertype == "USER":
                return redirect('/profile')

            else:
                return redirect('/profile-admin')
                    
        #make sure phone is numbers only
        x = re.findall("^[0-9]*$",newPhoneNum)
        if not x:
            if usertype == "USER":
                return redirect('/profile')

            else:
                return redirect('/profile-admin')
                    
        #make sure unitNum is numbers only
        x = re.findall("[0-9][0-9][0-9][0-9]",newUnitNum)
        if not (x and (len(newUnitNum) == 4)):
            if usertype == "USER":
                return redirect('/profile')

            else:
                return redirect('/profile-admin')
                    
        client = bigquery.Client()
        
        query = """
            UPDATE `bookit-court-booking-system-1.main.Customer`
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
                UPDATE `bookit-court-booking-system-1.main.Customer`
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

@app.route('/court-availability')
def courtAvailable():
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
        
        client=bigquery.Client()
        court1Open="Close";
        court2Open="Close";
        court3Open="Close";
        court4Open="Close";
        
        query ="""
            Select * from main.Court1 order by Start_Time
        """
        query_job = client.query(query)
        for row in query_job:
            if   row['Available'] ==True:
                court1Open="Open"
                break
        query ="""
            Select * from main.Court2 order by Start_Time
        """
        query_job = client.query(query)
        for row in query_job:
            if   row['Available'] ==True:
                court2Open="Open"
                break
        query ="""
            Select * from main.Court3 order by Start_Time
        """
        query_job = client.query(query)
        for row in query_job:
            if   row['Available'] ==True:
                court3Open="Open"
                break
        query ="""
            Select * from main.Court4 order by Start_Time
        """
        query_job = client.query(query)
        for row in query_job:
            if   row['Available'] ==True:
                court4Open="Open"
                break

        return render_template('court-availability.html',Court1Open=court1Open,Court2Open=court2Open,Court3Open=court3Open,Court4Open=court4Open,username=username, usertype=usertype,name=name,email=email,phoneNum=phoneNum,blockNum=blockNum,unitNum=unitNum);


#Render template for Manage facility 
@app.route('/ManageFacilityAvailability')
def ManageFacility():
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
        Court1_Start_Time="-"
        Court1_End_Time="-"
        Court3_Start_Time="-"
        Court3_End_Time="-"
        Court2_Start_Time="-"
        Court2_End_Time="-"
        Court4_Start_Time="-"
        Court4_End_Time="-"
        client=bigquery.Client()

        #Court 1 start time & END TIME
        query ="""
            Select * from main.Court1 order by Start_Time
        """
        query_job = client.query(query)
        for row in query_job:
            if   row['Available'] ==True:
                Court1_Start_Time = row['Start_Time']
                break
        for row in query_job:
            if   row['Available'] ==True:
                Court1_End_Time = row['End_Time']

        #Court 2 start time & end time
        query ="""
            Select * from main.Court2 order by Start_Time
        """
        query_job = client.query(query)
        for row in query_job:
            if   row['Available'] ==True:
                Court2_Start_Time = row['Start_Time']
                break
        for row in query_job:
            if   row['Available'] ==True:
                Court2_End_Time = row['End_Time']
        
        #Court 3 Start Time and End Time
        query ="""
            Select * from main.Court3 order by Start_Time
        """
        query_job = client.query(query)
        for row in query_job:
            if   row['Available'] ==True:
                Court3_Start_Time = row['Start_Time']
                break
        for row in query_job:
            if   row['Available'] ==True:
                Court3_End_Time = row['End_Time']

        #Court 4 Start Time and End Time
        query ="""
            Select * from main.Court4 order by Start_Time
        """
        query_job = client.query(query)
        for row in query_job:
            if   row['Available'] ==True:
                Court4_Start_Time = row['Start_Time']
                break
        for row in query_job:
            if   row['Available'] ==True:
                Court4_End_Time = row['End_Time']

        
        if Court1_Start_Time==Court2_Start_Time and Court1_Start_Time==Court3_Start_Time and Court1_Start_Time==Court4_Start_Time:
            AllCourt_Start_Time = Court1_Start_Time
        else:
            AllCourt_Start_Time ="-"

        if Court1_End_Time==Court2_End_Time and Court1_End_Time==Court3_End_Time and Court1_End_Time==Court4_End_Time:
            AllCourt_End_Time=Court1_End_Time
        else:
            AllCourt_End_Time="-"

        return render_template('ManageFacility.html',Court1_Start_Time=Court1_Start_Time,Court1_End_Time=Court1_End_Time,Court2_Start_Time=Court2_Start_Time,Court2_End_Time=Court2_End_Time,Court3_Start_Time=Court3_Start_Time,Court3_End_Time=Court3_End_Time,Court4_Start_Time=Court4_Start_Time,Court4_End_Time=Court4_End_Time,AllCourt_Start_Time=AllCourt_Start_Time,AllCourt_End_Time=AllCourt_End_Time,username=username, usertype=usertype,name=name,email=email,phoneNum=phoneNum,blockNum=blockNum,unitNum=unitNum)

@app.route("/feedbacks")
def feedbacks():
    if session['loggedIn'] == FALSE or session['UserType']=="ADMIN":
        return redirect('/login')
    else:
        name = session['name']
        blockNum = session['BlockNumber']
        unitNum = session['UnitNumber']
        username = session['username']
        client =bigquery.Client()
        cust_table_id='bookit-court-booking-system-1.main.Reservation'
        # View feedback list of user
        
        query = """
        SELECT Subject,FeedbackDetails,FORMAT_DATETIME("%T",Time) as time,EXTRACT (DATE FROM CURRENT_DATETIME()) as today, EXTRACT (DATE FROM Time) as date
        FROM main.Feedback WHERE Name='{}'
        ORDER BY date DESC
        """.format(username)
        query_job = client.query(query)
        return render_template("feedbacks.html",name=name,blockNum=blockNum,unitNum=unitNum,username=username,flist=query_job)

@app.route("/Adminfeedbacks")
def Adminfeedbacks():
    if session['loggedIn'] == FALSE or session['UserType']=="User":
        return redirect('/login')
    else:
        name = session['name']
        blockNum = session['BlockNumber']
        unitNum = session['UnitNumber']
        username = session['username']
        client =bigquery.Client()
        cust_table_id='bookit-court-booking-system-1.main.Reservation'
        # View feedback list of user
        
        query = """
        SELECT Name,Subject,FeedbackDetails,FORMAT_DATETIME("%T",Time) as time,Status,EXTRACT (DATE FROM CURRENT_DATETIME()) as today, EXTRACT (DATE FROM Time) as date
        FROM main.Feedback 
        ORDER BY Time DESC
        """
        query_job = client.query(query)
        return render_template("Adminfeedbacks.html",name=name,blockNum=blockNum,unitNum=unitNum,username=username,flist=query_job)

#Update Court 1
@app.route('/Update-Facility-1', methods=['GET', 'POST'])
def UpdateFacility1():
    if request.method == "GET":
        return render_template('ManageFacility.html')
    
    else:    
        
        client=bigquery.Client()
        

        Start_time = request.form['Start_time']
        End_time = request.form['End_time']
        availability=request.form['Availability']
        available="available"
        session['Start_time']=Start_time
        session['End_time']=End_time
        if availability == available:
            
        
            query="""
                UPDATE main.Court1 set Available = False ,Booking = False
                    where Start_Time >= '01:00:00' 
                    and  End_Time <= '23:00:00'

                """  
             
            query_job = client.query(query)
            
            query_job.result()
            
            query1="""
                UPDATE main.Court1 set Available = True 
                    where Start_Time >= '""" + Start_time + """' 
                   and  End_Time <= '""" + End_time + """'

               """

            query_job = client.query(query1)
        
            query_job.result()
            
        elif availability =="unavailable":
            query="""
                UPDATE main.Court1 set Available = False,Booking = False
                    where Start_Time >= '01:00:00' 
                    and  End_Time <= '23:00:00'

                """     
            query_job = client.query(query)
        
        
            query_job.result()           
        return redirect('/ManageFacilityAvailability')
        
#Update Court 2   
@app.route('/Update-Facility-2', methods=['GET', 'POST'])
def UpdateFacility2():
    if request.method == "GET":
        return render_template('ManageFacility.html')
    
    else:    
        
        client=bigquery.Client()
       

        Start_time = request.form['Start_time']
        End_time = request.form['End_time']
        availability=request.form['Availability']
        available="available"
        session['Start_time']=Start_time
        session['End_time']=End_time
        if availability == available:
            
        
            query="""
                UPDATE main.Court2 set Available = False,Booking = False
                    where Start_Time >= '01:00:00' 
                    and  End_Time <= '23:00:00'

                """  
             
            query_job = client.query(query)
            
            query_job.result()
            
            query1="""
                UPDATE main.Court2 set Available = True
                    where Start_Time >= '""" + Start_time + """' 
                   and  End_Time <= '""" + End_time + """'

               """

            query_job = client.query(query1)
        
            query_job.result()
            
        elif availability =="unavailable":
            query="""
                UPDATE main.Court2 set Available = False,Booking = False
                    where Start_Time >= '01:00:00' 
                    and  End_Time <= '23:00:00'

                """     
            query_job = client.query(query)
        
        
            query_job.result()           
        return redirect('/ManageFacilityAvailability')

#Update Court 3
@app.route('/Update-Facility-3', methods=['GET', 'POST'])
def UpdateFacility3():
    if request.method == "GET":
        return render_template('ManageFacility.html')
    
    else:    
        
        client=bigquery.Client()
        

        Start_time = request.form['Start_time']
        End_time = request.form['End_time']
        availability=request.form['Availability']
        available="available"
        session['Start_time']=Start_time
        session['End_time']=End_time
        if availability == available:
            
        
            query="""
                UPDATE main.Court3 set Available = False,Booking = False
                    where Start_Time >= '01:00:00' 
                    and  End_Time <= '23:00:00'

                """  
             
            query_job = client.query(query)
            
            query_job.result()
            
            query1="""
                UPDATE main.Court3 set Available = True
                    where Start_Time >= '""" + Start_time + """' 
                   and  End_Time <= '""" + End_time + """'

               """

            query_job = client.query(query1)
        
            query_job.result()
            
        elif availability =="unavailable":
            query="""
                UPDATE main.Court3 set Available = False,Booking = False
                    where Start_Time >= '01:00:00' 
                    and  End_Time <= '23:00:00'

                """     
            query_job = client.query(query)
        
        
            query_job.result()           
        return redirect('/ManageFacilityAvailability')


#Update Court 4
@app.route('/Update-Facility-4', methods=['GET', 'POST'])
def UpdateFacility4():
    if request.method == "GET":
        return render_template('ManageFacility.html')
    
    else:    
        
        client=bigquery.Client()
        

        Start_time = request.form['Start_time']
        End_time = request.form['End_time']
        availability=request.form['Availability']
        available="available"
        session['Start_time']=Start_time
        session['End_time']=End_time
        if availability == available:
            
        
            query="""
                UPDATE main.Court4 set Available = False,Booking = False
                    where Start_Time >= '01:00:00' 
                    and  End_Time <= '23:00:00'

                """  
             
            query_job = client.query(query)
            
            query_job.result()
            
            query1="""
                UPDATE main.Court4 set Available = True
                    where Start_Time >= '""" + Start_time + """' 
                   and  End_Time <= '""" + End_time + """'

               """

            query_job = client.query(query1)
        
            query_job.result()
            
        elif availability =="unavailable":
            query="""
                UPDATE main.Court4 set Available = False,Booking = False
                    where Start_Time >= '01:00:00' 
                    and  End_Time <= '23:00:00'

                """     
            query_job = client.query(query)
        
        
            query_job.result()           
        return redirect('/ManageFacilityAvailability')   

#Update for all Courts              HAVENT settle
@app.route('/Update-Facility-all', methods=['GET', 'POST'])
def UpdateFacilityAll():
    if request.method == "GET":
        return render_template('ManageFacility.html')
    
    else:    
        
        client=bigquery.Client()
        

        Start_time = request.form['Start_time']
        End_time = request.form['End_time']
        availability=request.form['Availability']
        available="available"
        session['Start_time']=Start_time
        session['End_time']=End_time
        if availability == available:
            
            

            for num in range(1,5):
                StringNum=str(num)
                query="""
                         UPDATE main.Court"""+(StringNum)+""" set Available = False,Booking = False
                        where Start_Time >= '01:00:00' 
                        and  End_Time <= '23:00:00'

                     """  
             
                query_job = client.query(query)
            
                query_job.result()
            
                query1="""
                    UPDATE main.Court"""+(StringNum)+""" set Available = True
                    where Start_Time >= '""" + Start_time + """' 
                     and  End_Time <= '""" + End_time + """'

                        """

                query_job = client.query(query1)
        
                query_job.result()
            
        elif availability =="unavailable":
            
            for num in range(1,5):
                StringNum=str(num)
                query="""
                    UPDATE main.Court"""+(StringNum)+""" set Available = False,Booking = False
                    where Start_Time >= '01:00:00' 
                    and  End_Time <= '23:00:00'

                    """     
                query_job = client.query(query)
        
        
                query_job.result()           
        return redirect('/ManageFacilityAvailability')   


@app.route('/faq')
def faq():
    return render_template('pages-faq.html')

@app.route('/Reschedule', methods=['GET','POST'])
def Reschedule():
    
    if session['loggedIn'] == FALSE or session['UserType']=="ADMIN":
        return redirect('/login')
    
    else:
        bookID = request.form['bookID']
        #startTime = request.form['startTime']
        #oldCourtID = request.form['oldCourtID']
        startTime=""
        oldCourtID=""
        
        client =bigquery.Client()
        
        queryTest = """
        SELECT FORMAT_TIME("%T",Start_Time) as stime, Court_ID
        FROM `bookit-court-booking-system-1.main.Reservation`
        WHERE Book_ID=\"""" + str(bookID) + """\"
        """
        
        query_job=client.query(queryTest)
        
        for row in query_job:
            startTime = str(row['stime'])
            oldCourtID = row['Court_ID']
        
        name = session['name']
        blockNum = session['BlockNumber']
        unitNum = session['UnitNumber']
        username = session['username']
        
        cust_table_id='bookit-court-booking-system-1.main.Court1'
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

        return render_template("reschedule.html",username=username,name=name, blockNum=blockNum,unitNum=unitNum,stime=stime,
        c2stime=c2stime,c3stime=c3stime,c4stime=c4stime,bookID=bookID,startTime=startTime,oldCourtID=oldCourtID)
   
   
   
        
@app.route('/RescheduleReservation<int:court_id>', methods=['GET', 'POST'])
def makeReschedule(court_id):   
    if session['loggedIn'] == FALSE or session['UserType']=="ADMIN":
        return redirect('/login')  
    else:
        client=bigquery.Client()
        cust_table_id='bookit-court-booking-system-1.main.Court{}'.format(court_id)
        query = """
        SELECT Start_Time,Booking,Available
        FROM main.Court{}
        ORDER BY Start_Time
        """.format(court_id)
        stime=[]
        query_job = client.query(query)
        for row in query_job:
            if row['Booking']==False and row['Available']==True:
                stime.append(row['Start_Time'])      
            else:
                pass
            #letters = string.digits
        Book_ID = request.form['bookID'] #str(''.join(random.choice(letters) for i in range(16)))
        startTime = request.form['startTime']
        oldCourtID = request.form['oldCourtID']
        Customer_Name = session["name"]
        Court_ID = request.form['courtID']
        Customer_Phone_Number = session['PhoneNumber']
        #if request.method == "POST":
        return render_template('makeReschedule.html',Customer_Name=Customer_Name,Book_ID=Book_ID,Court_ID=Court_ID, Customer_Phone_Number=Customer_Phone_Number,stime=stime,startTime=startTime,oldCourtID=oldCourtID)
        #else:   #might need to seperate this into a new route
        #     print("asd")
        #     Start_Time_Form = (str(request.form.get('Start_time')))
        #     date_object_start_time = datetime.strptime(Start_Time_Form, "%H:%M:%S")
        #     date_object_end_time = date_object_start_time + timedelta(hours=1)

        #     client=bigquery.Client()
        #     query = """
        #     INSERT INTO bookit-court-booking-system-1.main.Reservation 
        #     (Customer_Name,Book_ID,Court_ID,Approve_Status,Customer_Phone_Number,Reserve_Time,Start_Time,End_Time) 
        #     VALUES 
        #     ('""" + Customer_Name +"""','"""+ Book_ID + """','""" + Court_ID + """',True,'""" + Customer_Phone_Number + """', CURRENT_TIMESTAMP(),TIME \"""" + str(date_object_start_time.time()) + """\",TIME \"""" + str(date_object_end_time.time()) + """\")"""

        #     query_job = client.query(query)

        #     query1 = """
        #     UPDATE `bookit-court-booking-system-1.main.Court""" +Court_ID +"""`
        #     SET Booking=True
        #     WHERE Start_Time=TIME \"""" + str(date_object_start_time.time()) + """\"
        # """.format(court_id)

        #     query_job = client.query(query1)
        #     print('success')
        #     return redirect("/viewReservation")


@app.route('/UpdateReschedule<int:court_id>', methods=['GET', 'POST'])
def updateReschedule(court_id):   
    if session['loggedIn'] == FALSE or session['UserType']=="ADMIN":
        return redirect('/login')  
    else:
        Book_ID = request.form['bookID'] #str(''.join(random.choice(letters) for i in range(16)))
        oldCourtID = request.form['oldCourtID']
        Customer_initialTime = request.form['startTime']
        Customer_Name = session["name"]
        Court_ID = request.form['courtID']
        Customer_Phone_Number = session['PhoneNumber']
        
        # print("asd")
        # Start_Time_Form = (str(request.form.get('Start_time')))
        # date_object_start_time = datetime.strptime(Start_Time_Form, "%H:%M:%S")
        # date_object_end_time = date_object_start_time + timedelta(hours=1)

        # client=bigquery.Client()
        # #this query might have to change to an update query
        # query = """
        # INSERT INTO bookit-court-booking-system-1.main.Reservation 
        # (Customer_Name,Book_ID,Court_ID,Approve_Status,Customer_Phone_Number,Reserve_Time,Start_Time,End_Time) 
        # VALUES 
        # ('""" + Customer_Name +"""','"""+ Book_ID + """','""" + Court_ID + """',True,'""" + Customer_Phone_Number + """', CURRENT_TIMESTAMP(),TIME \"""" + str(date_object_start_time.time()) + """\",TIME \"""" + str(date_object_end_time.time()) + """\")"""

        # query_job = client.query(query)

        # query1 = """
        # UPDATE `bookit-court-booking-system-1.main.Court""" +Court_ID +"""`
        # SET Booking=True
        # WHERE Start_Time=TIME \"""" + str(date_object_start_time.time()) + """\"
        # """.format(court_id)
        
        # #additional codes and queries might need to be added to check weather or not the previously reserved time is still later than current
        # #time. if so, need to update prvious time back to available.
        # #if not, ignore

        # query_job = client.query(query1)
        # print('success')
        # return redirect("/viewReservation")
        
        Start_Time_Form = (str(request.form.get('Start_time'))) 
        date_object_start_time = datetime.strptime(Start_Time_Form, "%H:%M:%S")
        date_object_end_time = date_object_start_time + timedelta(hours=1)
        
        
        #Set reservation Time to new   (can use already )
        client=bigquery.Client()
        query = """
        UPDATE bookit-court-booking-system-1.main.Reservation 
        set Start_Time = TIME \"""" + str(date_object_start_time.time()) + """\",
        End_Time = TIME \"""" + str(date_object_end_time.time()) + """\",
        Court_ID = \"""" + str(court_id) + """\"
        WHERE Book_ID = '{}'
        """.format(Book_ID)


        query_job = client.query(query)

        #Change court old time to OPEN    (got problem)
        query1 = """
            UPDATE bookit-court-booking-system-1.main.Court"""+str(oldCourtID)+"""
            set Booking = False
            WHERE Start_Time=TIME \"""" + str(Customer_initialTime) + """\"
        """

        query_job = client.query(query1)

        #Change court new time to CLOSE    can use
        query2 = """
        UPDATE `bookit-court-booking-system-1.main.Court""" +str(court_id) +"""`
        SET Booking=True
        WHERE Start_Time=TIME \"""" + str(date_object_start_time.time()) + """\"
        """
        query_job = client.query(query2)
        
        return redirect("/viewReservation")        
        
@app.route("/cancelreservation<bid>")
def cancelreservation(bid):
    if session['loggedIn'] == FALSE or session['UserType']=="ADMIN":
        return redirect('/login') 
    else:
        client=bigquery.Client()
        query1 = """
        UPDATE bookit-court-booking-system-1.main.Reservation 
        set Approve_Status = False
        WHERE Book_ID = '{}'
        """.format(bid)
        query_job = client.query(query1)

        query2 = """
        SELECT Court_ID, Start_Time from bookit-court-booking-system-1.main.Reservation 
        WHERE Book_ID = '{}'
        """.format(bid)
        query_job2 = client.query(query2)

        for row in query_job2:
            court_id = row["Court_ID"]
            Start_Time = row["Start_Time"]
        print(Start_Time)
        query3 = """ 
        UPDATE bookit-court-booking-system-1.main.Court{} 
        set Booking = False
        WHERE Start_Time = '{}'
        """.format(court_id, Start_Time)
        query_job = client.query(query3)
            
        
        return redirect("/viewReservation")

@app.route("/viewFeedbacks", methods=['GET','POST'])
def viewFeedbacks():
    if session['loggedIn'] == FALSE or session['UserType']=="ADMIN":
        return redirect('/login') 
    else:
        name = session['name']
        blockNum = session['BlockNumber']
        unitNum = session['UnitNumber']
        username = session['username']
        client =bigquery.Client()
        cust_table_id='bookit-court-booking-system-1.main.Reservation'
        # View today feedback of user
        
        query = """
        SELECT FeedbackID, Subject,FeedbackDetails,FORMAT_DATETIME("%T",Time) as time,Status,EXTRACT (DATE FROM CURRENT_DATETIME()) as today,
        EXTRACT (DATE FROM Time) as date
        FROM main.Feedback WHERE Name='{}' AND Time>=DATETIME_TRUNC(CURRENT_DATE(),DAY)
        ORDER BY Time DESC
        """.format(username)
        query_job = client.query(query)
        
        return render_template("viewFeedbacks.html",name=username,blockNum=blockNum,unitNum=unitNum,username=username,flist=query_job)

                    

@app.route('/giveFeedback', methods=['GET','POST'])
def giveFeedback():   
    if session['loggedIn'] == FALSE or session['UserType']=="ADMIN":
        return redirect('/login')  
    else:
        client=bigquery.Client()
        letters = string.digits
        Feedback_ID = "F" + str(''.join(random.choice(letters) for i in range(8)))
        Customer_Name=session['name']
        username=session['username']
        blockNum=session['BlockNumber']
        unitNum=session['UnitNumber']
        feedback_Form= str(request.form.get('feedback'))
        time=str(datetime.today())
        subject=str(request.form.get('subject'))
        if request.method == "GET":
            return render_template('giveFeedback.html',username=username,blockNum=blockNum,unitNum=unitNum)
        else:
            query = """
            INSERT INTO bookit-court-booking-system-1.main.Feedback 
            (FeedbackID, Name,FeedbackDetails,Time,Status,Subject,Username) 
            VALUES 
            ('""" + Feedback_ID +"""','""" + username +"""','""" + feedback_Form +"""', DATETIME \"""" + time + """\",False,'""" + subject +"""','""" + username +"""')
            """

            query_job = client.query(query)
            print('success')
            return redirect("/viewFeedbacks")


@app.route('/updateFeedback<feedback_id>', methods=['GET','POST'])
def updateFeedback(feedback_id):   
    if session['loggedIn'] == FALSE or session['UserType']=="ADMIN":
        return redirect('/login')  
    else:
        client=bigquery.Client()
        Customer_Name=session['name']
        username=session['username']
        blockNum=session['BlockNumber']
        unitNum=session['UnitNumber']
        time=str(datetime.today())
        details = []

        query2 = """
        SELECT Subject, FeedbackDetails from bookit-court-booking-system-1.main.Feedback
        WHERE FeedbackID = '{}'
        """.format(feedback_id)
        query_job2 = client.query(query2)

        for row in query_job2:
            Feedback_Subject = row['Subject']
            Feedback_Details = row["FeedbackDetails"]

        if request.method == "GET":
            return render_template('updateFeedback.html',name=Customer_Name,blockNum=blockNum, feedback_id = feedback_id, unitNum=unitNum,Feedback_Details=Feedback_Details,Feedback_Subject=Feedback_Subject)
        else:
            Feedback_Subject = request.form["Feedback_Subject"]
            Feedback_Details = request.form["Feedback_Details"]
            query = """
            UPDATE `bookit-court-booking-system-1.main.Feedback`
            SET Subject='""" + Feedback_Subject + """',FeedbackDetails='""" + Feedback_Details + """'
            WHERE FeedbackID='""" + feedback_id + """'
        """
            query_job = client.query(query)

            print('success')
            return redirect("/viewFeedbacks")
        

@app.route('/deleteFeedback<feedback_id>', methods=['GET','POST'])
def deleteFeedback(feedback_id):   
    if session['loggedIn'] == FALSE or session['UserType']=="ADMIN":
        return redirect('/login')  
    else:
        client=bigquery.Client()
        
        query = """DELETE FROM `bookit-court-booking-system-1.main.Feedback` WHERE FeedbackID = \"""" + feedback_id + """\""""
        
        query_job = client.query(query)
        
        return redirect("/viewFeedbacks")


if __name__ == "__main__":
    app.run()