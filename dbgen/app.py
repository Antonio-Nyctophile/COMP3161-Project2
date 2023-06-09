
from flask import Flask, request, make_response, jsonify,render_template
from flask_login import login_user
import psycopg2 
import os
from passlib.hash import sha256_crypt
#from flask_wtf.csrf import generate_csrf
#from . import db
#from app.forms import LoginForm

app = Flask(__name__)



@app.route('/Lecturers',methods=['GET'])
def lecturers():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor= psql.cursor()
        cursor.execute('SELECT * FROM lecturers')
        lecturerslist=[]
        for lecturerID, firstname,lastname, email, password in cursor:
            lecturers={}
            lecturers ['lecturerID'] = lecturerID
            lecturers ['Name'] = firstname
            lecturers ['Lastname'] = lastname
            lecturers ['Email'] = email
            lecturers ['Password'] = password
            lecturerslist.append(lecturers)
        cursor.close()
        psql.close()
        return make_response(lecturerslist, 200)
    except Exception as e:
        print(e)
        return make_response({'error': 'All lecturers were not found'}, 400)

# Display all students

@app.route('/Students', methods=['GET'])
def students():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        cursor.execute('SELECT * FROM Students')
        studentslist = []
        for userID, firstname, lastname, email, password in cursor:
            students = {}
            students['studentID'] = userID
            students['firstname'] = firstname
            students['lastname'] = lastname
            students['email'] = email
            students['password'] = password
            studentslist.append(students)
        cursor.close()
        psql.close()
        return make_response(studentslist, 200)
    except Exception as e:
        print(e)
        return make_response({'error': 'All students were not found'}, 400)

# Display all courses

@app.route('/Courses', methods=['GET'])
def courses():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        cursor.execute('SELECT * FROM courses')
        courseslist = []
        for ccode, courseName, startdate, enddate in cursor:
            courses = {}
            courses['ccode'] = ccode
            courses['courseName'] = courseName
            courses['startdate'] = startdate
            courses['enddate'] = enddate
            courseslist.append(courses)
        cursor.close()
        psql.close()
        return make_response(courseslist, 200)
    except Exception as e:
        print(e)
        return make_response({'error': 'All courses were not found'}, 400)

# Display all admins

@app.route('/Admin', methods=['GET'])
def admin():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        cursor.execute('SELECT * FROM admins')
        adminlist = []
        for userID, firstname, lastname, password in cursor:
            admin = {}
            admin['adminID'] = userID
            admin['firstname'] = firstname
            admin['lastname'] = lastname
            admin['password'] = password
            adminlist.append(admin)
        cursor.close()
        psql.close()
        return make_response(adminlist, 200)
    except Exception as e:
        print(e)
        return make_response({'error': 'All admins were not found'}, 400)

#register user
@app.route('/RegisterStudent', methods = ['POST'])
def RegisterStudent():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        custom =request.json
        studentID=custom['studentID']
        firstname=custom['firstname']
        lastname=custom['lastname']
        email=custom['email']
        password=custom['password']
        cursor.execute(f"INSERT INTO Students VALUES({studentID},'{firstname}','{lastname}','{email}','{password}')")
        psql.commit()
        cursor.close()
        psql.close()
        return make_response('Student Registered', 200)
    except Exception as e:
        print(e)
        return make_response({'error': 'Student not registered'}, 400)

@app.route('/RegisterLecturer', methods = ['POST'])
def RegisterLecturer():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        custom =request.json
        lecturerID=custom['lecturerID']
        firstname=custom['firstname']
        lastname=custom['lastname']
        email=custom['email']
        password=custom['password']
        cursor.execute(f"INSERT INTO lecturers VALUES({lecturerID},'{firstname}','{lastname}','{email}','{password}')")
        psql.commit()
        cursor.close()
        psql.close()
        return make_response('Lecturer Registered', 200)
    except Exception as e:
        print(e)
        return make_response({'error': 'Lecturer not registered'}, 400)

@app.route('/RegisterAdmin', methods = ['POST'])
def RegisterAdmin():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        custom =request.json
        adminID=custom['adminID']
        firstname=custom['firstname']
        lastname=custom['lastname']
        password=custom['password']
        cursor.execute(f"INSERT INTO admins VALUES({adminID},'{firstname}','{lastname}','{password}')")
        psql.commit()
        cursor.close()
        psql.close()
        return make_response('Admin Registered', 200)
    except Exception as e:
        print(e)
        return make_response({'error': 'Admin not registered'}, 400)
    
