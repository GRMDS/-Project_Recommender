import random
import pandas as pd
import numpy as np

project_num_list = []
while len(project_num_list) < 1000:
    index = random.randint(0,20000)
    if index not in project_num_list: 
        project_num_list.append(index)
random.shuffle(project_num_list)
project_list_ori = project_num_list.copy()
user_id_ls =random.sample(range(1,2000), 1000)
#user_id =  [x for item in user_id_ls for x in repeat(item, 50)]
user_id_ls.sort()

#assume the first one is used repeatly 35 times
for i in range (35):
    project_num_list.append(project_num_list[0])
#assume the second,third one is used repeatly 25 times
for i in range (25):
    project_num_list.append(project_num_list[1])
    project_num_list.append(project_num_list[2])
#assume the forth one is used repeatly 16 times
for i in range (16):
    project_num_list.append(project_num_list[3])
#assume the fifth one is used repeatly 8 times
for i in range (8):
    project_num_list.append(project_num_list[4])
#assume the sixth one is used repeatly 6 times
for i in range (6):
    project_num_list.append(project_num_list[5])
#assume the 7~14 one is used repeatly 3 times
for i in range (3):
    project_num_list.append(project_num_list[6])
    project_num_list.append(project_num_list[7])
    project_num_list.append(project_num_list[8])
    project_num_list.append(project_num_list[9])
    project_num_list.append(project_num_list[10])
    project_num_list.append(project_num_list[11])
    project_num_list.append(project_num_list[12])
    project_num_list.append(project_num_list[13])
    project_num_list.append(project_num_list[14])
#assume the 14~24 one is used repeatly 2 times
for i in range (2):
    project_num_list.append(project_num_list[15])
    project_num_list.append(project_num_list[16])
    project_num_list.append(project_num_list[17])
    project_num_list.append(project_num_list[18])
    project_num_list.append(project_num_list[19])
    project_num_list.append(project_num_list[20])
    project_num_list.append(project_num_list[21])
    project_num_list.append(project_num_list[22])
    project_num_list.append(project_num_list[23])
    project_num_list.append(project_num_list[24])
random.seed(10)

#determine how many dataset used by each user
project_number_list = ['None'] * len(user_id_ls)
# 7% of users have 1 project. 7%*1000 = 70
for i in range(70):
    project_number_list[i] = 1
# 3% of users have 2 project. 3%*1000 = 30
for i in range(70,100):
    project_number_list[i] = 2
# 1% of users have 3 project. 1%*1000 = 10
for i in range(100,110):
    project_number_list[i] = 3
# 1% of users have 4 project. 1%*1000 = 10
for i in range(110,120):
    project_number_list[i] = 4
#5~11 projects only 1 person
for i in range(120,124):
    project_number_list[i] = i-115
for i in range(len(project_number_list)):
    if project_number_list[i] == 'None':
        project_number_list[i] = 0
random.shuffle(project_number_list)
len(project_number_list)
uid_project_id_match = []
for i in range(len(user_id_ls)):
    uid_project_id_match.append(np.random.choice(project_num_list, project_number_list[i], replace=False).tolist())
node = []
for i in range(len(uid_project_id_match)):
    node_each = "["
    if len(uid_project_id_match[i]) == 0:
        node_each += "]"
    else:
        for j in range (len(uid_project_id_match[i])-1):
            node_each += "'/node/"
            node_each += str(uid_project_id_match[i][j])
            node_each += "',"
        node_each += "'/node/"
        node_each += str(uid_project_id_match[i][len(uid_project_id_match[i])-1])
        node_each += "']"
    node.append(node_each)
top_click_all_pd = pd.DataFrame(user_id_ls, columns = ['uid'])
top_click_all_pd['node'] = node
top_click_all_pd.to_csv('../output/top_click_all.csv',index=False)  
