from google.cloud import bigquery
from datetime import datetime
from flask import request,session
from google.cloud.bigquery.job.query import QueryJob
#set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\User\Downloads\hlb-carbon-footprint-ps6\turing-goods-324908-d52fcabab09f.json


def GetUserName():
    username=request.form['username']
    return username

    





#def getAvgCFB001():
    # Construct a BigQuery client object.
#    client = bigquery.Client()

#    query = """
#        SELECT AVG(totalCarbonFootprint) AS avg_CF
#        FROM `hlbcyhi2021-2.main.b001-performance-updated`
#    """
#    query_job = client.query(query)  # Make an API request.

 #   print("The query data:")
  #  # print(query_job[0]["avg_CF"])
  #  for row in query_job:
  #      # print(type(query_job))
  #      # Row values can be accessed by field name or index.
  #      # print("name={}, count={}".format(row[0], row["total_people"]))
  #      return(row["avg_CF"])
        
    # return query_job[0]["avg_CF"]
    
    
#def getBranchCount():
#    client = bigquery.Client()
    
#    query = """
#        SELECT COUNT(BranchID) as branchCount
#        FROM `hlbcyhi2021-2.main.main-table`
#        WHERE EXTRACT(Month FROM Date) = 1
#    """
#    query_job = client.query(query)
    
    # print("The query data:")
#    for row in query_job:
#        return(row["branchCount"])
    


#def getCurrentDay():
#    day = datetime.now().strftime("%d")
#    return day


#def getCurrentMonth():
#    month = datetime.now().strftime('%B')
#    return month

#def getCurrentYear():
#    year = datetime.now().strftime('%Y')
#    return year

#def getStaffCount():
#    client = bigquery.Client()
    
#    query="""
#        SELECT SUM(staffCount) as staffCount
#        FROM `hlbcyhi2021-2.main.main-table`
#        WHERE EXTRACT(Month FROM Date) = EXTRACT(Month FROM CURRENT_DATE())
#    """    
#    query_job = client.query(query)
    # print("The query data:")
#    for row in query_job:
#        return(row["staffCount"])    
    
    
#def getTotalCFcurrMonth():
#    client = bigquery.Client()
    
#    query="""
#        SELECT SUM(totalCF_kgCO2) AS totalCF
#        FROM `hlbcyhi2021-2.main.main-table`
#        WHERE EXTRACT(Month FROM Date) = EXTRACT(Month FROM CURRENT_DATE())
#    """
#    query_job = client.query(query)
#    # print("The query data:")
#    for row in query_job:
#        return(row["totalCF"])
    
    
#def getCulmulativeCFcurrMonth():
#    client = bigquery.Client()
    
#    query="""
#        SELECT SUM(totalCF_kgCO2) as culTotal
#        FROM `hlbcyhi2021-2.main.main-table`
#        WHERE EXTRACT(Month FROM Date) <= EXTRACT(Month FROM CURRENT_DATE())
#    """
    
#    query_job = client.query(query)
    # print("The query data:")
#    for row in query_job:
#        return(row["culTotal"])
    
    
def getTotalRecycledKG():
   client = bigquery.Client()
    
   query="""
       SELECT SUM(totalKG) AS totalKGrecycled
       FROM `hlbcyhi2021-2.main.hlb-recycle`
       WHERE EXTRACT(Month FROM Date) = EXTRACT(Month FROM CURRENT_DATE())
   """
    
   query_job = client.query(query)
   # print("The query data:")
   for row in query_job:
       return(row["totalKGrecycled"])    
    
    
    
#def getTotalTreesPlanted():
#    client = bigquery.Client()
    
#    query="""
#        SELECT SUM(treesPlanted) AS totalTreesPlanted
#        FROM `hlbcyhi2021-2.main.hlb-recycle`
#        WHERE EXTRACT(Month FROM Date) = EXTRACT(Month FROM CURRENT_DATE())
#    """
    
#   query_job = client.query(query)
#    # print("The query data:")
#    for row in query_job:
#        return(row["totalTreesPlanted"])  
    
    
    
#def getTotalEnergySaved():
#    client = bigquery.Client()
    
#    query="""
#        SELECT SUM(energySavedkwh) AS totalEnergySaved
#        FROM `hlbcyhi2021-2.main.hlb-recycle`
#        WHERE EXTRACT(Month FROM Date) = EXTRACT(Month FROM CURRENT_DATE())
#    """
    
#    query_job = client.query(query)
    # print("The query data:")
#    for row in query_job:
#        return(row["totalEnergySaved"])  


def testingInsert():
    
    oldusername = "clcheong"
    username = "cl"
    usertype = "USER"
    name = "Chien Li"
    email = "cl@gmail.com"
    phoneNum = "012"
    blockNum = "AA"
    unitNum = "00-01"
    
    client = bigquery.Client()
    
    query = """
        UPDATE `bookit-court-booking-system.main.Customer`
        SET username='""" + username + """', name='""" + name + """', email='"""+ email + """', PhoneNumber='""" + phoneNum + """',BlockNumber='""" + blockNum + """',UnitNumber='""" + unitNum + """'
        WHERE username='""" + oldusername + """'
    """
    query_job = client.query(query)
    
    query_job.result()

    print(f"DML query modified {query_job.num_dml_affected_rows} rows.")
    return query_job.num_dml_affected_rows

    
# if __name__ == "__main__":
#     print(testingInsert())