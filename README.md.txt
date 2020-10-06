I have a developed a school webseite application using python, css, bootstrap, html and some javascript code.

The functionality of the site is as follows:

There are three different sessions for different users, they include:
1. Admin
2. Teachers
3. Students.

Each session has its own separate functionality.

Here is a breakdown of the sessions and there capability.

1. Admin:
    On the "Teachers" menu they will see the details of registered Teachers
    On the "Students" menu they will also see the details of registered Students
    "Register":
        An admin can register another admin
        Register Teachers (they can also import a csv file containing Students details to register them)
        Register Students (they can also import a csv file containing Students details to register them)
    Upload a pdf version of students result;
    Then logout.

2. Teachers:
    On the 'Students' menu they will only see the student that is in the class that they teach
    They can register students either by uploading a csv file or manually typing students details
    Upload result in pdf format
    Lastly logout

3. Students:
    Can change the default password assigned to them during the registration process
    Now, using only there password they can check for their termly(or semester) result
    Loging out is not left out here as well.

Defintion of terms as included in the project:
    JS1-JS3: this is a short form of identifying Junior Secondary students, starting from class one to three
    SS1-SS3: this also means Senior Secondary one to three
    First Term - Third Term: terms are eqivalent to 'semester' depending on the educational system involved

Additional info:
    I used only four years or sessions (i.e. 2016-2020) to simulate the assumption of years changing
    During registration of Admin, Teachers or Students, their name is used as a default username for them to be able to do their first time login 
    A default password is also being hashed and sent to our database
    Admin can upload result for any student in any class and also register students in any class 
    A Teacher can only be assigned min of 1 & max of 3 classes during registration
    The Teachers session allows them to only register students that are in the class they teach
    Teachers are only permitted to upload result for the class they teach


    