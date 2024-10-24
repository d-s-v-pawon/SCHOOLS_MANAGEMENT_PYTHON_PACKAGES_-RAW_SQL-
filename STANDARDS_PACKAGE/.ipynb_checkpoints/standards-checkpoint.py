import re
import random
import copy
from tabulate import tabulate
import string
class STANDARDS:
    standards=[]
    sub_num=[5,6]
    max_att_per=100
    max_sch_time_high=10
    max_sch_time_pri=7
    def __init__(self,name,no_subjects,min_att_per,max_cap,max_sch_time,stu_list):
        for i in stu_list:
            if i.standard not in STANDARDS.standards:
                STANDARDS.standards.append(i.standard)
        STANDARDS.standards.sort()
        class noclass(Exception):
            pass
        class Invalidnum(Exception):
            pass
        class Overatt(Exception):
            pass
        class Overtime(Exception):
            pass
        try:
            if name not in self.standards:
                raise noclass
            self.name=name
        except noclass:
            print(f"NO STUDENTS DETAILS ENTERED FOR THE CLASS {name}")
            print("TRY FOR ANOTHER CLASS")        
        else:
            try:
                if self.name<=5:
                    if no_subjects!=STANDARDS.sub_num[0]:
                        raise Invalidnum
                else:
                    if no_subjects!=STANDARDS.sub_num[1]:
                        raise Invalidnum
                self.no_subjects=no_subjects
            except Invalidnum:
                print("THE PRIMARY CLASS STUDENTS CONTAINS FIVE SUBJECTS AND HIGHER STUDENTS HAVE SIX")
                if self.name<=5:
                    while(True):
                        self.no_subjects=int(input("ENTER VALID NUMBER OF SUBJECTS:"))
                        if self.no_subjects==STANDARDS.sub_num[0]:
                            break
                else:
                    while(True):
                        self.no_subjects=int(input("ENTER VALID NUMBER OF SUBJECTS:"))
                        if self.no_subjects==STANDARDS.sub_num[1]:
                            break
            try:
                if min_att_per>=STANDARDS.max_att_per:
                    raise Overatt
                self.min_att_per=min_att_per         #MINIMUM ATTENDANCE PERCENTAGE
            except Overatt:
                print("THE MINIMUM ATTENDANCE PERCENT FOR A STUDENT IN A YEAR SHOULD NOT BE 100 OR ABOVE PERCENT")
                while(True):
                    self.min_att_per=int(input("ENTER THE ACCEPTABLE MINIMUM ATTENDANCE PERCENT:"))
                    if self.min_att_per<STANDARDS.max_att_per:
                        break
            self.max_cap=max_cap
            try:
                if self.name<=5:
                    if max_sch_time>=STANDARDS.max_sch_time_pri:
                        raise Overtime
                else:
                    if max_sch_time>=STANDARDS.max_sch_time_high:
                        raise Overtime
                self.max_sch_time=max_sch_time         #MAXIMUM TIME TO SPEND IN ANY SCHOOL FOR THE CLASS STUDENTS
            except Overtime:
                if self.name<=5:
                    print(f"THE PRIMARY STUDENT MAXIMUM SCHOOL TIME SHOULD BE LESS THAN {STANDARDS.max_sch_time_pri} HOURS")
                    while(True):
                        self.max_sch_time=int(input("ENTER THE SCHOOL TIME BELOW MAX_TIME:"))
                        if self.max_sch_time<STANDARDS.max_sch_time_pri:
                            break
                else:
                    print(f"THE HIGHER STUDENT MAXIMUM SCHOOL TIME SHOUULD BE LESS THAN {STANDARDS.max_sch_time_high} HOURS")
                    while(True):
                        self.max_sch_time=int(input("ENTER THE SCHOOL TIME BELOW MAX_TIME:"))
                        if self.max_sch_time<STANDARDS.max_sch_time_high:
                            break
            finally:
                print(f"THE CLASS {self.name} GENERAL DETAILS ENTRY IS COMPLETED")
            self.stu_list=stu_list
    def cls_details(self):
        print(f"THE DETAILS OF CLASS{self.name} ARE AS FOLLOWS:")
        print(f"THIS IS CLASS {self.name}")
        print(f"NUMBER OF SUBJECTS FOR THIS CLASS STUDENTS ARE {self.no_subjects}")
        print(f"MINIMUM ATTENDANCE PERCENTAGE REQUIRED FOR THIS CLASS STUDENTS IS {self.min_att_per}%")
        print(f"THE NUMBER OF STUDENTS IN THIS CLASS INCLUDING ALL SECTIONS SHOULD NOT EXCEED {self.max_cap} STUDENTS")
        print(f"THE STUDENTS SHOULD SPEND ONLY {self.max_sch_time} HOURS TIME IN THE SCHOOL")
    def cls_students(self):
        self.CLASS=[]
        for i in self.stu_list:
            if i.standard==self.name:
                self.CLASS.append(i)
        print(f"STUDENTS OF THE CLASS {self.name} ARE AS FOLLOWS")
        for i in self.CLASS:            
            print(i.name,end=' ')
            print(i.section)
        self.stu_list=self.CLASS
    def PERIODS(self):
        if self.name<=5:
            print(f"THE SCHOOL TIME FOR PRIMARY STUDENTS IS {self.max_sch_time} HOURS")
            print("FIVE GENERAL PERIODS FOR FIVE SUBJECTS")
            print("EACH PERIOD SHOULD BE OF 40 MIN ONLY")
            print(f"THREE PERIODS SHOULD BE FOR PLAYTIME WITHIN {self.max_sch_time} HOURS OF 45MIN EACH")
            print(f"IF TIME LEFT,THE REMAINING TIME OF {self.max_sch_time} HOURS SHOULD BE USED ACCORDINGLY")
        elif(self.name<=7):
            print(f"THE SCHOOL TIME FOR UPPER PRIMARY STUDENTS IS {self.max_sch_time} HOURS")
            print("SIX GENERAL PERIODS FOR SIX SUBJECTS")
            print("EACH PERIOD SHOULD BE OF 45 MIN ONLY")
            print(f"TWO PERIODS SHOULD BE FOR PLAYTIME WITHIN {self.max_sch_time} HOURS OF 45MIN EACH")
            print(f"IF TIME LEFT,THE REMAINING TIME OF {self.max_sch_time} HOURS SHOULD BE USED ACCORDINGLY")
        else:
            print(f"THE SCHOOL TIME FOR HIGHER STUDENTS IS {self.max_sch_time} HOURS")
            print("EIGHT GENERAL PERIODS FOR SIX SUBJECTS")
            print("EACH PERIOD SHOULD BE OF 45 MIN ONLY")
            print(f"ONE PERIOD SHOULD BE FOR PLAYTIME WITHIN {self.max_sch_time} HOURS OF 1HOUR")
            print(f"IF TIME LEFT,THE REMAINING TIME OF {self.max_sch_time} HOURS SHOULD BE USED ACCORDINGLY")