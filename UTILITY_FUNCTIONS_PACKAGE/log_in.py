import json
from UTILITY_FUNCTIONS_PACKAGE import log_out
def log_in_fun(name,role,password,readfile,writefile):
    name=name.upper()
    role=role.upper()
#     stu_login_id = 0
#     teach_login_id = 0 
#     sch_login_id = 0
    with open(f"UTILITY_FUNCTIONS_PACKAGE/{readfile}","r") as f1:
        user_accounts = json.load(f1)
    stu_user_accounts = user_accounts.get('stu_user_accounts')
    teach_user_accounts = user_accounts.get('teach_user_accounts')
    sch_user_accounts = user_accounts.get('sch_user_accounts')
    with open(f"UTILITY_FUNCTIONS_PACKAGE/{writefile}","r") as f2:
            user_logins = json.load(f2)
    stu_log_in=user_logins.get('stu_log_in')
    teach_log_in=user_logins.get('teach_log_in')
    sch_log_in=user_logins.get('sch_log_in')
    if role=='STUDENT':
                if name in stu_user_accounts:
                        if password in stu_user_accounts[name]:
                                for i in stu_user_accounts[name]:
                                        if i == password:
                                                # stu_login_id = stu_login_id+1
                                                INDEX = stu_user_accounts[name].index(password)
                                                stu_log_in[name][INDEX][0] = True
                                                # stu_log_in[name][INDEX].append(stu_login_id)
                                                # login_id = stu_login_id
                                                print("You Have Successfully LoggedIn as a STUDENT")
                                                break
                        else:                                        
                                print("INCORRECT LOGIN CREDENTIALS")
                else:
                        print("INCORRECT LOGIN CREDENTIALS")
    elif role=='TEACHER':                             
                if name in teach_user_accounts:
                        if password in teach_user_accounts[name]:
                                for i in teach_user_accounts[name]:
                                        if i == password:
                                                # teach_login_id = teach_login_id+1
                                                INDEX = teach_user_accounts[name].index(password)
                                                teach_log_in[name][INDEX][0] = True
                                                # teach_log_in[name][INDEX].append(teach_login_id)
                                                # login_id = teach_login_id
                                                print("You Have Successfully LoggedIn as a STUDENT")
                                                break
                        else:                                        
                                print("INCORRECT LOGIN CREDENTIALS")
                else:
                        print("INCORRECT LOGIN CREDENTIALS")
    elif role=='SCHOOL':                    
            if name in sch_user_accounts:                        
                        if password in sch_user_accounts[name]:
                                for i in sch_user_accounts[name]:
                                        if i == password:
                                                # sch_login_id = sch_login_id+1
                                                INDEX = sch_user_accounts[name].index(password)
                                                sch_log_in[name][INDEX][0] = True
                                                # sch_log_in[name][INDEX].append(sch_login_id)
                                                # login_id = sch_login_id
                                                print("You Have Successfully LoggedIn as a STUDENT")
                                                break
                        else:                                                                      
                                print("INCORRECT LOGIN CREDENTIALS")                                
            else:                        
                        print("INCORRECT LOGIN CREDENTIALS")
    else:
            print("INVALID ROLE")
    data_to_write={'stu_log_in':stu_log_in,
                   'teach_log_in':teach_log_in,
                   'sch_log_in':sch_log_in}
    with open(f"UTILITY_FUNCTIONS_PACKAGE/{writefile}","w") as f3:
        json.dump(data_to_write,f3,indent=4)
        f2.close()
    while(True):
        command = input('IF YOU WORK IS DONE PLEASE TYPE "LOGOUT" TO GET LOGOUT SAFELY')
        command = command.lower()
        if command == "logout":            
                log_out.log_out_fun(role,writefile)
                break
        else:
                print('PLEASE TYPE "LOGOUT" ONLY')