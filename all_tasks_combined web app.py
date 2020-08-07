import pymysql
import os
import datetime
from datetime import datetime, timedelta
import time
from flask import Flask, make_response, request, send_file
import io
import csv
import ast
import sqlite3
import pandas as pd5
import requests

from werkzeug import secure_filename

app = Flask(__name__)

@app.route('/')
def form():
    return """
        <html>
            <body>
            Click on the button corresponding to the task to be performed.<br>
            <form>
            <input type=button onClick="location.href='../locations_from_coordinates'" value="Locations finder">
            <input type=button onClick="location.href='../stoppage_time_calculator'" value="Stoppage Time Calculator">
            </form>
            </body>
        </html>
    """



@app.route('/stoppage_time_calculator')
def stoppage_time_calculator():
    return """
        <html>
            <body>
                <h1>Program to find the stoppage times from entered table name inside the entered database name and then adding a result to the table "trip_stoppage" inside the passed database.</h1>
                <form action="/stoppage_time" method="post" enctype="multipart/form-data">
                    Host: <input name="host_1"><br><br>
                    User: <input name="user_1"><br><br>
                    Password: <input type="password" name="password_1"><br><br>
                    Database: <input name="database_1"><br><br>
                    Table containing service ids: <input name="tbname_sysid"><br><br>
                    Table containing data of service ids in above table: <input name="tbname_data"><br><br>
                    <input type="submit">
                </form>
            </body>
        </html>
    """

@app.route('/stoppage_time', methods=["GET", "POST"])
def stoppage_time():
    ho_st=request.form['host_1']
    user=request.form['user_1']
    password=request.form['password_1']
    database=request.form['database_1']
    service_id=request.form['tbname_sysid']
    data_table=request.form['tbname_data']
    mydb = pymysql.connect(host=str(ho_st), user=str(user),passwd=str(password),database=str(database))
    cur = mydb.cursor()
    create="CREATE TABLE IF NOT EXISTS "+database+".trip_stoppage(vehicle_index INT, sys_service_id BIGINT, start_latitude FLOAT, start_longitude FLOAT, stoppage_time BIGINT)"
    cur.execute(create)


    task=sql = "INSERT INTO matrix.trip_stoppage(vehicle_index,sys_service_id,start_latitude,start_longitude,stoppage_time) VALUES (%s,%s,%s,%s,%s)"
    fetch_serviceids="SELECT * FROM "+database+"."+service_id
    cur.execute(fetch_serviceids)
    y=cur.fetchall()

    r=[]
    for i in range(100):
        r.append(y[i])

    for loop in y:
        fetch_count="SELECT COUNT(*) FROM "+database+"."+data_table+" WHERE sys_service_id=%s ORDER BY sys_service_id ASC"
        cur.execute(str(fetch_count)%(loop[0]))
        x=cur.fetchone()    
        a=x[0]
        vehicledata=[]
        fetch_data="SELECT * FROM "+database+"."+data_table+" WHERE sys_service_id=%s ORDER BY Start_time ASC"
        cur.execute(str(fetch_data)%(loop[0]))
        for j in range(a):
            x=cur.fetchone()
            vehicledata.append(x)

        i=1
        data_list=[]
        while i<a:
            data=vehicledata[i]
            data_prev=vehicledata[i-1]
            if data[2]+timedelta(hours=36)<data[15]:
                i+=1
                continue
            else:
                start  = data[2]
                previousend  = data_prev[6]
                stoppage_time=start-previousend
                stoppage_time = (stoppage_time.days * 24 * 60)+(stoppage_time.seconds/60)
                data_list.append(i)
                data_list.append(data[1])
                data_list.append(data[4])
                data_list.append(data[5])
                data_list.append(stoppage_time)
                cur.execute(task,data_list)
                data_list=[]
                i+=1
                continue
        mydb.commit()
    return """<html>
                <body>
                    <h1>Program completed without any errors</h1><br>
                    please check the entered database's trip_stoppage table to view result.
                    <form action="/"><input type=submit value="Click here to go the home page"></form>
                </body>
              </html>"""

@app.route('/locations_from_coordinates')
def locations_from_coordinates():
    return """
        <html>
            <body>
                <h1>Program to find the locations to 1791 correspondiong latitudes and longitudes.</h1>
                Please note the following before executing the program:<ul><li>The data insid ethe file should be in the following format: gps_latitude, gps_longitude</li>
    <li>In case more than 1791 rows of data are present in the uploaded file, the program shall consider first 1791 rows only and the rest shall not be processed.</li>
<li>This program can be used only once in a day</li>
                <form action="/key_assigning" method="post" enctype="multipart/form-data">
                    <input type="file" name="data_file_1" accept=".csv">
                    <input type="submit">
                </form>
            </body>
        </html>
    """
