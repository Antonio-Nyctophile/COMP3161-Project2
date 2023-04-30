from data import female as Fname, male as Mname, lastname as Lname
import random
import string
import csv


emailDomains = [
    "gmail.com",
    "yahoo.com",
    "outlook.com",
    "hotmail.com",
    "icloud.com",
    "aol.com",
    "protonmail.com",
    "zoho.com",
    "mail.com",
    "yandex.com",
    "inbox.com",
    "mailinator.com",
    "gmx.com",
    "live.com",
    "fastmail.com",
    "tutanota.com",
    "rocketmail.com",
    "disposable.com",
    "hushmail.com",
    "proemail.com"
]

firstNames = [Fname, Mname]
userID = 630000001

#Generate a random email based on the name parameters entered
def generateRandomEmail(fname, lname):
  choice = random.randint(0,2)
  first = [fname, fname[random.randint(0, len(fname)-1):], fname[:random.randint(0, len(fname)-1)]]
  last = [lname, lname[random.randint(0, len(lname)-1):], lname[:random.randint(0, len(lname)-1)]]
  format = [random.choice(first), random.choice(last), str(random.randint(0, 1000))]
  random.shuffle(format)
  if choice == 0:
    return format[0] + '@'+random.choice(emailDomains)
  if choice == 1:
    return format[0] + format[1] + "@" +random.choice(emailDomains)
  return format[0] + format[1] + format[2] + "@" +random.choice(emailDomains)

#Generates a random username based on the name parameters entered
def generate_username(firstname, lastname):
    # Convert the first and last names to lowercase
    firstname = firstname.lower()
    lastname = lastname.lower()

    # Extract the first and last name initials
    firstname_initial = firstname[0]
    lastname_initial = lastname[0]

    # Randomly choose a variation of the first and last name
    variations = [
        firstname,
        lastname,
        f"{firstname}_{lastname}",
        f"{firstname}{lastname}",
        f"{firstname}_{lastname_initial}",
        f"{firstname_initial}{lastname}",
        f"{firstname_initial}_{lastname_initial}",
    ]
    username = random.choice(variations)

    
    random_number = random.randint(1000, 9999)

    
    username += str(random_number)

    return username

#Generates a random password of length specified as the parameter
def generate_password(length=12):
    # Define the characters to choose from
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate a random password
    password = ''.join(random.choice(characters) for _ in range(length))

    return password

#Adjust the CSV file for the data to be written
csv_file = "LecturerDataBase.csv"


EntriesNeeded = 1050 #How many unique enteries needed
for x in range(EntriesNeeded):
  random_number = random.randint(0, 1)
  FnameChoice = firstNames[random_number]
  studentFname = random.choice(FnameChoice)
  studentLname = random.choice(Lname)
  studentEmail = generateRandomEmail(studentFname, studentLname)
  #UserName = generate_username(studentFname, studentLname)
  password = generate_password()
  data = [str(userID), studentFname, studentLname, studentEmail, UserName, password]
  #data = [str(userID), studentFname, studentLname, studentEmail, password]
  userID +=1 
  


  with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(data)

print("Data has been written to the CSV file.")

"""Course Generation"""

csv_file = "CourseDataBase.csv"

import random
import string


start = "01/09/2023"
end = "31/12/2023"

#Generates a list of different course names and their associated course numbers
def generate_course_names(n):
    adjectives = ['Advanced', 'Introductory', 'Fundamental', 'Applied', 'Theoretical', 'Experimental', 'Computational', 'Statistical']
    subjects = ['Mathematics', 'Mathematics ', 'Physics', 'Chemistry', 'Biology', 'Computer Science', 'Engineering', 'Economics', 'Psychology', "Business", "Agriculture", "Astrology", "Philosophy", "Sociology"]
    newSubs = []
    courses = []
    courseCode = []
    for x in subjects:
      newSubs.append(x+" I")
      
      newSubs.append(x+" II")
      
      newSubs.append(x+" III")
     
      newSubs.append(x+" IV")
      
      newSubs.append(x+" V")
      
    subjects = newSubs
    number = 1
    for x in subjects:
      count = 1000
      
      for y in adjectives:
        courses.append(y + " " + x)
        courseCode.append(x[:4].upper()+str(count+number))
        count += 1000
      number += 2
    
    
    print(len(courseCode), len(courses))
    return courseCode, courses

CCList,CNameList = generate_course_names(350)

for x in range(350):
  data = [CCList[x], CNameList[x], start, end]
  with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(data)