#Create Course

@app.route('/CreateCourse', methods = ['POST'])
def CreateCourse():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        custom =request.json
        ccode=custom['ccode']
        courseName=custom['courseName']
        startdate=custom['startdate']
        enddate=custom['enddate']
        cursor.execute(f"INSERT INTO courses VALUES('{ccode}','{courseName}','{startdate}','{enddate}')")
        psql.commit()
        cursor.close()
        psql.close()
        return make_response('Course Added', 200)
    except Exception as e:
        print(e)
        return make_response({'error': 'Course not created'}, 400)


# Login API
IsAdmin = False
@app.route('/UserLogin', methods = ['POST'])
def UserLogin():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        data=request.get_json()

        adminID= data['UserID']
        password= data['password']
        #cursor.execute(f"SELECT * FROM clonevle_db.Students WHERE Students.studentID = {studentID}")
        #print(f"SELECT * FROM admins WHERE adminID = {adminID}")
        cursor.execute(f'SELECT * FROM admins WHERE "adminID" = {adminID}')
        row = cursor.fetchone()
        user = {}
        psql.commit()
        #cursor.close()
        #psql.close()
        
        if row is not None:
            adminID, firstname,lastname,password = row
            user['adminID'] = adminID
            user['firstname']= firstname
            user['lastname']= lastname
           # user['email']=email
            user['password'] = password 
            #return ({"error": "No customer found with id "}, 404)
            if password == data['password']:
              message = "Successfully logged in as: {}".format(user['firstname'])
              IsAdmin = True
              return make_response(message, 200)  
            else:
                return make_response({'error': 'Invalid password. Please try again.'}, 400)
        
        studentID= data['UserID']
        password= data['password']
        #cursor.execute(f"SELECT * FROM clonevle_db.Students WHERE Students.studentID = {studentID}")
        #print(f"SELECT * FROM admins WHERE adminID = {adminID}")
        cursor.execute(f'SELECT * FROM students WHERE "studentID" = {studentID}')
        row = cursor.fetchone()
        user = {}
        psql.commit()
        #cursor.close()
        #psql.close()

        if row is not None:
            print(row)
            studentID,FirstName,LastName,Email,Password = row
            user['studentID'] = studentID
            user['firstname']= FirstName
            user['lastname']= LastName
            user['email']=Email
            user['password'] = Password 
            
            if user['password'] == data['password']:
              message = "Successfully logged in as: {}".format(user['firstname'])
              return make_response(message, 200)  
            else:
                return make_response({'error': 'Invalid password. Please try again.'}, 400)
        

        lecturerID= data['UserID']
        password= data['password']
        #cursor.execute(f"SELECT * FROM clonevle_db.Students WHERE Students.studentID = {studentID}")
        #print(f"SELECT * FROM admins WHERE adminID = {adminID}")
        cursor.execute(f'SELECT * FROM lecturers WHERE "LecturerID" = {lecturerID}')
        row = cursor.fetchone()
        user = {}
        psql.commit()
        cursor.close()
        psql.close()

        if row is not None:
            print(row)
            lecturerID,FirstName,LastName,Email,Password = row
            user['lectuerID'] = lecturerID
            user['firstname']= FirstName
            user['lastname']= LastName
            user['email']=Email
            user['password'] = Password 
            
            if user['password'] == data['password']:
              message = "Successfully logged in as: {}".format(user['firstname'])
              return make_response(message, 200)  
            else:
                return make_response({'error': 'Invalid password. Please try again.'}, 400)
        else:
            return make_response({'error': 'Invalid username. Please try again.'}, 400)
    except Exception as e:
        print(e)
        #print(adminID)
        return make_response({'error': 'User not found'}, 400)




