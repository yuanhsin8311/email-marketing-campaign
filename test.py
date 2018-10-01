from flask import Flask
from flask import request
from flask import render_template
#import cgi, cgitb
import sys
import os
import MySQLdb
import time
import datetime

class BarChartEntry:
    def __init__(self):
        self.name_list = []
        self.value_list_text = ''
        self.play_name_list = []
        self.play_value_list_text = ''

app = Flask(__name__)

@app.route('/lookup.html')
def hello():
    #return 'Hello, World!'
    #reload(sys)
    #sys.setdefaultencoding('utf-8')


    #cgitb.enable()
    #form = cgi.FieldStorage()

    # Get data from fields
    #Name = form.getvalue('Name')
    Name = request.args.get("Name")
    #request.form.get('Name')
    #request.form['Name']
    #print(Name)

    date_time = datetime.datetime.now()
    now_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
    date = date_time.date()
    cur_time = date_time.time()

    db = MySQLdb.connect(host="localhost", user="root", passwd="abcd0101", db="loandb")
    cur = db.cursor()
    mysql_cmd = 'select * from click_table where Name="' + Name + '";'
    cur.execute(mysql_cmd)
    entry_list = cur.fetchone()

    if entry_list is None:
        mysql_cmd = 'insert into `click_table` (`pid`, `Name`, `Date_sorted`) VALUES (NULL, "' + Name  + '", "' + now_time  + '");'
        cur.execute(mysql_cmd)
        db.commit()
    else:
        mysql_cmd = 'UPDATE `click_table` SET `Date_sorted` = "' + now_time + '" WHERE Name = "' + Name + '";'
        cur.execute(mysql_cmd)
        db.commit()
    html_body = '\n<form action="submit.html" method="post">\n <input type="hidden" name="Name" value="' + Name + '"><br>\n  <button type="submit">Submit</button><br>\n</form>\n\n<p\><strong>User: ' + Name +' clicked at ' + now_time + '</strong></p>\n'

    html_cont = '<html>\n<head>\n<title>Hello - Second CGI Program</title>\n</head>\n<body>' + html_body + '</body>\n</html>'

    return html_cont


@app.route('/submit.html', methods=['GET', 'POST'])
def submit():
    #print('submit')

    Name = request.form.get('Name')

    date_time = datetime.datetime.now()
    now_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
    date = date_time.date()
    cur_time = date_time.time()

    db = MySQLdb.connect(host="localhost", user="root", passwd="abcd0101", db="loandb")
    cur = db.cursor()
    mysql_cmd = 'select * from submit_table where Name="' + Name + '";'
    cur.execute(mysql_cmd)
    entry_list = cur.fetchone()

    if entry_list is None:
        mysql_cmd = 'insert into `submit_table` (`pid`, `Name`, `Date_sorted`) VALUES (NULL, "' + Name  + '", "' + now_time  + '");'
        cur.execute(mysql_cmd)
        db.commit()
    else:
        mysql_cmd = 'UPDATE `submit_table` SET `Date_sorted` = "' + now_time + '" WHERE Name = "' + Name + '";'
        cur.execute(mysql_cmd)
        db.commit()

    html_body = '\n<p\><strong>User: ' + Name + ' submitted</strong></p>\n'
    html_cont = '<html>\n<head>\n<title>Hello - Second CGI Program</title>\n</head>\n<body>' + html_body + '</body>\n</html>'

    return html_cont

@app.route('/barchart')
def barchart():
    #mysql_cmd = 'select * from submit_table where Name="' + Name + '";'

    mybar = BarChartEntry()

    db = MySQLdb.connect(host="localhost", user="root", passwd="abcd0101", db="loandb")
    cur = db.cursor()
    mysql_cmd = 'SELECT CASE WHEN WEEKDAY(DATE(C.Date_sorted)) = 5 THEN "Sat" WHEN WEEKDAY(DATE(C.Date_sorted)) = 4 THEN "Fri" WHEN WEEKDAY(DATE(C.Date_sorted)) = 3 THEN "Thur" WHEN WEEKDAY(DATE(C.Date_sorted)) = 2 THEN "Wed" WHEN WEEKDAY(DATE(C.Date_sorted)) = 1 THEN "Tue" WHEN WEEKDAY(DATE(C.Date_sorted)) = 0 THEN "Mon" WHEN WEEKDAY(DATE(C.Date_sorted)) = 6 THEN "Sun" END AS "Weekday", COUNT(DISTINCT C.PID) AS "Number of Click without Conversion" FROM CLICK_TABLE C LEFT JOIN SUBMIT_TABLE S ON C.PID = S.PID WHERE S.PID IS NULL group by CASE WHEN WEEKDAY(DATE(C.Date_sorted)) = 5 THEN "Sat" WHEN WEEKDAY(DATE(C.Date_sorted)) = 4 THEN "Fri" WHEN WEEKDAY(DATE(C.Date_sorted)) = 3 THEN "Thur" WHEN WEEKDAY(DATE(C.Date_sorted)) = 2 THEN "Wed" WHEN WEEKDAY(DATE(C.Date_sorted)) = 1 THEN "Tue" WHEN WEEKDAY(DATE(C.Date_sorted)) = 0 THEN "Mon" WHEN WEEKDAY(DATE(C.Date_sorted)) = 6 THEN "Sun" END;'

    print(mysql_cmd)

    cur.execute(mysql_cmd)
    rows = cur.fetchall()
    if len(rows) == 0:
        print('no data')
    else:
        for each_row in rows:
            print(each_row[0], each_row[1])
            if mybar.value_list_text == '':
                mybar.value_list_text = each_row[1]
            else:
                mybar.value_list_text = mybar.value_list_text + ', ' + each_row[1]
            mybar.name_list.append(each_row[0])

    result_entry = mybar
    return render_template('test3.html', result_entry = result_entry)
