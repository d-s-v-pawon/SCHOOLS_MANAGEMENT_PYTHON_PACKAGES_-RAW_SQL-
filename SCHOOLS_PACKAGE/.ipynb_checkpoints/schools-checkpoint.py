import re
import random
import copy
from tabulate import tabulate
import string
class SCHOOLS:
    sch_name_chars=[string.whitespace[0]]
    for i in range(26):
        sch_name_chars.append(string.ascii_uppercase[i])
    max_sch_work_time=10
    SY_BOARDS=['ICSE','CBSE','CCE','IB','CIE','NIOS']
    def __init__(self,sch_name,sch_time,no_stands,sch_addr,no_branch,sy_board,c_no,standards_list):
        class Invalidname(Exception):
            pass
        class Overtime(Exception):
            pass
        class Invalidboard(Exception):
            pass
        class Invalidcontact(Exception):
            pass
        try:
            sch_name=sch_name.upper()
            for i in sch_name:
                if i not in SCHOOLS.sch_name_chars:
                    raise Invalidname
                else:
                    pass
            self.sch_name=sch_name
        except Invalidname:
            print("SCHOOL NAME SHOULD CONTAIN ONLY ALPHABETS")
            while(True):                
                self.sch_name=input("ENTER VALID SCHOOL NAME:")
                self.sch_name=self.sch_name.upper()
                for i in self.sch_name:
                    if i not in SCHOOLS.sch_name_chars:
                        self.sch_name=''
                        break
                if len(self.sch_name)>2:
                    print(self.sch_name)
                    break
        try:
            if sch_time>=SCHOOLS.max_sch_work_time:
                raise Overtime
            print("THE SCHOOL RUNTIME IS WITHIN THE LIMIT")
            self.sch_time=input("NOW PLEASE ENTER THE SCHOOL TIMINGS:")
            self.sch_time.upper()
        except Overtime:
            print(f"THE MAXIMUM SCHOOL RUNNING TIME SHOULD NOT EXCEED {SCHOOLS.max_sch_work_time} HOURS")
            while(True):
                sch_time=int(input("ENTER VALID RUNTIME:"))
                if sch_time<SCHOOLS.max_sch_work_time:
                    print("THE SCHOOL RUNTIME IS WITHIN THE LIMIT")
                    self.sch_time=input("NOW PLEASE ENTER THE SCHOOL TIMINGS:")
                    self.sch_time.upper()
                    break
        self.no_stands=no_stands
        self.sch_addr=sch_addr.upper()
        self.no_branch=no_branch
        try:
            if sy_board not in SCHOOLS.SY_BOARDS:
                raise Invalidboard
            self.sy_board=sy_board.upper()
        except Invalidboard:
            print("THE FOLLOWING ARE MOSTLY ADAPTED SYLLABUS BOARDS BY THE SCHOOLS")
            for i in SCHOOLS.SY_BOARDS:
                if i!=SCHOOLS.SY_BOARDS[len(SCHOOLS.SY_BOARDS)-1]:
                    print(i,end=',')
                else:
                    print(i)
            while(True):
                Confirm=input("Since You Have Entered An Unknown Board Please Confirm That Do You Still Want To Keep The Same Board(Y/N):")
                Confirm=Confirm.lower()
                if not re.match("^[y&n]",Confirm):
                    print("Error! Only letters Y AND N allowed!")
                    print("INVALID INPUT,CONFIRM AGAIN")
                elif Confirm=='y':                    
                    self.sy_board=sy_board
                    break
                else:
                    print("OK!THEN CHOOSE FROM THE FOLLOWING BOARDS")
                    for i in SCHOOLS.SY_BOARDS:
                        if i!=SCHOOLS.SY_BOARDS[len(SCHOOLS.SY_BOARDS)-1]:
                            print(i,end=',')
                        else:
                            print(i)
                    self.sy_board=input().upper()
                    break
        try:
            if len(str(c_no))!=10:
                raise Invalidcontact
            self.c_no=c_no
        except Invalidcontact:
            print("CONTACT NUMBER CONTAINS ONLY 10DIGITS IN MAXIMUM")
            while(True):
                self.c_no=int(input("ENTER VALID CONTACT:"))
                if len(str(self.c_no))==10:
                    break
        finally:
            print(f"THE {self.sch_name} SCHOOL GENERAL DETAILS ENTRY IS COMPLETED")
        self.standards_list=standards_list
    def sch_details(self):
        print(f"OUR SCHOOL NAME IS {self.sch_name}")
        print(f"THE SCHOOL TIMINGS ARE {self.sch_time}")
        print(f"THE NUMBER OF STANDARDS IN THIS SCHOOL ARE {self.no_stands}")
        print(f"ADDRESS OF THE SCHOOL: {self.sch_addr}")
        print(f"NUMBER OF BRANCHES OF THE SCHOOL ARE {self.no_branch}")
        print(f"THE SYLLABUS ADAPTED BY THE SCHOOL IS {self.sy_board}")
        print(f"CONTACT NUMBER: {self.c_no}")
    def C_YEAR_DET(self):
        print(f"THE CURRENT YEAR INFO OF THE {self.sch_name} SCHOOL IS AS FOLLOWS")
        self.SCHOOL=[]
        self.CY_SCHOOL=[]
        for i in range(1,self.no_stands+1):
            CLASS=[f"CLASS_{int(i)}"]
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
            CLASS=[f"CLASS_{i[0]}",[],[]]
            for j in i[1]:
                CLASS[1].append(j.name)
                CLASS[2].append(j.percent)
            SCHOOL.append(CLASS)
        head=["CLASS NAME","STUDENTS","PERCENTAGES"]
        print(tabulate(SCHOOL,headers=head,tablefmt="rounded_grid"))
    def N_YEAR_DET(self):
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
            if i!=self.CY_SCHOOL[len(self.CY_SCHOOL)-1] and i!=self.CY_SCHOOL[0]:
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
                                STU.append(copy.deepcopy(j))
                if STU!=[]:
                    CLASS.append(STU)
                if N_STU!=[]:
                    N_CLASS.append(N_STU)
                if len(CLASS)>1:
                    self.NY_SCHOOL.append(CLASS)
                if len(N_CLASS)>1:
                    self.NY_SCHOOL.append(N_CLASS)
            if i==self.CY_SCHOOL[len(self.CY_SCHOOL)-1]:
                N_CLASS=[f"CLASS_{int(i[1][0].standard)+1} SCHOOL MIGRATORS" if self.CY_SCHOOL[len(self.CY_SCHOOL)-1]==10 else f"CLASS_{int(i[1][0].standard)+1}"]
                N_STU=[]
                for j in i[1]:
                    if j.percent>75:
                        N_STU.append(copy.deepcopy(j))
                    else:
                        for i in self.NY_SCHOOL:
                            if i[0]==f"CLASS_{j.standard}":
                                i[1].append(copy.deepcopy(j))
                if N_STU!=[]:
                    N_CLASS.append(N_STU)
                if len(N_CLASS)>1:
                    self.NY_SCHOOL.append(N_CLASS)
        for i in self.NY_SCHOOL:
            for j in i[1]:
                if j.percent>75:
                    j.standard=j.standard+1
        N_SCHOOL=[]
        for i in self.NY_SCHOOL:
            CLASS=[f"CLASS_{i[0]}",[],[]]
            for j in i[1]:
                CLASS[1].append(j.name)
                CLASS[2].append(j.percent)
            N_SCHOOL.append(CLASS)
        head=["CLASS NAME","STUDENTS","PERCENTAGES"]
        print(tabulate(N_SCHOOL,headers=head,tablefmt="rounded_grid"))