@app.route('/key_assigning', methods=["POST"])
def key_asigning():
    f=request.files['data_file_1']

    if not f:
        return """No file uploaded<br> 
                    <form action="/locations_from_coordinates"> 
                        <input type="submit" value="Retry">
                    </form>"""
    else:
        
        database=sqlite3.connect("C:\SQLiteStudio\data.db")
        cur=database.cursor()
        task1="""CREATE TABLE IF NOT EXISTS coordinates_table (
               sr_no int,
               gps_latitude DOUBLE PRECISION ,
               gps_longitude DOUBLE PRECISION,
               license_key_allotted VARCHAR
           );"""
        task2="""INSERT INTO coordinates_table (sr_no,gps_latitude,gps_longitude,license_key_allotted) VALUES (?,?,?,?)"""

        cur.execute(task1)

        out=pd.read_csv(f)
        x=out
        if len(out)>1791:
            data_count=1791
        elif len(out)<199:
            data_count=len(out)
        elif len(out)<398:
            data_count=len(out)
        elif len(out)<597:
            data_count=len(out)
        elif len(out)<796:
            data_count=len(out)
        elif len(out)<995:
            data_count=len(out)
        elif len(out)<1194:
            data_count=len(out)
        elif len(out)<1393:
            data_count=len(out)
        elif len(out)<1592:
            data_count=len(out)
        elif len(out)<1791:
            data_count=len(out)

            
        row=1
        x=[]
        while row<=199 and row <data_count :
                x=[row,out.iloc[row,0],out.iloc[row,1],"key_1"]
                cur.execute(task2,x)
                database.commit()
                row+=1

        a=row+199

        while row<a and row<data_count:
                x=[row,out.iloc[row,0],out.iloc[row,1],"key_2"]
                cur.execute(task2,x)
                database.commit()
                row+=1

        a=row+199

        while row<a and row<data_count:
                x=[row,out.iloc[row,0],out.iloc[row,1],"key_3"]
                cur.execute(task2,x)
                database.commit()
                row+=1

        a=row+199

        while row<a and row<data_count:
                x=[row,out.iloc[row,0],out.iloc[row,1],"key_4"]
                cur.execute(task2,x)
                database.commit()
                row+=1

        a=row+199

        while row<a and row<data_count:
                x=[row,out.iloc[row,0],out.iloc[row,1],"key_5"]
                cur.execute(task2,x)
                database.commit()
                row+=1

        a=row+199

        while row<a and row<data_count:
                x=[row,out.iloc[row,0],out.iloc[row,1],"key_6"]
                cur.execute(task2,x)
                database.commit()
                row+=1

        a=row+199

        while row<a and row<data_count:
                x=[row,out.iloc[row,0],out.iloc[row,1],"key_7"]
                cur.execute(task2,x)
                database.commit()
                row+=1

        a=row+199

        while row<a and row<data_count:
                x=[row,out.iloc[row,0],out.iloc[row,1],"key_8"]
                cur.execute(task2,x)
                database.commit()
                row+=1

        a=row+199

        while row<data_count:
                x=[row,out.iloc[row,0],out.iloc[row,1],"key_9"]
                cur.execute(task2,x)
                database.commit()
                row+=1


        if len(out)>1791:
            out.drop(out.head(1791).index, inplace=True)
            out.to_csv(f, index=False)



        with open('location_file.csv', mode='a', newline='') as location_file:
            location_writer = csv.writer(location_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            cur.execute("""SELECT * FROM coordinates_table""")
            coordinates=cur.fetchall()


            for i in range(len(coordinates)):
                key_check=coordinates[i]
                if key_check[3]=="key_1":
                    a=key_check
                    url = "https://apis.mapmyindia.com/advancedmaps/v1/kgpxta9p6y6zjdxnxh6qcwnke19bx8bt/rev_geocode"
                    querystring = {"lat":a[1],"lng":a[2]}
                    headers = {
                     'cache-control': "no-cache",
                     'postman-token': "e511fc69-0887-9eb7-8865-08b3afd25902"
                         }
                    response = requests.request("POST", url, headers=headers, params=querystring)
                    res=response.text
                    res=ast.literal_eval(res)
                    res=res["results"]
                    res=res[0]
                    res=res["formatted_address"]
                    location_writer.writerow([a[1],a[2],res])


                if key_check[3]=="key_2":
                    a=key_check
                    url = "https://apis.mapmyindia.com/advancedmaps/v1/zo3mglknal8p14y8jnq7m7pyy2vpxaha/rev_geocode"
                    querystring = {"lat":a[1],"lng":a[2]}
                    headers = {
                     'cache-control': "no-cache",
                     'postman-token': "e511fc69-0887-9eb7-8865-08b3afd25902"
                         }
                    response = requests.request("POST", url, headers=headers, params=querystring)
                    res=response.text
                    res=ast.literal_eval(res)
                    res=res["results"]
                    res=res[0]
                    res=res["formatted_address"]
                    
                    location_writer.writerow([a[1],a[2],res])


                if key_check[3]=="key_3":
                    
                    a=key_check
                    
                    
                    url = "https://apis.mapmyindia.com/advancedmaps/v1/aqfz9dx2xbv358yt3v8aia9cfhw97mxg/rev_geocode"
                    querystring = {"lat":a[1],"lng":a[2]}
                    headers = {
                     'cache-control': "no-cache",
                     'postman-token': "e511fc69-0887-9eb7-8865-08b3afd25902"
                         }
                    response = requests.request("POST", url, headers=headers, params=querystring)
                    res=response.text
                    res=ast.literal_eval(res)
                    res=res["results"]
                    res=res[0]
                    res=res["formatted_address"]
                    
                    location_writer.writerow([a[1],a[2],res])
            
            
                if key_check[3]=="key_4":
                    
                    a=key_check
                    
                    
                    url = "https://apis.mapmyindia.com/advancedmaps/v1/l9gtdjyqz4hy2plrxxmkrkvz46ztarg7/rev_geocode"
                    querystring = {"lat":a[1],"lng":a[2]}
                    headers = {
                     'cache-control': "no-cache",
                     'postman-token': "e511fc69-0887-9eb7-8865-08b3afd25902"
                         }
                    response = requests.request("POST", url, headers=headers, params=querystring)
                    res=response.text
                    res=ast.literal_eval(res)
                    res=res["results"]
                    res=res[0]
                    res=res["formatted_address"]
                    
                    location_writer.writerow([a[1],a[2],res])


                if key_check[3]=="key_5":
                    
                    a=key_check
                    
                    
                    url = "https://apis.mapmyindia.com/advancedmaps/v1/hxjlievzoxm8pdqr2vt27fb28tm553ox/rev_geocode"
                    querystring = {"lat":a[1],"lng":a[2]}
                    headers = {
                     'cache-control': "no-cache",
                     'postman-token': "e511fc69-0887-9eb7-8865-08b3afd25902"
                         }
                    response = requests.request("POST", url, headers=headers, params=querystring)
                    res=response.text
                    res=ast.literal_eval(res)
                    res=res["results"]
                    res=res[0]
                    res=res["formatted_address"]
                    
                    location_writer.writerow([a[1],a[2],res])
            

                if key_check[3]=="key_6":
                    
                    a=key_check
                    
                    
                    url = "https://apis.mapmyindia.com/advancedmaps/v1/lixj3orrkt79psvne2wbm5bymq4j8nu5/rev_geocode"
                    querystring = {"lat":a[1],"lng":a[2]}
                    headers = {
                     'cache-control': "no-cache",
                     'postman-token': "e511fc69-0887-9eb7-8865-08b3afd25902"
                         }
                    response = requests.request("POST", url, headers=headers, params=querystring)
                    res=response.text
                    res=ast.literal_eval(res)
                    res=res["results"]
                    res=res[0]
                    res=res["formatted_address"]
                    
                    location_writer.writerow([a[1],a[2],res])


                if key_check[3]=="key_7":
                    
                    a=key_check
                    
                    
                    url = "https://apis.mapmyindia.com/advancedmaps/v1/wjby24gltm99nrm3eq8ohgzxzjeafwmo/rev_geocode"
                    querystring = {"lat":a[1],"lng":a[2]}
                    headers = {
                     'cache-control': "no-cache",
                     'postman-token': "e511fc69-0887-9eb7-8865-08b3afd25902"
                         }
                    response = requests.request("POST", url, headers=headers, params=querystring)
                    res=response.text
                    res=ast.literal_eval(res)
                    res=res["results"]
                    res=res[0]
                    res=res["formatted_address"]
                    
                    location_writer.writerow([a[1],a[2],res])


                if key_check[3]=="key_8":
                    
                    a=key_check
                    
                    
                    url = "https://apis.mapmyindia.com/advancedmaps/v1/zpuh5cx385m29b1mlgrxwrg3w7n6d1vo/rev_geocode"
                    querystring = {"lat":a[1],"lng":a[2]}
                    headers = {
                     'cache-control': "no-cache",
                     'postman-token': "e511fc69-0887-9eb7-8865-08b3afd25902"
                         }
                    response = requests.request("POST", url, headers=headers, params=querystring)
                    res=response.text
                    res=ast.literal_eval(res)
                    res=res["results"]
                    res=res[0]
                    res=res["formatted_address"]
                    
                    location_writer.writerow([a[1],a[2],res])


                if key_check[3]=="key_9":
                    a=key_check
                    url = "https://apis.mapmyindia.com/advancedmaps/v1/i1wsduwd81xnoi6o4awmjdvnn9cq8pop/rev_geocode"
                    querystring = {"lat":a[1],"lng":a[2]}
                    headers = {
                     'cache-control': "no-cache",
                     'postman-token': "e511fc69-0887-9eb7-8865-08b3afd25902"
                         }
                    response = requests.request("POST", url, headers=headers, params=querystring)
                    res=response.text
                    res=ast.literal_eval(res)
                    res=res["results"]
                    res=res[0]
                    res=res["formatted_address"]
                    location_writer.writerow([a[1],a[2],res])

        cur.execute("""DROP TABLE coordinates_table;""")
        database.close()
        res=make_response(send_file("C:\\Users\\Jay Paliwal\\Desktop\\Internship\\location_file.csv"))
        res.headers.set('Content-Disposition', 'attachment', filename='location_file.csv')
        return res
if __name__ == "__main__":
    app.run(debug=True)