#import random
#Enroll Student 
@app.route('/EnrollStudent',methods = ['POST'])
def EnrollStudent():
    IsAdmin = True
    if not IsAdmin:
        return make_response({'error': 'You are not an ADMIN'}, 400)
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        cursor2 = psql.cursor()
        cursor3 = psql.cursor()
        data=request.get_json()

        UserID= data['UserID']
        courseID= str(data['CourseID'])
        print(courseID)
        
        cursor.execute(f'SELECT * FROM students WHERE "studentID" = {UserID}')
        #cursor.execute(f'SELECT * FROM lecturers')
        row = cursor.fetchone()
        
        cursor.execute(f"SELECT * FROM courses WHERE ccode = '{courseID}'")
        #cursor.execute(f"SELECT * FROM courses")

        row2 = cursor.fetchone()
        cursor.execute(f"SELECT * FROM enroll WHERE userid = {UserID}")
        #cursor.execute(f"SELECT * FROM courses")
        row3 = cursor.fetchall()
        if len(row3) >= 6:
            return make_response({'error': 'Student is already enrolled in max courses'}, 400)
        if courseID in [x[1] for x in row3]:
             return make_response({'error': 'Student is already enrolled in this course'}, 400)
        user = {}
        psql.commit()
        #cursor.close()
        #psql.close()
        # '''Used to enroll all Students and lecturers to courses
        # for x in row:
        #     courses = []
        #     studentID,FirstName,LastName,Email,Password = x
        #     for k in range(random.randint(1,5)):
        #         course_choice = random.choice(row2)[0]
        #         while course_choice in courses:
        #             course_choice = random.choice(row2)[0]
        #         courses.append(course_choice)
        #     for m in courses:
        #         insert_query = "INSERT INTO enrolllecturer (userid, courseid) VALUES (%s, %s)"
        #         values = (studentID, m)
        #         print(values)
        #         cursor3.execute(insert_query, values)
        #         psql.commit()
        # '''

        if row is not None:
            studentID,FirstName,LastName,Email,Password = row
            print("Found Student: ", FirstName," ", LastName)

        print(row2)
        if row2 is not None:
            Ccode,CourseName,StartDate,EndDate = row2
            print("Found Course: ", CourseName)
        
        if (row is not None) and (row2 is not None):
            insert_query = "INSERT INTO enroll (userid, courseid) VALUES (%s, %s)"
            values = (UserID, courseID)
            cursor3.execute(insert_query, values)
            psql.commit()
            cursor.close()
            cursor2.close()
            cursor3.close()
            psql.close()
            message = "Successfully enrolled: {} in {}".format(row[1], row2[1])
            return make_response(message, 200) 
            
        else:
            if row == None and row2 == None:
                errorMessage = "Please Check Student ID and Course ID"
            elif row == None:
                errorMessage = "Please Check Student ID"
            elif row2 == None:
                errorMessage = "Please Check Course ID"
            cursor.close()
            cursor2.close()
            cursor3.close()
            psql.close()

            return make_response({'error': errorMessage}, 400)
    
    except Exception as e:
        print(e)
        #print(adminID)
        return make_response({'error': 'User not found'}, 400)
    
#----------------------------------------------------Course Container---------------------------------------------------------#
#Retrieve Members of a courses container
@app.route('/RetrieveMembers', methods=['GET'])
def RetrieveMembers():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
       

        return {"success":"Calendar Event Created"}
    except Exception as e:
        print(e)
        return {"error":e}    

    
#
#
#Create Calendar Event for course
@app.route('/CalendarEvents', methods=['POST'])
def CalendarEvents():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        data= request.get_json()
        eventid = data['eventid']
        courseid = data['courseid']
        eventname = data['eventname']
        eventdate = data['evendate']
        
        cursor.execute(f"INSERT INTO calendarevent VALUES('{eventid}','{courseid}','{eventname}','{eventdate}');")
        psql.commit()
        cursor.close()
        psql.close()
       
        return {"success":"Calendar Event Created"}
    except Exception as e:
        print(e)
        return {"error":'Failed to create Calendar event'}    


# 
# Retrieve Calendar Event
@app.route('/GetCalendarEvents/<courseid>',methods=['GET'])
def GetCalendarEvents(courseid):
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        cursor.execute(f"SELECT * FROM calendarevent WHERE Courseid='{courseid}'")
        events=[]
        for eventid, courseid,eventname,eventdate in cursor:
            data = {}
            data['eventid'] = eventid
            data['courseid'] = courseid
            data['eventname'] = eventname
            data['eventdate'] = eventdate
            events.append(data)
        cursor.close()
        psql.close()
        return make_response(events, 200)
    except Exception as e:
        print(e)
        return {"error":'Failed to retrieve Calendar events'}   
