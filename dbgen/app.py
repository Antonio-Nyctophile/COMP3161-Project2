
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
'''
@app.route('/UserLogin', methods = ['POST'])
def UserLogin():
    try:
        psql = psycopg2.connect(database='clonevle_db', user='postgres', password='3072001', host='localhost', port='5432' )
        cursor = psql.cursor()
        data=request.get_json()

        adminID= data['adminID']
        password= data['password']
        #cursor.execute(f"SELECT * FROM clonevle_db.Students WHERE Students.studentID = {studentID}")
        #print(f"SELECT * FROM admins WHERE adminID = {adminID}")
        cursor.execute(f'SELECT * FROM admins WHERE "adminID" = {adminID}')
        row = cursor.fetchone()
        user = {}
        psql.commit()
        cursor.close()
        psql.close()
        
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
              return make_response(message, 200)  
            else:
                return make_response({'error': 'Invalid password. Please try again.'}, 400)
        else:
            return make_response({'error': 'Invalid username. Please try again.'}, 400)
    except Exception as e:
        print(e)
        #print(adminID)
        return make_response({'error': 'User not found'}, 400)
'''

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




import random
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

#----------------------------------------------------REPORTS---------------------------------------------------------#

# Returns Courses with 50 or more students 
# 
# 
# 
# 
# 
# 
# 
# All lecturers that teaches 3 or more courses will be
# 
# 
# 
# 
# 
# 
# All students that do 5 or more courses
# 
# 


# Top 10 most enrolled course
# 
# 



# Top 10 students with highest overall averages



