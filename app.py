# Library from Flask

from google.cloud import bigquery
from google.cloud.bigquery import client, dbapi, query
from bigquery import GetUserName
from flask import * #Flask, render_template, request, redirect, session, flash, url_for
from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from tkinter import *  
  
from tkinter import messagebox  
  

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
        return render_template("indexResident.html",username=username,name=name, blockNum=blockNum,unitNum=unitNum)

@app.route('/IndexAdmin')
def IndexAdmin():
    
    if session['loggedIn'] == FALSE or session['UserType']=="USER":
        return redirect('/login')
    
    else:    
        client = bigquery.Client()

        query="""
           SELECT *
           FROM `bookit-court-booking-system-1.main.Reservation`
        """

        query_job = client.query(query)
        # print("The query data:")
        name = session['name']
        username = session['username']
        return render_template('IndexAdmin.html',name=name, username=username, bookingData=query_job)

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
    if Booking_Status=="Disapprove":
        query="""
        UPDATE `bookit-court-booking-system-1.main.Reservation` 
        SET Approve_Status = FALSE
        WHERE Book_ID = {}
        """.format('\"'+Booking_ID+'\"')
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

    return '', 400
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

        return render_template('court-availability.html',Court1Open=court1Open,Court2Open=court2Open,Court3Open=court3Open,Court4Open=court4Open);


#Render template for Manage facility 
@app.route('/ManageFacilityAvailability')
def ManageFacility():
    if session['loggedIn'] == FALSE or session['UserType']=="USER":
        return redirect('/login')
    else:
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

        return render_template('ManageFacility.html',Court1_Start_Time=Court1_Start_Time,Court1_End_Time=Court1_End_Time,Court2_Start_Time=Court2_Start_Time,Court2_End_Time=Court2_End_Time,Court3_Start_Time=Court3_Start_Time,Court3_End_Time=Court3_End_Time,Court4_Start_Time=Court4_Start_Time,Court4_End_Time=Court4_End_Time,AllCourt_Start_Time=AllCourt_Start_Time,AllCourt_End_Time=AllCourt_End_Time)

@app.route('/Feedback')
def Feedback():
    if session['loggedIn'] == FALSE or session['UserType']=="USER":
        return redirect('/login')
    else:
        return render_template('Feedback.html')

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

if __name__ == "__main__":
    app.run()