# 
# Create Forum for course
@app.route('/CreateForum', methods=['POST'])
def CreateForum():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        data = request.get_json()
        forumid= data['forumid']
        courseid= data['courseid']
        discussiontopic= data['discussiontopic']
        datestarted=data['datestarted']
        active=data['active']
        cursor.execute(f"INSERT INTO forums VALUES('{forumid}','{courseid}','{discussiontopic}','{datestarted}','{active}')")
        psql.commit()
        cursor.close()
        psql.close()
        return make_response({"success" : "The forum has been added"}, 201)
    except Exception as e:
        print(e)
        return {"error":'Failed to create forum '}  




# 
# Retrieve Forum for course
@app.route('/GetCourseForum/<courseid>',methods=['GET'])
def GetCourseForum(courseid):
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        cursor.execute(f"SELECT active, forumid, courseid, discussiontopic, datestarted FROM forums WHERE courseid ='{courseid}'")
        forum = []
        for active, forumid, courseid, discussiontopic, datestarted in cursor:
            forumdict = {}
            forumdict['forumid'] = forumid
            forumdict['courseid'] = courseid
            forumdict['discussiontopic'] = discussiontopic
            forumdict['datestarted'] = datestarted
            forumdict['active'] = active
            forum.append(forumdict)

        cursor.close
        psql.close
        return make_response(forum, 200)
    except Exception as e:
        print(e)
        return {"error":'Failed to retrieve forums'}  


#Cretae Discussion Thread
@app.route("/CreateDiscussionThread", methods = ['POST'])
def CreateDiscussionThread():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        data = request.get_json()
        threadid = data['threadid']  
        forumid = data['forumid']
        threadname = data['threadname']
        threadreply = data['threadreply']
        replyno = data['replyno']
        replycontent = data['replycontent']
        cursor.execute(f"INSERT INTO threads VALUES('{threadid}','{forumid}','{threadname}','{threadreply}',{replyno},'{replycontent}');") 
        psql.commit()
        cursor.close()
        psql.close()
        return make_response({"success" : "The thread has been added"}, 201)
    except Exception as e:
        print(e)
        return {"error":'Failed to create Thread '}  


# 
# Retrieve discussion thread for forum
@app.route("/GetDiscussionThread/<forumid>", methods = ['GET'])
def GetDiscussionThread(forumid):
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        cursor.execute(f"SELECT * FROM threads WHERE forumid = '{forumid}'")
        threads = []
        for  threadid, forumid, threadname, threadreply, replyno, replycontent in cursor:
            discuss_thread = {}
            discuss_thread['threadid'] = threadid
            discuss_thread['forumid'] = forumid
            discuss_thread['threadname'] = threadname
            discuss_thread['threadreply'] = threadreply
            discuss_thread['replyno'] = replyno
            discuss_thread['replycontent'] = replycontent
            threads.append(discuss_thread)
        cursor.close()
        psql.close()
        return make_response(threads, 200)
    except Exception as e:
        print(e)
        return {"error":'Failed to retrieve threads'} 

# 
# 
# Create Assignment
# 
#
# 
# Add grade for assignment
# 
# 
#  #

#----------------------------------------------------REPORTS---------------------------------------------------------#

# Returns Courses with 50 or more students 
@app.route('/CourseReport', methods=['GET'])
def CourseReport():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        #data=request.get_json()
        #cursor.execute('SELECT courseid COUNT(userid) FROM enroll JOIN enroll ON courses.ccode HAVING COUNT(userid) >=50')
        sql='SELECT c."courseName", COUNT(DISTINCT e.userid) AS enrolled FROM enroll e JOIN courses c ON e."courseid" = c."ccode" GROUP BY c."ccode", c."courseName" HAVING COUNT(DISTINCT e.userid) >= 50;'
        cursor.execute(sql)
        courselist=[]
        for courseName, studentCount in cursor:
            course={}
            course["courseName"]= courseName
            course["studentCount"]=studentCount
            courselist.append(course)
        cursor.close()
        psql.close()
        return make_response({'courselist': courselist}, 200)
        
    except Exception as e:
        print(e)
        return make_response({'error':'An error has occured, could not return all courses that  have  50 or more students'}, 400)




