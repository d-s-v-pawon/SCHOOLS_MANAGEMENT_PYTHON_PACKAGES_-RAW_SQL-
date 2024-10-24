import json
def log_out_fun(role,login_file):
    

    with open(f"UTILITY_FUNCTIONS_PACKAGE/{login_file}","r") as f1:
            user_logins = json.load(f1)
    stu_log_in=user_logins.get('stu_log_in')
    teach_log_in=user_logins.get('teach_log_in')
    sch_log_in=user_logins.get('sch_log_in')


    if role=='STUDENT':
            for i in stu_log_in:
                    for j in stu_log_in[i]:                                                                
                        #     for k in j:
                                # if k == login_id:
                                #         j[0] = False
                                #         j.remove(k)
                                if j[0] == True:                                        
                                        j[0] = False
                                        print('YOU HAVE SUCCESSFULLY "LOGGED-OUT"')
                                        break
                    
    elif role=='TEACHER':
                for i in teach_log_in:
                    for j in teach_log_in[i]:                                        
                                        if j[0] == True:                                        
                                                j[0] = False
                                                print('YOU HAVE SUCCESSFULLY "LOGGED-OUT"')
                                                break
                                        
                        #     for k in j:
                        #         if k == login_id:
                        #                 j[0] = False
                        #                 j.remove(k)

    elif role=='SCHOOL':
            for i in sch_log_in:
                    for j in sch_log_in[i]:
                            if j[0] == True:                                                                                                                     
                                        j[0] = False
                                        print('YOU HAVE SUCCESSFULLY "LOGGED-OUT"')
                                        break
                        #     for k in j:
                        #         if k == login_id:
                        #                 j[0] = False
                        #                 j.remove(k)

    data_to_write={'stu_log_in':stu_log_in,
                   'teach_log_in':teach_log_in,
                   'sch_log_in':sch_log_in}
    
    with open(f"UTILITY_FUNCTIONS_PACKAGE/{login_file}","w") as f2:
        json.dump(data_to_write,f2,indent=4)