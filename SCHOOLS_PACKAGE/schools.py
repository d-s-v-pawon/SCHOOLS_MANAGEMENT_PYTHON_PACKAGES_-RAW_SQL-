import re
import random
import copy                   #The Following modules should be imported before creating the class SCHOOLS
from tabulate import tabulate
import string
from STUDENTS_PACKAGE import students
import json
import pypyodbc as odbc

DRIVER_NAME ='SQL Server'
SERVER_NAME='LAPTOP-04Q912VM\SQLEXPRESS'
DATABASE_NAME='SCHOOL_EDUCATION'

connection_string=f"""
                        DRIVER={{{DRIVER_NAME}}};
                        SERVER={SERVER_NAME};
                        DATABASE={DATABASE_NAME};
                        Trust_Connection=yes;"""

conn=odbc.connect(connection_string)
csr=conn.cursor()

class SCHOOLS:              #creating a class named SCHOOLS
    sch_name_chars=[string.whitespace[0]]
    for i in range(26):
        sch_name_chars.append(string.ascii_uppercase[i])
    data_to_write={"sch_name_chars":sch_name_chars,
                    "max_sch_work_time":10,
                    "SY_BOARDS":['ICSE','CBSE','CCE','IB','CIE','NIOS']
    }
    
    with open("SCHOOLS_PACKAGE/properties.json","w") as f1:
        json.dump(data_to_write,f1,indent=4)                    #Creates/Opens the properties.json file in writing mode and writes all the data into the json file

    def __init__(self,sch_name,sch_time,no_stands,sch_addr,no_branch,sy_board,c_no,standards_list):                     #The __init__ constructor is used for taking the schools details as instance variables of each individual school
        class Invalidname(Exception):
            pass
        class Overtime(Exception):
            pass
        class Invalidboard(Exception):                  #User-defined Exceptions
            pass
        class Invalidcontact(Exception):
            pass

        with open('SCHOOLS_PACKAGE/properties.json', 'r') as json_file:             #The properties.json file is opened in reading mode to work with static data in the file
                data = json.load(json_file)

        try:
            sch_name=sch_name.upper()
            for i in sch_name:
                if i not in data.get('sch_name_chars'):
                    raise Invalidname
                else:
                    pass
            self.sch_name=sch_name              #Name of the school
        except Invalidname:
            print("SCHOOL NAME SHOULD CONTAIN ONLY ALPHABETS")
            while(True):                
                self.sch_name=input("ENTER VALID SCHOOL NAME:")
                self.sch_name=self.sch_name.upper()
                for i in self.sch_name:
                    if i not in data.get('sch_name_chars'):
                        self.sch_name=''
                        break
                if len(self.sch_name)>2:
                    print(self.sch_name)
                    break
        try:
            if sch_time>=data.get('max_sch_work_time'):
                raise Overtime
            print("THE SCHOOL RUNTIME IS WITHIN THE LIMIT")
            self.sch_time=input("NOW PLEASE ENTER THE SCHOOL TIMINGS:")             #Timings of the school in a day
            self.sch_time.upper()
        except Overtime:
            print(f"THE MAXIMUM SCHOOL RUNNING TIME SHOULD NOT EXCEED {data.get('max_sch_work_time')} HOURS")
            while(True):
                sch_time=int(input("ENTER VALID RUNTIME:"))
                if sch_time<data.get('max_sch_work_time'):
                    print("THE SCHOOL RUNTIME IS WITHIN THE LIMIT")
                    self.sch_time=input("NOW PLEASE ENTER THE SCHOOL TIMINGS:")
                    self.sch_time.upper()
                    break

        self.no_stands=no_stands            #Number of standards in the school

        stands=[]
        for i in range(1,self.no_stands+1):
            stands.append(i)

        data['stands']=stands

        with open("SCHOOLS_PACKAGE/properties.json","w") as f2:             #Creates/Opens the properties.json file in writing mode and writes the additional data into the json file
            json.dump(data,f2,indent=4)

        self.sch_addr=sch_addr.upper()                          #Address of the school

        self.no_branch=no_branch                                #Number of branches having for the school

        try:
            if sy_board not in data.get('SY_BOARDS'):
                raise Invalidboard
            self.sy_board=sy_board.upper()                  #Syllabus followed by the school
        except Invalidboard:
            print("THE FOLLOWING ARE MOSTLY ADAPTED SYLLABUS BOARDS BY THE SCHOOLS")
            for i in data.get('SY_BOARDS'):
                if i!=data.get('SY_BOARDS')[len(data.get('SY_BOARDS'))-1]:
                    print(i,end=',')
                else:
                    print(i)
            while(True):
                Confirm=input("Since You Have Entered An Unknown Board Please Confirm That Do You Still Want To Keep The Same Board(Y/N):")
                Confirm=Confirm.lower()
                if not re.match("^[y&n]",Confirm):
                    print("Error! Only letters Y AND N allowed!")
                    print("PLEASE CONFIRM AGAIN")
                elif Confirm=='y':                    
                    self.sy_board=sy_board
                    break
                else:
                    print("OK!THEN CHOOSE FROM THE FOLLOWING BOARDS")
                    for i in data.get('SY_BOARDS'):
                        if i!=data.get('SY_BOARDS')[len(data.get('SY_BOARDS'))-1]:
                            print(i,end=',')
                        else:
                            print(i)
                    self.sy_board=input().upper()
                if self.sy_board in data.get('SY_BOARDS'):
                    break
                else:
                    print("INVALID INPUT,CONFIRM AGAIN")                    
        try:
            if len(str(c_no))!=10:
                raise Invalidcontact
            self.c_no=c_no                              #Contact number for the school
        except Invalidcontact:
            print("CONTACT NUMBER CONTAINS ONLY 10DIGITS IN MAXIMUM")
            while(True):
                self.c_no=int(input("ENTER VALID CONTACT:"))
                if len(str(self.c_no))==10:
                    break
        finally:
            print(f"THE {self.sch_name} SCHOOL GENERAL DETAILS ENTRY IS COMPLETED")
        self.standards_list=standards_list                      #List of students in standard wise 

    def sch_details(self):                          #The school object can use this method to describe all the details of the school specified
        print(f"OUR SCHOOL NAME IS {self.sch_name}")
        print(f"THE SCHOOL TIMINGS ARE {self.sch_time}")
        print(f"THE NUMBER OF STANDARDS IN THIS SCHOOL ARE {self.no_stands}")
        print(f"ADDRESS OF THE SCHOOL: {self.sch_addr}")
        print(f"NUMBER OF BRANCHES OF THE SCHOOL ARE {self.no_branch}")
        print(f"THE SYLLABUS ADAPTED BY THE SCHOOL IS {self.sy_board}")
        print(f"CONTACT NUMBER: {self.c_no}")



    def C_YEAR_DET(self):                                   #The school object describes the current students details of the specified school using this method
        with open('SCHOOLS_PACKAGE/properties.json', 'r') as json_file:
                data = json.load(json_file)
        print(f"THE CURRENT YEAR INFO OF THE {self.sch_name} SCHOOL IS AS FOLLOWS")
        self.SCHOOL=[]
        self.CY_SCHOOL=[]
        for i in range(self.no_stands):
            CLASS=[f"CLASS_{data.get('stands')[i]}"]
            self.SCHOOL.append(CLASS)
        for j in self.standards_list:
            STU=[]
            for k in j.stu_list:
                if k.sch_name==self.sch_name:
                    for i in self.SCHOOL:                    
                        if i[0]==f"CLASS_{k.standard}":                        
                            STU.append(k)
                            break
            if STU!=[]:
                for i in self.SCHOOL:
                    if i[0]==f"CLASS_{STU[0].standard}":                             
                        i.append(STU)
                        break
        for i in self.SCHOOL:
            if len(i)>1:
                self.CY_SCHOOL.append(i)
        SCHOOL=[]
        for i in self.CY_SCHOOL:
            CLASS=[f"{i[0]}",[],[]]
            for j in i[1]:
                CLASS[1].append(j.name)
                CLASS[2].append(j.percent)
            SCHOOL.append(CLASS)
        head=["CLASS NAME","STUDENTS","PERCENTAGES"]
        print(tabulate(SCHOOL,headers=head,tablefmt="rounded_grid"))

        qry1=f"""CREATE TABLE C_YEAR_{self.sch_name}_SCHOOL(NAMES VARCHAR(30) NOT NULL,
                        GENDERS VARCHAR(10) NOT NULL,
                        AGES INT NOT NULL,
                        SCHOOL_NAMES VARCHAR(30) NOT NULL,
                        STANDARDS INT NOT NULL,
                        SECTIONS VARCHAR(2) NOT NULL,
                        ROLL_NUMBERS INT PRIMARY KEY,
                        CONTACT_NUMBERS BIGINT UNIQUE,
                        PERCENTAGES FLOAT(5) NOT NULL)"""
        csr.execute(qry1)
        csr.commit()

        for i in self.CY_SCHOOL:
            for j in i[1]:
                qry2=f"""INSERT INTO C_YEAR_{self.sch_name}_SCHOOL VALUES('{j.name}',
                        '{j.gender}',
                        '{j.age}',
                        '{j.sch_name}',
                        '{j.standard}',
                        '{j.section}',
                        '{j.r_no}',
                        '{j.c_no}',
                        '{j.percent}')"""
        csr.execute(qry2)
        csr.commit()


    def N_YEAR_DET(self):                       #The school object describes the students details of the school specified using this method
        print(f"THE NEXT YEAR INFO OF THE {self.sch_name} SCHOOL IS AS FOLLOWS")
        self.NY_SCHOOL=[]
        for i in self.CY_SCHOOL:
            if i==self.CY_SCHOOL[0]:
                N_CLASS=[f"CLASS_{int(i[1][0].standard)+1}"]
                CLASS=[f"CLASS_{int(i[1][0].standard)}"]
                STU=[]
                N_STU=[]
                for j in i[1]:
                    if j.percent>75:
                        N_STU.append(copy.deepcopy(j))
                    else:
                        STU.append(copy.deepcopy(j))
                if STU!=[]:
                    CLASS.append(STU)
                if N_STU!=[]:
                    N_CLASS.append(N_STU)
                if len(CLASS)>1:
                    self.NY_SCHOOL.append(CLASS)
                if len(N_CLASS)>1:
                    self.NY_SCHOOL.append(N_CLASS)
            elif i==self.CY_SCHOOL[len(self.CY_SCHOOL)-1]:
                N_CLASS=[f"CLASS_{int(i[1][0].standard)+1} SCHOOL MIGRATORS"]
                N_STU=[]
                for j in i[1]:
                    if j.percent>75:
                        N_STU.append(copy.deepcopy(j))
                    else:
                        for k in self.NY_SCHOOL:
                            if k[0]==f"CLASS_{j.standard}":
                                k[1].append(copy.deepcopy(j))
                            else:
                                if k==self.NY_SCHOOL[len(self.NY_SCHOOL)-1]:
                                    STU.append(copy.deepcopy(j))
                if STU!=[]:
                    CLASS.append(STU)
                if N_STU!=[]:
                    N_CLASS.append(N_STU)
                if len(CLASS)>1:
                    self.NY_SCHOOL.append(CLASS)
                if len(N_CLASS)>1:
                    self.NY_SCHOOL.append(N_CLASS)
            else:
                N_CLASS=[f"CLASS_{int(i[1][0].standard)+1}"]
                N_STU=[]
                CLASS=[f"CLASS_{int(i[1][0].standard)}"]
                STU=[]
                for j in i[1]:
                    if j.percent>75:
                        N_STU.append(copy.deepcopy(j))
                    else:
                        for k in self.NY_SCHOOL:
                            if k[0]==f"CLASS_{j.standard}":
                                k[1].append(copy.deepcopy(j))
                            else:
                                if k==self.NY_SCHOOL[len(self.NY_SCHOOL)-1]:
                                    STU.append(copy.deepcopy(j))
                if STU!=[]:
                    CLASS.append(STU)
                if N_STU!=[]:
                    N_CLASS.append(N_STU)
                if len(CLASS)>1:
                    self.NY_SCHOOL.append(CLASS)
                if len(N_CLASS)>1:
                    self.NY_SCHOOL.append(N_CLASS)
        for i in self.NY_SCHOOL:
            for j in i[1]:
                if j.percent>75:
                    j.standard=j.standard+1
        N_SCHOOL=[]
        for i in self.NY_SCHOOL:
            CLASS=[f"{i[0]}",[],[]]
            for j in i[1]:
                CLASS[1].append(j.name)
                CLASS[2].append(j.percent)
            N_SCHOOL.append(CLASS)
        head=["CLASS NAME","STUDENTS","PERCENTAGES"]
        print(tabulate(N_SCHOOL,headers=head,tablefmt="rounded_grid"))

        qry1=f"""CREATE TABLE N_YEAR_{self.sch_name}_SCHOOL(NAMES VARCHAR(30) NOT NULL,
                GENDERS VARCHAR(10) NOT NULL,
                AGES INT NOT NULL,
                SCHOOL_NAMES VARCHAR(30) NOT NULL,
                STANDARDS INT NOT NULL,
                SECTIONS VARCHAR(2) NOT NULL,
                ROLL_NUMBERS INT PRIMARY KEY,
                CONTACT_NUMBERS BIGINT UNIQUE,
                PERCENTAGES FLOAT(5) NOT NULL)"""
        csr.execute(qry1)
        csr.commit()

        for i in self.NY_SCHOOL:
            for j in i[1]:
                qry2=f"""INSERT INTO N_YEAR_{self.sch_name}_SCHOOL VALUES('{j.name}',
                        '{j.gender}',
                        '{j.age}',
                        '{j.sch_name}',
                        '{j.standard}',
                        '{j.section}',
                        '{j.r_no}',
                        '{j.c_no}',
                        '{j.percent}')"""
        csr.execute(qry2)
        csr.commit()



    def promotion_status(self,stu_name):                #The school object specifies the promotion status of an individual student using this method
        self.stu_name=stu_name.upper()
        for i in self.CY_SCHOOL:
            for j in i[1]:
                if self.stu_name==j.name:
                    for k in self.NY_SCHOOL:
                        for l in k[1]:
                            if self.stu_name==l.name and l.standard==j.standard+1:
                                print(f'YES!THE STUDENT {self.stu_name} IS PROMOTED FROM THE CLASS {j.standard} TO THE NEXT CLASS {l.standard}')
    


    trans_stu=[[],[]]
    def STU_TRANSFERS(self,stu_name):                   #The school object specifies the transfer details of the students from the specified school using this method
        self.stu_name=stu_name.upper()
        print(f"THE STUDENT {self.stu_name} IS APPLIED FOR TRANSFER FROM THE SCHOOL {self.sch_name}")
        for i in self.NY_SCHOOL:
            for j in i[1]:
                if j.name==self.stu_name:
                    self.trans_stu[0].append(j.standard)
                    self.trans_stu[1].append(j.r_no)
                    i[1].remove(j)
                    print(f"THE STUDENT IS TRANSFERRED SUCCESSFULLY FROM THE SCHOOL {self.sch_name}")
                    break
                else:
                    pass
        for i in self.NY_SCHOOL:
            if i[1]!=[]:
                if i[1][0].standard>self.no_stands:            
                    print(f"THE STUDETNS WHO COMPLETED THEIR SCHOOL EDUCATION IN THE {self.sch_name} ARE AS FOLLOWS")
                    for j in i[1]:
                        print(j.name)
                    self.NY_SCHOOL.remove(i)
                    print()
                    print(f"THE ABOVE ALL STUDENTS CAN JOIN IN COLLEGES WITHOUT ANY FAIL")
                    print(f"THESE STUDENTS ARE SUCCESFULLY TRANSFERRED FROM THE SCHOOL")
                    break
        print(f"THE NEXT YEAR INFO OF THE {self.sch_name} SCHOOL AFTER STUDENT TRANSFERS IS AS FOLLOWS")
        N_SCHOOL=[]
        for i in self.NY_SCHOOL:
            CLASS=[f"{i[0]}",[],[]]
            for j in i[1]:
                CLASS[1].append(j.name)
                CLASS[2].append(j.percent)
            N_SCHOOL.append(CLASS)
        head=["CLASS NAME","STUDENTS","PERCENTAGES"]
        print(tabulate(N_SCHOOL,headers=head,tablefmt="rounded_grid"))
        print(self.trans_stu)

        qry=f"""DELETE FROM N_YEAR_{self.sch_name}_SCHOOL WHERE ROLL_NUMBERS={j.c_no}"""
        csr.execute(qry)
        csr.commit()



    def NEW_ADMISSIONS(self,name,gender,age,standard,c_no,percent):                 #The school object specifies the new admission details of the students into the school using this method
        sch_name=self.name
        r_no=0
        section=None
        n_stu=students.STUDENTS(name,gender,age,sch_name,standard,section,r_no,c_no,percent)
        n_stu.stu_details()
        st_list=[]
        for i in self.NY_SCHOOL:
            if i[1]!=[]:
                st_list.append(i[1][0].standard)
        if n_stu.standard+1 in st_list:
            if n_stu.percent>60:
                n_stu.standard=n_stu.standard+1
                for i in self.NY_SCHOOL:
                    if i[0]==f"CLASS_{n_stu.standard}":                
                        i[1].append(n_stu)
                        print(f"THE STUDENT IS SUCCESSFULLY ADMITTED INTO THE CLASS {n_stu.standard} IN THE SCHOOL")
                        if n_stu.standard in self.trans_stu[0]:
                            n_stu.r_no=self.trans_stu[1][self.trans_stu[0].index(n_stu.standard)]
                            self.trans_stu[0].remove(n_stu.standard)
                            self.trans_stu[1].remove(n_stu.r_no)
                        else:
                            r_nos=[]
                            for j in range(len(i[1])):
                                r_nos.append(i[1][j].r_no)
                            r_nos.sort()
                            n_stu.r_no=r_nos[len(r_nos)-1]+1
                        n_stu.section=random.choice(['A','B','C'])
                        print(f"THE ROLL_NUMBER OF THE STUDENT {n_stu.name} FOR THE CLASS {n_stu.standard} IN THE SECTION_{n_stu.section} IS {n_stu.r_no}")
                        break
            else:
                print(f"THE STUDENT ANNUAL YEAR PERCENTAGE OF THE CLASS {n_stu.standard} IS VERY POOR(LESS THAN 60),HE WON'T BE ADMITTED INTO THE NEXT CLASS {n_stu.standard+1} DIRECTLY")
                command=input("DO YOU WANT HIS/HER ADMISSION INTO THEIR SAME CLASS(Y/N):")
                command=command.lower()
                if not re.match("^[y&n]",command):
                    print("Error! Only letters Y AND N allowed!")
                    print("PLEASE TRY AGAIN")
                else:
                    if command=='y':
                        if n_stu.standard in st_list:
                            for i in self.NY_SCHOOL:
                                if i[0]==f"CLASS_{n_stu.standard}":                
                                    i[1].append(n_stu)
                                    print(f"THE STUDENT IS SUCCESSFULLY ADMITTED INTO THE CLASS {n_stu.standard} IN THE SCHOOL")
                                    if n_stu.standard in self.trans_stu[0]:
                                        n_stu.r_no=self.trans_stu[1][self.trans_stu[0].index(n_stu.standard)]
                                        self.trans_stu[0].remove(n_stu.standard)
                                        self.trans_stu[1].remove(n_stu.r_no)
                                    else:
                                        r_nos=[]
                                        for j in range(len(i[1])):
                                            r_nos.append(i[1][j].r_no)
                                        r_nos.sort()
                                        n_stu.r_no=r_nos[len(r_nos)-1]+1
                                    n_stu.section=random.choice(['A','B','C'])
                                    print(f"THE ROLL_NUMBER OF THE STUDENT {n_stu.name} FOR THE CLASS {n_stu.standard} IN THE SECTION_{n_stu.section} IS {n_stu.r_no}")
                                    break
                        else:
                            CLASS=[f"CLASS_{n_stu.standard}"]
                            STU=[]
                            STU.append(n_stu)
                            CLASS.append(STU)
                            classes=[]
                            for i in range(1,self.no_stands+1):
                                classes.append(i)
                            if n_stu.standard in classes:                            
                                i=n_stu.standard
                                if i>st_list[0]:               
                                    while(True):
                                        i-=1
                                        if i in st_list:
                                            INDEX=st_list.index(i)+1
                                            break
                                else:                            
                                    INDEX=0
                                self.NY_SCHOOL.insert(INDEX,CLASS)
                                print(f"THE STUDENT IS SUCCESSFULLY ADMITTED INTO THE CLASS {n_stu.standard} IN THE SCHOOL")
                                if n_stu.standard in self.trans_stu[0]:
                                    n_stu.r_no=self.trans_stu[1][self.trans_stu[0].index(n_stu.standard)]
                                    self.trans_stu[0].remove(n_stu.standard)
                                    self.trans_stu[1].remove(n_stu.r_no)
                                else:
                                    n_stu.r_no=1
                                n_stu.section='A'
                                print(f"THE ROLL_NUMBER OF THE STUDENT {n_stu.name} FOR THE CLASS {n_stu.standard} IN THE SECTION_{n_stu.section} IS {n_stu.r_no}")
                            else:                            
                                print(f"THERE IS NO SUCH CLASS {n_stu.standard} IN THE SCHOOL {self.sch_name} TO JOIN YOU")
                                print("PLEASE RECHECK AND TRY AGAIN")
                    else:
                        print("THANK YOU,BETTER LUCK NEXT TIME")
        else:
            if n_stu.percent>60:
                n_stu.standard=n_stu.standard+1
                CLASS=[f"CLASS_{n_stu.standard}"]
                STU=[]
                STU.append(n_stu)
                CLASS.append(STU)
                classes=[]
                for i in range(1,self.no_stands+1):                    
                    classes.append(i)
                if n_stu.standard in classes:                    
                    i=n_stu.standard
                    if i>st_list[0]:                        
                        while(True):                            
                            i-=1
                            if i in st_list:
                                INDEX=st_list.index(i)+1
                                break
                    else:                        
                        INDEX=0
                    self.NY_SCHOOL.insert(INDEX,CLASS)
                    print(f"THE STUDENT IS SUCCESSFULLY ADMITTED INTO THE CLASS {n_stu.standard} IN THE SCHOOL")
                    if n_stu.standard in self.trans_stu[0]:                        
                        n_stu.r_no=self.trans_stu[1][self.trans_stu[0].index(n_stu.standard)]
                        self.trans_stu[0].remove(n_stu.standard)
                        self.trans_stu[1].remove(n_stu.r_no)
                    else:
                        n_stu.r_no=1
                    n_stu.section='A'
                    print(f"THE ROLL_NUMBER OF THE STUDENT {n_stu.name} FOR THE CLASS {n_stu.standard} IN THE SECTION_{n_stu.section} IS {n_stu.r_no}")
                else:                    
                    print(f"THERE IS NO SUCH CLASS {n_stu.standard} IN THE SCHOOL {self.sch_name} TO JOIN YOU")
                    print("PLEASE RECHECK AND TRY AGAIN")               
            else:
                print(f"THE STUDENT ANNUAL YEAR PERCENTAGE OF THE CLASS {n_stu.standard} IS VERY POOR(LESS THAN 60),HE WON'T BE ADMITTED INTO THE NEXT CLASS {n_stu.standard+1} DIRECTLY")
                command=input("DO YOU WANT HIS/HER ADMISSION INTO THEIR SAME CLASS(Y/N):")
                command=command.lower()
                if not re.match("^[y&n]",command):
                    print("Error! Only letters Y AND N allowed!")
                    print("PLEASE TRY AGAIN")
                else:
                    if command=='y':
                        if n_stu.standard in st_list:
                            for i in self.NY_SCHOOL:
                                if i[0]==f"CLASS_{n_stu.standard}":                
                                    i[1].append(n_stu)
                                    print(f"THE STUDENT IS SUCCESSFULLY ADMITTED INTO THE CLASS {n_stu.standard} IN THE SCHOOL")
                                    if n_stu.standard in self.trans_stu[0]:
                                        n_stu.r_no=self.trans_stu[1][self.trans_stu[0].index(n_stu.standard)]
                                        self.trans_stu[0].remove(n_stu.standard)
                                        self.trans_stu[1].remove(n_stu.r_no)
                                    else:
                                        r_nos=[]
                                        for j in range(len(i[1])):
                                            r_nos.append(i[1][j].r_no)
                                        r_nos.sort()
                                        n_stu.r_no=r_nos[len(r_nos)-1]+1
                                    n_stu.section=random.choice(['A','B','C'])
                                    print(f"THE ROLL_NUMBER OF THE STUDENT {n_stu.name} FOR THE CLASS {n_stu.standard} IN THE SECTION_{n_stu.section} IS {n_stu.r_no}")
                                    break
                        else:
                            CLASS=[f"CLASS_{n_stu.standard}"]
                            STU=[]
                            STU.append(n_stu)
                            CLASS.append(STU)
                            classes=[]
                            for i in range(1,self.no_stands+1):
                                classes.append(i)
                            if n_stu.standard in classes:                            
                                i=n_stu.standard
                                if i>st_list[0]:               
                                    while(True):
                                        i-=1
                                        if i in st_list:
                                            INDEX=st_list.index(i)+1
                                            break
                                else:                            
                                    INDEX=0
                                self.NY_SCHOOL.insert(INDEX,CLASS)
                                print(f"THE STUDENT IS SUCCESSFULLY ADMITTED INTO THE CLASS {n_stu.standard} IN THE SCHOOL")
                                if n_stu.standard in self.trans_stu[0]:
                                    n_stu.r_no=self.trans_stu[1][self.trans_stu[0].index(n_stu.standard)]
                                    self.trans_stu[0].remove(n_stu.standard)
                                    self.trans_stu[1].remove(n_stu.r_no)
                                else:
                                    n_stu.r_no=1
                                n_stu.section='A'
                                print(f"THE ROLL_NUMBER OF THE STUDENT {n_stu.name} FOR THE CLASS {n_stu.standard} IN THE SECTION_{n_stu.section} IS {n_stu.r_no}")
                            else:                            
                                print(f"THERE IS NO SUCH CLASS {n_stu.standard} IN THE SCHOOL {self.sch_name} TO JOIN YOU")
                                print("PLEASE RECHECK AND TRY AGAIN")
                    else:                        
                        print("THANK YOU,BETTER LUCK NEXT TIME")
        print(f"THE NEXT YEAR INFO OF THE {self.sch_name} SCHOOL AFTER NEW ADMISSIONS IS AS FOLLOWS")
        N_SCHOOL=[]
        for i in self.NY_SCHOOL:
            CLASS=[f"{i[0]}",[],[]]
            for j in i[1]:
                CLASS[1].append(j.name)
                CLASS[2].append(j.percent)
            N_SCHOOL.append(CLASS)
        head=["CLASS NAME","STUDENTS","PERCENTAGES"]
        print(tabulate(N_SCHOOL,headers=head,tablefmt="rounded_grid"))

        qry=f"""INSERT INTO N_YEAR_{self.sch_name}_SCHOOL VALUES('{n_stu.name}',
                                '{n_stu.gender}',
                                '{n_stu.age}',
                                '{n_stu.sch_name}',
                                '{n_stu.standard}',
                                '{n_stu.section}',
                                '{n_stu.r_no}',
                                '{n_stu.c_no}',
                                '{n_stu.percent}')"""
        csr.execute(qry)
        csr.commit()



    def FEE(self,stu_name):                         #The school object specifies the fee details of an individual student in the specified school using this method
        self.stu_name=stu_name.upper()
        for i in self.NY_SCHOOL:
            for j in i[1]:
                if j.name==self.stu_name:
                    fee=j.standard*5000
                    print(f'THE FEE OF {self.stu_name} FOR THE NEXT YEAR FOR THE CLASS {j.standard} is {fee}')
                    break



    def t_removals(self):                                   #The school object specifies the teacher removals from the specified school using this method
        TEACHERS=[['PRASAD','TELUGU',8],['RAMANA','HINDI',7],['SRINIVAS','ENGLISH',6],['MADHU','MATHS',8],['RASHIDA','PHYSICS',8],['RAJU','CHEMISTRY',5],['AHMAD','SOCIAL',8],['ARJUN','BIOLOGY',6],['PARVATHI','PET',8],['SARASWATHI','SANSKRIT',8]]
        self.N_TEACHERS=[]
        for i in TEACHERS:
            if i[2]>=7:
                self.N_TEACHERS.append(i)
        print('THE STAFF REMOVED FROM THE SCHOOL ARE')
        for i in TEACHERS:
            if i[2]<7:
                print(i[0],end=',')



    def t_appoint(self,name,subject,t_points):                  #The school object specifies the teacher appointments into the specified school using this method
        self.name=name.upper()
        self.subject=subject.upper()
        self.t_points=t_points
        if self.t_points>=7:
            self.N_TEACHERS.append([self.name,self.subject,self.t_points])
        else:
            print("SORRY!BETTER LUCK MEXT TIME")
        print('THE STAFF LIST AFTER NEW APPOINTMENTS')
        print(self.N_TEACHERS)