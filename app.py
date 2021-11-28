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
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from tkinter import *  
  
from tkinter import messagebox  
  




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
        SELECT EXTRACT(HOUR FROM Start_Time) as hour ORDER BY Start_Time,Start_Time,Booking
        FROM main.Court1
        """
        stime=[]
        query_job = client.query(query)
        for row in query_job:
            if row['Booking']==False:
                if row['hour']==1:
                    stime.append(row['Start_Time'])
                    
                if row['hour']==2:
                    stime.append(row['Start_Time'])

                if row['hour']==3:
                    stime.append(row['Start_Time'])

                if row['hour']==4:
                    stime.append(row['Start_Time'])

                if row['hour']==5:
                    stime.append(row['Start_Time'])

                if row['hour']==6:
                    stime.append(row['Start_Time'])

                if row['hour']==7:
                    stime.append(row['Start_Time'])

                if row['hour']==8:
                    stime.append(row['Start_Time'])

                if row['hour']==9:
                    stime.append(row['Start_Time'])

                if row['hour']==10:
                    stime.append(row['Start_Time'])

                if row['hour']==11:
                    stime.append(row['Start_Time'])

                if row['hour']==12:
                    stime.append(row['Start_Time'])
        
                if row['hour']==13:
                    stime.append(row['Start_Time'])

                if row['hour']==14:
                    stime.append(row['Start_Time'])

                if row['hour']==15:
                    stime.append(row['Start_Time'])
            
                if row['hour']==16:
                    stime.append(row['Start_Time'])

                if row['hour']==17:
                    stime.append(row['Start_Time'])
                    
                if row['hour']==18:
                    stime.append(row['Start_Time'])
                    
                if row['hour']==19:
                    stime.append(row['Start_Time'])
                    
                if row['hour']==20:
                    stime.append(row['Start_Time'])
                
                if row['hour']==21:
                    stime.append(row['Start_Time'])

                if row['hour']==22:
                    stime.append(row['Start_Time'])
            else:
                pass
                              
        query = """
        SELECT EXTRACT(HOUR FROM Start_Time) as hour,Start_Time,Booking
        FROM main.Court2
        """
        c2stime1=""
        c2stime2=""
        c2stime3=""
        c2stime4=""
        c2stime5=""
        c2stime6=""
        c2stime7=""
        c2stime8=""
        c2stime9=""
        c2stime10=""
        c2stime11=""
        c2stime12=""
        c2stime13=""
        c2stime14=""
        c2stime15=""
        c2stime16=""
        c2stime17=""
        c2stime18=""
        c2stime19=""
        c2stime20=""
        c2stime21=""
        c2stime22=""
        query_job = client.query(query)
        for row in query_job:
            if row['Booking']==False:
                if row['hour']==1:
                    c2stime1=row['Start_Time']
                    
                if row['hour']==2:
                    c2stime2=row['Start_Time']

                if row['hour']==3:
                    c2stime3=row['Start_Time']

                if row['hour']==4:
                    c2stime4=row['Start_Time']

                if row['hour']==5:
                    c2stime5=row['Start_Time']

                if row['hour']==6:
                    c2stime6=row['Start_Time']

                if row['hour']==7:
                    c2stime7=row['Start_Time']

                if row['hour']==8:
                    c2stime8=row['Start_Time']

                if row['hour']==9:
                    c2stime9=row['Start_Time']

                if row['hour']==10:
                    c2stime10=row['Start_Time']

                if row['hour']==11:
                    c2stime11=row['Start_Time']

                if row['hour']==12:
                    c2stime12=row['Start_Time']
        
                if row['hour']==13:
                    c2stime13=row['Start_Time']

                if row['hour']==14:
                    c2stime14=row['Start_Time']

                if row['hour']==15:
                    c2stime15=row['Start_Time']            
            
                if row['hour']==16:
                    c2stime16=row['Start_Time']

                if row['hour']==17:
                    c2stime17=row['Start_Time']
                    
                if row['hour']==18:
                    c2stime18=row['Start_Time']
                    
                if row['hour']==19:
                    c2stime19=row['Start_Time']
                    
                if row['hour']==20:
                    c2stime20=row['Start_Time']
                
                if row['hour']==21:
                    c2stime21=row['Start_Time']

                if row['hour']==22:
                    c2stime22=row['Start_Time']

            else:
                pass

        query = """
        SELECT EXTRACT(HOUR FROM Start_Time) as hour,Start_Time,Booking
        FROM main.Court3
        """
        c3stime1=""
        c3stime2=""
        c3stime3=""
        c3stime4=""
        c3stime5=""
        c3stime6=""
        c3stime7=""
        c3stime8=""
        c3stime9=""
        c3stime10=""
        c3stime11=""
        c3stime12=""
        c3stime13=""
        c3stime14=""
        c3stime15=""
        c3stime16=""
        c3stime17=""
        c3stime18=""
        c3stime19=""
        c3stime20=""
        c3stime21=""
        c3stime22=""
        query_job = client.query(query)
        for row in query_job:
            if row['Booking']==False:
                if row['hour']==1:
                    c3stime1=row['Start_Time']
                    
                if row['hour']==2:
                    c3stime2=row['Start_Time']

                if row['hour']==3:
                    c3stime3=row['Start_Time']

                if row['hour']==4:
                    c3stime4=row['Start_Time']

                if row['hour']==5:
                    c3stime5=row['Start_Time']

                if row['hour']==6:
                    c3stime6=row['Start_Time']

                if row['hour']==7:
                    c3stime7=row['Start_Time']        
                if row['hour']==8:
                    c3stime8=row['Start_Time']

                if row['hour']==9:
                    c3stime9=row['Start_Time']

                if row['hour']==10:
                    c3stime10=row['Start_Time']

                if row['hour']==11:
                    c3stime11=row['Start_Time']

                if row['hour']==12:
                    c3stime12=row['Start_Time']
        
                if row['hour']==13:
                    c3stime13=row['Start_Time']

                if row['hour']==14:
                    c3stime14=row['Start_Time']

                if row['hour']==15:
                    c3stime15=row['Start_Time']            
            
                if row['hour']==16:
                    c3stime16=row['Start_Time']

                if row['hour']==17:
                    c3stime17=row['Start_Time']
                    
                if row['hour']==18:
                    c3stime18=row['Start_Time']
                    
                if row['hour']==19:
                    c3stime19=row['Start_Time']
                    
                if row['hour']==20:
                    c3stime20=row['Start_Time']
                
                if row['hour']==21:
                    c3stime21=row['Start_Time']

                if row['hour']==22:
                    c3stime22=row['Start_Time']
            else:
                pass
        query = """
        SELECT EXTRACT(HOUR FROM Start_Time) as hour,Start_Time,Booking
        FROM main.Court4
        """
        c4stime1=""
        c4stime2=""
        c4stime3=""
        c4stime4=""
        c4stime5=""
        c4stime6=""
        c4stime7=""
        c4stime8=""
        c4stime9=""
        c4stime10=""
        c4stime11=""
        c4stime12=""
        c4stime13=""
        c4stime14=""
        c4stime15=""
        c4stime16=""
        c4stime17=""
        c4stime18=""
        c4stime19=""
        c4stime20=""
        c4stime21=""
        c4stime22=""
        query_job = client.query(query)
        for row in query_job:
            if row['Booking']==False:
                if row['hour']==1:
                    c4stime1=row['Start_Time']
                    
                if row['hour']==2:
                    c4stime2=row['Start_Time']

                if row['hour']==3:
                    c4stime3=row['Start_Time']

                if row['hour']==4:
                    c4stime4=row['Start_Time']

                if row['hour']==5:
                    c4stime5=row['Start_Time']

                if row['hour']==6:
                    c4stime6=row['Start_Time']

                if row['hour']==7:
                    c4stime7=row['Start_Time']
                            
                if row['hour']==8:
                    c4stime8=row['Start_Time']

                if row['hour']==9:
                    c4stime9=row['Start_Time']

                if row['hour']==10:
                    c4stime10=row['Start_Time']

                if row['hour']==11:
                    c4stime11=row['Start_Time']

                if row['hour']==12:
                    c4stime12=row['Start_Time']
        
                if row['hour']==13:
                    c4stime13=row['Start_Time']

                if row['hour']==14:
                    c4stime14=row['Start_Time']

                if row['hour']==15:
                    c4stime15=row['Start_Time']            
            
                if row['hour']==16:
                    c4stime16=row['Start_Time']

                if row['hour']==17:
                    c4stime17=row['Start_Time']
                    
                if row['hour']==18:
                    c4stime18=row['Start_Time']
                    
                if row['hour']==19:
                    c4stime19=row['Start_Time']
                    
                if row['hour']==20:
                    c4stime20=row['Start_Time']
                
                if row['hour']==21:
                    c4stime21=row['Start_Time']

                if row['hour']==22:
                    c4stime22=row['Start_Time']
            else:
                pass

        return render_template("indexResident.html",username=username,name=name, blockNum=blockNum,unitNum=unitNum,stime1=stime[0],
        stime2=stime[1],stime3=stime[2],stime4=stime[3],stime5=stime[4],stime6=stime[5],stime7=stime[6],stime8=stime[7],stime9=stime[8],stime10=stime[9],
        stime11=stime[10],stime12=stime[11],stime13=stime[12],stime14=stime[13],stime15=stime[14],stime16=stime[15],stime17=stime[16],stime18=stime[17],
        stime19=stime[18],stime20=stime[19],stime21=stime[20],stime22=stime[21],c2stime1=c2stime1,c2stime2=c2stime2,c2stime3=c2stime3,
        c2stime4=c2stime4,c2stime5=c2stime5,c2stime6=c2stime6,c2stime7=c2stime7,c2stime8=c2stime8,c2stime9=c2stime9,c2stime10=c2stime10,
        c2stime11=c2stime11,c2stime12=c2stime12,c2stime13=c2stime13,c2stime14=c2stime14,c2stime15=c2stime15,c2stime16=c2stime16,
        c2stime17=c2stime17,c2stime18=c2stime18,c2stime19=c2stime19,c2stime20=c2stime20,c2stime21=c2stime21,c2stime22=c2stime22,
        c3stime1=c3stime1,c3stime2=c3stime2,c3stime3=c3stime3,c3stime4=c3stime4,c3stime5=c3stime5,c3stime6=c3stime6,c3stime7=c3stime7,
        c3stime8=c3stime8,c3stime9=c3stime9,c3stime10=c3stime10,c3stime11=c3stime11,c3stime12=c3stime12,c3stime13=c3stime13,
        c3stime14=c3stime14,c3stime15=c3stime15,c3stime16=c3stime16,c3stime17=c3stime17,c3stime18=c3stime18,c3stime19=c3stime19,
        c3stime20=c3stime20,c3stime21=c3stime21,c3stime22=c3stime22,c4stime1=c4stime1,c4stime2=c4stime2,c4stime3=c4stime3,
        c4stime4=c4stime4,c4stime5=c4stime5,c4stime6=c4stime6,c4stime7=c4stime7,c4stime8=c4stime8,c4stime9=c4stime9,c4stime10=c4stime10,
        c4stime11=c4stime11,c4stime12=c4stime12,c4stime13=c4stime13,c4stime14=c4stime14,c4stime15=c4stime15,c4stime16=c4stime16,
        c4stime17=c4stime17,c4stime18=c4stime18,c4stime19=c4stime19,c4stime20=c4stime20,c4stime21=c4stime21,c4stime22=c4stime22,)

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
        
        
        cust=name
        tcourt=""
        tstatus=""
        tstime=""
        tetime=""
        tbook_id=""
        t2court=""
        t2status=""
        t2stime=""
        t2etime=""
        t2book_id=""
        r1court=""
        r1status=""
        r1stime=""
        r1etime=""
        r1book_id=""
        r2court=""
        r2status=""
        r2stime=""
        r2etime=""
        r2book_id=""
        r3court=""
        r3status=""
        r3stime=""
        r3etime=""
        r3book_id=""
        # View reservation of user
        query = """
        SELECT Court_ID, Customer_Name, ApproveStatus,EXTRACT(HOUR FROM CURRENT_TIME()) as now,EXTRACT(DAY FROM CURRENT_DATE) as today
        EXTRACT(HOUR FROM Start_Time) as hour,Start_Time, End_Time,EXTRACT(DAY FROM Reserve_Time) as date,Book_ID,
        DATE_DIFF(today,date) as daysdiff
        FROM main.Reservation
        """
        query_job = client.query(query)
        for row in query_job:
            if cust==name:
                if row['date']==row['today']:
                    tcourt=row['Court_ID']
                    tstatus=row['ApproveStatus']
                    tstime=row['Start_Time']
                    tetime=row['End_Time']
                    tbook_id=row['Book_ID']

                if row['date']==row['today']:
                    t2court=row['Court_ID']
                    t2status=row['ApproveStatus']
                    t2stime=row['Start_Time']
                    t2etime=row['End_Time']
                    t2book_id=row['Book_ID']

                if row['daysdiff']==0:
                    r1court=row['Court_ID']
                    r1status=row['ApproveStatus']
                    r1stime=row['Start_Time']
                    r1etime=row['End_Time']
                    r1book_id=row['Book_ID']

                if row['daysdiff']==0:
                    r2court=row['Court_ID']
                    r2status=row['ApproveStatus']
                    r2stime=row['Start_Time']
                    r2etime=row['End_Time']
                    r2book_id=row['Book_ID']

                if row['daysdiff']>=0:
                    r3court=row['Court_ID']
                    r3status=row['ApproveStatus']
                    r3stime=row['Start_Time']
                    r3etime=row['End_Time']
                    r3book_id=row['Book_ID']

    return render_template("viewReservation.html",name=name,blockNum=blockNum,unitNum=unitNum,username=username,
    cust=cust,tcourt=tcourt,tstatus=tstatus,tstime=tstime,tetime=tetime,tbook_id=tbook_id,t2court=t2court,t2status=t2status,t2stime=t2stime,
    t2etime=t2etime,t2book_id=t2book_id,r1court=r1court,r1status=r1status,r1stime=r1stime,r1etime=r1etime,r1book_id=r1book_id,
    r2court=r2court,r2status=r2status,r2stime=r2stime,r2etime=r2etime,r2book_id=r2book_id,r3court=r3court,r3status=r3status,
    r3stime=r3stime,r3etime=r3etime,r3book_id=r3book_id,)
            

@app.route('/jsontest')
def jsontest():
    if session['loggedIn'] == FALSE or session['UserType']=="ADMIN":
        return redirect('/login')
    
    else:
        name = session['name']
        blockNum = session['BlockNumber']
        unitNum = session['UnitNumber']
        username = session['username']

    client =bigquery.Client()
    cust_table_id='bookit-court-booking-system.main.Reservation'
    query = """
    SELECT Court_ID, Customer_Name, ApproveStatus,Start_Time,Book_ID
    FROM main.Reservation
    """
    court=""
    cust=name
    status=""
    stime=""
    book_id=""
    reservationlist=[]
    query_job = client.query(query)
    for row in query_job:
        cust=row['Customer_Name']
        if cust==name:
            court=row['Court_ID']
            status=row['ApproveStatus']
            stime=row['Start_Time']
            book_ID=row['Book_ID']
            reservationlist.append("Court Number: "+court)
            reservationlist.append(status)
            reservationlist.append(stime)
            reservationlist.append(book_ID)
    return render_template("IndexResident.html",rlist=reservationlist,blockNum=blockNum,unitNum=unitNum,username=username)




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