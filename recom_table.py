# total view
import random
import math
import json
import pandas as pd
import numpy as np

with open('title_list.json') as json_file:
    title_list = json.load(json_file)
with open('desc_list.json') as json_file:
    desc_list = json.load(json_file)

view_ls = []
for i in range (2000):
    temp = random.randint(2000, 100000)
    temp = float(temp)
    view_ls.append(temp)
for j in range(700):
    view_ls.append(float('nan'))
random.shuffle(view_ls)

#last_month_view
last_month_ls = []
for i in range (len(view_ls)):
    if math.isnan(view_ls[i]):
        temp = random.randint(0, 10000)
        last_month_ls.append(temp)
    else:
        temp = random.randint(0, view_ls[i])
        last_month_ls.append(temp)

#num_download
num_download = []
for i in range (len(view_ls)):
    if math.isnan(view_ls[i]):
        temp = float('nan')
        num_download.append(temp)
    else:
        temp = float(random.randint(0, view_ls[i]))
        num_download.append(temp)

#data_source
source_type = ['portal','uae','socrata']
source_ls = []
for i in range (2000):
    temp = random.choice(source_type)
    source_ls.append(temp)
#source_ls

#url
import string
url_ls = ['na'] * 2000
letters = string.ascii_lowercase
for i in range (len(source_ls)):
    if source_ls[i] == 'portal':
        temp = random.randint(1,20000)
        url_ls[i] = 'https://grmds.org/node/'+str(temp)
    if source_ls[i] == 'uae':
        temp = title_list[i].replace(' ', '_')
        url_ls[i] = 'https://data.abudhabi/dataset/'+str(temp)
    if source_ls[i] == 'socrata':
        temp = ''.join(random.choice(letters) for i in range(6))
        url_ls[i] = 'https://data.cityofchicago.org/d/'+temp
#url_ls

#categories
cate_ls = []
cate_type = [float('nan'),'economy','environment','education','social services','finance','politics','health']
for i in range (2000):
    temp = random.choice(cate_type)
    cate_ls.append(temp)
#cate_ls

#domain
domain_ls = []
dommain_type = [float('nan'),'data.cityofnewyork.us','data.cityofchicago.org','data.sfgov.org','data.seattle.gov']
for i in range (2000):
    temp = random.choice(dommain_type)
    domain_ls.append(temp)
#domain_ls

#create_time
from random import randrange
from datetime import timedelta
def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

from datetime import datetime
d1 = datetime.strptime('1/1/2020 1:30 PM', '%m/%d/%Y %I:%M %p')
d2 = datetime.strptime('1/1/2022 4:50 AM', '%m/%d/%Y %I:%M %p')
create_time = []
create_time_formate = []
for i in range (2000):
    temp = random_date(d1, d2)
    create_time_formate.append(temp)
    temp = temp.strftime('%Y-%m-%d %I:%M:%S')
    create_time.append(temp)

update_time = []
for i in range (2000):
    temp = random_date(create_time_formate[i], d2)
    temp = temp.strftime('%Y-%m-%d %I:%M:%S')
    update_time.append(temp)

#uae_publisher
uae_pub_ls = []
uae_pub_type = ['Open-source portal','Federal competitiveness and statistics authority','Abu Dhabi Agriculture and Food Safety Authority','Statistics Centre Abu Dhabi','Ministry Of Economy','Ministry of Climate Change & Environment','Department of Economic Development','Federal Customs Authority']
for i in range (2000):
    if source_ls[i] == 'uae':
        temp = random.choice(uae_pub_type)
        uae_pub_ls.append(temp)
    else:
        uae_pub_ls.append('')

all_data_df = pd.DataFrame(list(zip(title_list, desc_list, view_ls,last_month_ls,num_download,url_ls,cate_ls,domain_ls,update_time,create_time,source_ls,uae_pub_ls)),
               columns =['title', 'description','total_views','last_month_views','num_download','link','categories','domain','update_time','create_time','data_source','uae_publisher'])

all_data_df['dataset_id'] = range(1, len(all_data_df) + 1)
all_data_df["publisher_id"] = ""
all_data_df["file_type"] = ""
all_data_df.to_csv("all_data_fake.csv")