# All lecturers that teaches 3 or more courses will be
@app.route('/LecturerReport', methods=['GET'])
def LecturerReport():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        sql='SELECT l.firstname, l.lastname, COUNT(DISTINCT e.courseid) AS num_courses FROM enrolllecturer e JOIN lecturers l ON e.userid = l."lecturerID" GROUP BY l."lecturerID", l.firstname, l.lastname HAVING COUNT(DISTINCT e.courseid) >= 3;'
        cursor.execute(sql)        
        lecturerslist=[]
        for firstname, lastname, num_courses in cursor:
            lecturer={}
            lecturer["firstname"]= firstname
            lecturer["lastname"]= lastname
            lecturer["num_courses"]= num_courses
            lecturerslist.append(lecturer)
        cursor.close()
        psql.close()

        return make_response({'lecturerlist': lecturerslist}, 200)
    except Exception as e:
        print(e)
        return make_response({'error':'An error has occured, could not return the lectures that teach 3 or more courses'}, 400)






# 
# 
# 


# All students that do 5 or more courses
@app.route('/StudentReport', methods=['GET'])
def StudentReport():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        sql='SELECT s."studentID",s.firstname,s.lastname, COUNT(DISTINCT e.courseid) AS num_courses FROM enroll e JOIN students s ON e.userid = s."studentID" GROUP BY s."studentID", s."firstname", s."lastname" HAVING COUNT(DISTINCT e.courseid) >= 5;'
        cursor.execute(sql)
        studentlist=[]
        for studentID,firstname,lastname,num_course in cursor:
            student={}
            student["studentID"] = studentID
            student["firstname"]= firstname
            student["lastname"] = lastname
            student["num_course"] = num_course

            studentlist.append(student)

        cursor.close()
        psql.close()
        return make_response({'studentlist': studentlist}, 200)
    except Exception as e:
        print(e)
        return make_response({'error':'An error has occured, could not return allstudents that do 5 or more courses'},400)
# 


# Top 10 most enrolled course
@app.route('/MostEnrolledCourseReport', methods=['GET'])
def MostEnrolledCourseReport():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        sql='SELECT c."ccode",c."courseName", COUNT(DISTINCT e.userid) AS enrolled FROM enroll e JOIN courses c ON e.courseid = c."ccode" GROUP BY c."ccode", c."courseName" ORDER BY enrolled DESC LIMIT 10;'
        cursor.execute(sql)
        courselist=[]
        for ccode,courseName, enrolled in cursor:
            course = {}
            course["ccode"] = ccode
            course["courseName"] = courseName
            course["enrolled"] = enrolled
            
            courselist.append(course)
        cursor.close()
        psql.close()        
        return make_response({'courselist': courselist}, 200)
    except Exception as e:
        print(e)
        return make_response({'error':'An error has occured, could not return the top 10 most enrolled courses'}, 400)
# 



# Top 10 students with highest overall averages


# Total number of students
@app.route("/TotalStudents",methods=['GET'])
def TotalStudents():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        sql='SELECT COUNT(*) FROM Students;'
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        cursor.close()
        psql.close()        
        message = "There are {} students in the database.".format(result)
        return make_response(message, 200)
    except Exception as e:
        print(e)
        return make_response({'error':'An error has occured, could not return the total number of students in the database'}, 400)


# Total number of lecturers
@app.route('/TotalLecturers', methods=['GET'])
def TotalLecturers():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        sql='SELECT COUNT(*) FROM lecturers;'
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        cursor.close()
        psql.close()        
        message = "There are {} lecturers in the database.".format(result)
        return make_response(message, 200)
    except Exception as e:
        print(e)
        return make_response({'error':'An error has occured, could not return the number of lecturers in the database'}, 400)




#Total number of courses
@app.route('/TotalCourses', methods=['GET'])
def TotalCourses():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        sql='SELECT COUNT(*) FROM courses;'
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        cursor.close()
        psql.close()        
        message = "There are {} courses in the database.".format(result)
        return make_response(message, 200)
    except Exception as e:
        print(e)
        return make_response({'error':'An error has occured, could not return the number of courses in the database'}, 400)

# 
# 
# #
