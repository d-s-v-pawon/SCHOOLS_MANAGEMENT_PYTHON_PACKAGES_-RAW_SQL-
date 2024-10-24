import json             #imports json to read and write the content from json properties file

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

class STANDARDS:                                #Creating the class named standards

    data_to_write={ "sub_num":[5,6],
                    "max_att_per":100,
                    "max_sch_time_high":10,
                    "max_sch_time_pri":7}
    with open("STANDARDS_PACKAGE/properties.json","w") as f1:
        json.dump(data_to_write,f1,indent=4)                            #Writing all the data_to_write into the json file

    def __init__(self,name,no_subjects,min_att_per,max_cap,max_sch_time,stu_list):

        stands=[]
        for i in stu_list:                
                if i.standard not in stands:                                #Collects all the students standards in a single list without having duplicates
                    stands.append(i.standard)
                stands.sort()


        with open('STANDARDS_PACKAGE/properties.json', 'r') as json_file:                       #Loads all the data from the json file to write additional content                
                data = json.load(json_file)

        data["stands"]=stands
        with open("STANDARDS_PACKAGE/properties.json","w") as f2:               #Writes additional content into the data and dumps it into the json file again        
                json.dump(data,f2,indent=4)

        with open('STANDARDS_PACKAGE/properties.json', 'r') as json_file:           #Again loads all the data from the json file to work with the data
                data = json.load(json_file)

        class noclass(Exception):
            pass
        class Invalidnum(Exception):
            pass
        class Overatt(Exception):                                           #User-defined exceptions
            pass
        class Overtime(Exception):
            pass

        try:
            if name not in data.get('stands'):
                raise noclass
            self.name=name          #Name of the standard in numbers
        except noclass:
            print(f"NO STUDENTS DETAILS ENTERED FOR THE CLASS {name}")
            print("TRY FOR ANOTHER CLASS")        
        else:
            try:
                if self.name<=5:
                    if no_subjects!=data.get('sub_num')[0]:
                        raise Invalidnum
                else:
                    if no_subjects!=data.get('sub_num')[1]:
                        raise Invalidnum
                self.no_subjects=no_subjects
            except Invalidnum:
                print("THE PRIMARY CLASS STUDENTS CONTAINS FIVE SUBJECTS AND HIGHER STUDENTS HAVE SIX")
                if self.name<=5:
                    while(True):
                        self.no_subjects=int(input("ENTER VALID NUMBER OF SUBJECTS:"))
                        if self.no_subjects==data.get('sub_num')[0]:
                            break
                else:
                    while(True):
                        self.no_subjects=int(input("ENTER VALID NUMBER OF SUBJECTS:"))
                        if self.no_subjects==data.get('sub_num')[1]:
                            break
        try:
            if min_att_per>=data.get('max_att_per'):
                raise Overatt
            self.min_att_per=min_att_per         #MINIMUM ATTENDANCE PERCENTAGE
        except Overatt:
            print("THE MINIMUM ATTENDANCE PERCENT FOR A STUDENT IN A YEAR SHOULD NOT BE 100 OR ABOVE PERCENT")
            while(True):
                self.min_att_per=int(input("ENTER THE ACCEPTABLE MINIMUM ATTENDANCE PERCENT:"))
                if self.min_att_per<data.get('max_att_per'):
                    break
        self.max_cap=max_cap            #Capacity of the standard
        try:
            if self.name<=5:
                if max_sch_time>=data.get('max_sch_time_pri'):
                    raise Overtime
            else:
                if max_sch_time>=data.get('max_sch_time_high'):
                    raise Overtime
            self.max_sch_time=max_sch_time         #MAXIMUM TIME TO SPEND IN ANY SCHOOL FOR THE CLASS STUDENTS
        except Overtime:
            if self.name<=5:
                print(f"THE PRIMARY STUDENT MAXIMUM SCHOOL TIME SHOULD BE LESS THAN {data.get('max_sch_time_pri')} HOURS")
                while(True):
                    self.max_sch_time=int(input("ENTER THE SCHOOL TIME BELOW MAX_TIME:"))
                    if self.max_sch_time<data.get('max_sch_time_pri'):
                        break
            else:
                print(f"THE HIGHER STUDENT MAXIMUM SCHOOL TIME SHOUULD BE LESS THAN {data.get('max_sch_time_high')} HOURS")
                while(True):
                    self.max_sch_time=int(input("ENTER THE SCHOOL TIME BELOW MAX_TIME:"))
                    if self.max_sch_time<data.get('max_sch_time_high'):
                        break
        finally:
            self.stu_list=stu_list      #List of students entered 
            print(f"THE CLASS {self.name} GENERAL DETAILS ENTRY IS COMPLETED")
        
    def cls_details(self):              #A standard object describes the details of the specified standard using this method
        print(f"THE DETAILS OF CLASS{self.name} ARE AS FOLLOWS:")
        print(f"THIS IS CLASS {self.name}")
        print(f"NUMBER OF SUBJECTS FOR THIS CLASS STUDENTS ARE {self.no_subjects}")
        print(f"MINIMUM ATTENDANCE PERCENTAGE REQUIRED FOR THIS CLASS STUDENTS IS {self.min_att_per}%")
        print(f"THE NUMBER OF STUDENTS IN THIS CLASS INCLUDING ALL SECTIONS SHOULD NOT EXCEED {self.max_cap} STUDENTS")
        print(f"THE STUDENTS SHOULD SPEND ONLY {self.max_sch_time} HOURS TIME IN THE SCHOOL")


    def cls_students(self):             #A standard object specifies the students of the specified standard using this method
        self.CLASS=[]
        for i in self.stu_list:
            if i.standard==self.name:
                self.CLASS.append(i)
        print(f"STUDENTS OF THE CLASS {self.name} ARE AS FOLLOWS")
        for i in self.CLASS:            
            print(i.name,end=' ')
            print(i.section)
        self.stu_list=self.CLASS

        qry1=f"""CREATE TABLE CLASS_{self.name}(NAMES VARCHAR(30) NOT NULL,
                GENDERS VARCHAR(10) NOT NULL,
                AGES INT NOT NULL,
                SCHOOL_NAMES VARCHAR(30) NOT NULL,
                STANDARDS INT NOT NULL,
                SECTIONS VARCHAR(2) NOT NULL,
                ROLL_NUMBERS INT PRIMARY KEY,
                CONTACT_NUMBERS BIGINT UNIQUE,
                PERCENTAGES FLOAT(5) NOT NULL)"""
        csr.execute(qry1)
        for i in self.CLASS:
            qry2=f"""INSERT INTO CLASS_{self.name} VALUES('{i.name}','{i.gender}','{i.age}','{i.sch_name}','{i.standard}','{i.section}','{i.r_no}','{i.c_no}','{i.percent}')"""
            csr.execute(qry2)
        csr.commit()


    def SECT_STU(self):                     #A standard object specifies the students of the specified standard based on their sections using this method
        self.SECTS={}
        for i in self.CLASS:
            if i.section in self.SECTS.keys():
                self.SECTS[i.section].append(i)
            else:
                SECT_NAME=f"{i.section}"
                self.SECTS[SECT_NAME]=[]
                self.SECTS[i.section].append(i)
        for j in self.SECTS.keys():
            if self.SECTS[j]==[]:
                pass
            else:
                print(f"CLASS {self.name} SECTION_{j} STUDENTS ARE:")
                for k in self.SECTS[j]:
                    print(f"{k.name}")



    def GENDER(self):           #A standard object specifies the students of the specified standard on gender basis using this method
        for i in self.SECTS.keys():         
            G1=[]
            G2=[]
            for j in self.SECTS.get(i):
                if j.gender=='MALE':
                    G1.append(j)
                if j.gender=='FEMALE':
                    G2.append(j)
            self.SECTS[i]=[]
            self.SECTS[i].append(G1)
            self.SECTS[i].append(G2)
            print()
            print(f"MALE STUDENTS OF CLASS {self.name} AND SECTION_{i} ARE AS FOLLOWS:")
            for k in self.SECTS[i][0]:
                print(k.name,k.gender)
            print()
            print(f"FEMALE STUDENTS OF CLASS {self.name} AND SECTION_{i} ARE AS FOLLOWS:")
            for k in self.SECTS[i][1]:
                print(k.name,k.gender)
            print()
            print()



    def CLASSROOM(self):            #A standard object specifies about it's classroom for the specified standard structure using this method
        print("THE MALE STUDENTS SITS ON THE RIGHT SIDE BENCHES IN THE CLASSROOM")
        print("THE FEMALE STUDENTS SITS ON THE LEFT SIDE BENCHES IN THE CLASSROOM")
        RIGHT=[]
        LEFT=[]
        for i in self.SECTS.keys():
            for k in self.SECTS[i][0]:
                RIGHT.append(k)
            for k in self.SECTS[i][1]:
                LEFT.append(k)
        print(f"IT MEANS THE STUDENTS ON THE RIGHT BENCHES IN CLASS {self.name} ARE AS FOLLOWS:")
        for j in RIGHT:
            print(j.name,end=' ')
        print()
        print(f"THE STUDENTS ON THE LEFT BENCHES IN CLASS {self.name} ARE AS FOLLOWS:")
        for j in LEFT:
            print(j.name,end=' ')
        print()



    def SUBJECTS(self):         #A standard object specifies the subjects for the specified standard students using this method
        if self.name<=5:
            print("THE SUBJECTS FOR PRIMARY STUDENTS ARE")
            print("TELUGU","HINDI","ENGLISH","MATHS","EVS",sep=',')
        elif(self.name<=7):
            print("THE SUBJECTS FOR UPPER PRIMARY STUDENTS ARE")
            print("TELUGU","HINDI","ENGLISH","MATHS","SCIENCE","SOCIAL",sep=',')
        else:
            print("THE SUBJECTS FOR HIGHER CLASS STUDENTS ARE")
            print("TELUGU","HINDI","ENGLISH","MATHS","SCIENCE","SOCIAL",sep=",")
            print("HERE SCIENCE IS CLASSIFIED INTO TWO PARTS")
            print("SCIENCE=",["PHYSICAL SCIENCE","BIOLOGICAL SCIENCE"])
            print("PHYSICAL SCIECNE=",["PHYSICS","CHEMISTRY"])



    def PERIODS(self):      #A standard object specifies about the periods for the specified standard students using this periods method
        if self.name<=5:
            print(f"THE SCHOOL TIME FOR PRIMARY STUDENS IS {self.max_sch_time} HOURS")
            print("FIVE GENERAL PERIODS FOR FIVE SUBJECTS")
            print("EACH PERIOD SHOULD BE OF 40 MIN ONLY")
            print(f"THREE PERIODS SHOULD BE FOR PLAYTIME WITHIN {self.max_sch_time} HOURS OF 45MIN EACH")
            print(f"IF TIME LEFT,THE REMAINING TIME OF {self.max_sch_time} HOURS SHOULD BE USED ACCORDINGLY")
        elif(self.name<=7):
            print(f"THE SCHOOL TIME FOR UPPER PRIMARY STUDENS IS {self.max_sch_time} HOURS")
            print("SIX GENERAL PERIODS FOR SIX SUBJECTS")
            print("EACH PERIOD SHOULD BE OF 45 MIN ONLY")
            print(f"TWO PERIODS SHOULD BE FOR PLAYTIME WITHIN {self.max_sch_time} HOURS OF 45MIN EACH")
            print(f"IF TIME LEFT,THE REMAINING TIME OF {self.max_sch_time} HOURS SHOULD BE USED ACCORDINGLY")
        else:
            print(f"THE SCHOOL TIME FOR HIGHER STUDENS IS {self.max_sch_time} HOURS")
            print("EIGHT GENERAL PERIODS FOR SIX SUBJECTS")
            print("EACH PERIOD SHOULD BE OF 45 MIN ONLY")
            print(f"ONE PERIOD SHOULD BE FOR PLAYTIME WITHIN {self.max_sch_time} HOURS OF 1HOUR")
            print(f"IF TIME LEFT,THE REMAINING TIME OF {self.max_sch_time} HOURS SHOULD BE USED ACCORDINGLY")
