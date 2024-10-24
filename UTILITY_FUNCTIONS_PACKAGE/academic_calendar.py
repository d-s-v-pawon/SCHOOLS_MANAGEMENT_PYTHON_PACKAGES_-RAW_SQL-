
from tabulate import tabulate

CAL=[[],[],[]]      #List of the lists of months their respective working days and holidays

def academic_calendar_fun(start_year,end_year):
    import random
    import calendar
    print(f"THE ACADEMIC CALENDAR FOR THE YEAR JUNE {start_year} - APRIL {end_year}")
    list_of_months = list(calendar.month_name)[1:]   # Get a list of month names using the calendar module & Exclude the empty string at index 0
    for i in list_of_months:
        if i in list(calendar.month_name)[1:6]:
            CAL[0].append(f"{i} {end_year}")
        else:
            CAL[0].append(f"{i} {start_year}")


    def sorting_year(month):        
        if month in [f"June {start_year}", f"July {start_year}", f"August {start_year}", f"September {start_year}", f"October {start_year}", f"November {start_year}", f"December {start_year}"]:
            return CAL[0].index(month)
        else:
            return CAL[0].index(month) + 7

    CAL[0] = sorted(CAL[0], key=sorting_year)

    for i in range(1,13):
        while(True):
            working_days = random.randint(17,22)
            if CAL[1].count(working_days)<2:
                CAL[1].append(working_days)
                break

    for i in CAL[0]:
        if i in list(calendar.month_name)[1:6]:
            year = end_year
        else:
            year = start_year
        for j in CAL[1]:
            if i in [f"list_of_months[0] {year}",f"list_of_months[2] {year}",f"list_of_months[4] {year}",f"list_of_months[6] {year}",f"list_of_months[7] {year}",f"list_of_months[9] {year}",f"list_of_months[11] {year}"]:
                tot_work_days = 31
                holidays = tot_work_days - j
                CAL[2].append(holidays)
            elif i==list_of_months[1]:
                if calendar.isleap(end_year):
                    tot_work_days = 29
                else:
                    tot_work_days = 28
                holidays = tot_work_days - j
                CAL[2].append(holidays)
            else:
                tot_work_days = 30
                holidays = tot_work_days - j
                CAL[2].append(holidays)

    data = list(zip(CAL[0],CAL[1],CAL[2]))

    head=["ACADEMIC MONTH","WORKING_DAYS","HOLIDAYS"]
    print(tabulate(data,headers=head,tablefmt="rounded_grid"))

    