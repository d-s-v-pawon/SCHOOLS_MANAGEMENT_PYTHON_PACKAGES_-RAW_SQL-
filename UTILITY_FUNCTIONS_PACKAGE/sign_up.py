import re
import json
def sign_up_fun(name,role,password,filename1,filename2):        
        name=name.upper()
        role=role.upper()
        with open(f"UTILITY_FUNCTIONS_PACKAGE/{filename1}","r") as f1:
            user_accounts = json.load(f1)
        stu_user_accounts = user_accounts.get('stu_user_accounts')
        teach_user_accounts = user_accounts.get('teach_user_accounts')
        sch_user_accounts = user_accounts.get('sch_user_accounts')
        with open(f"UTILITY_FUNCTIONS_PACKAGE/{filename2}","r") as f2:
            user_logins = json.load(f2)
        stu_log_in=user_logins.get('stu_log_in')
        teach_log_in=user_logins.get('teach_log_in')
        sch_log_in=user_logins.get('sch_log_in')
        if len(password) < 8 and ' ' not in password:
            return False
        elif not re.search(r'[a-z]', password):
            return False
        elif not re.search(r'[A-Z]', password):
            return False
        elif not re.search(r'\d', password):
            return False
        elif name == password:
            return False
        else:
            if role=='STUDENT':
                if name in stu_user_accounts.keys():
                    if password not in stu_user_accounts[name]:
                        stu_user_accounts[name].append(password)
                        stu_log_in[name].append([False])
                        print(f"THE {role} ACCOUNT FOR {name} IS CREATED SUCCESSFULLY")
                    else:
                        print("USER_ALREADY EXISTS OR INVALID ROLE")
                elif name not in stu_user_accounts.keys():
                    passwords = []
                    passwords.append(password)
                    stu_user_accounts[name] = passwords
                    logins = [[]]
                    logins[0].append(False)
                    stu_log_in[name] = logins
                    print(f"THE {role} ACCOUNT FOR {name} IS CREATED SUCCESSFULLY")
            elif role=='TEACHER':
                if name in teach_user_accounts.keys():
                    if password not in teach_user_accounts[name]:
                        teach_user_accounts[name].append(password)
                        teach_log_in[name].append("False")
                        print(f"THE {role} ACCOUNT FOR {name} IS CREATED SUCCESSFULLY")
                    else:
                        print("USER_ALREADY EXISTS OR INVALID ROLE")
                elif name not in teach_user_accounts.keys():
                    passwords = []
                    passwords.append(password)
                    teach_user_accounts[name] = passwords
                    logins = []
                    logins.append("False")
                    teach_log_in[name] = logins
                    print(f"THE {role} ACCOUNT FOR {name} IS CREATED SUCCESSFULLY")
            elif role=='SCHOOL':
                if name in sch_user_accounts.keys():
                    if password not in sch_user_accounts[name]:
                        sch_user_accounts[name].append(password)
                        sch_log_in[name].append("False")
                        print(f"THE {role} ACCOUNT FOR {name} SCHOOL IS CREATED SUCCESSFULLY")
                    else:
                        print("USER_ALREADY EXISTS OR INVALID ROLE")
                elif name not in sch_user_accounts.keys():
                    passwords = []
                    passwords.append(password)
                    sch_user_accounts[name] = passwords
                    logins = []
                    logins.append("False")
                    sch_log_in[name] = logins
                    print(f"THE {role} ACCOUNT FOR {name} SCHOOL IS CREATED SUCCESSFULLY")
            else:
                print("USER_ALREADY EXISTS OR INVALID ROLE")
        data_to_write={"stu_user_accounts":stu_user_accounts,
                       "teach_user_accounts":teach_user_accounts,
                       "sch_user_accounts":sch_user_accounts}
        with open(f"UTILITY_FUNCTIONS_PACKAGE/{filename1}","w") as f3:
            json.dump(data_to_write,f3,indent=4)
        data_to_write={"stu_log_in":stu_log_in,
                       "teach_log_in":teach_log_in,
                       "sch_log_in":sch_log_in}
        with open(f"UTILITY_FUNCTIONS_PACKAGE/{filename2}","w") as f4:
            json.dump(data_to_write,f4,indent=4)