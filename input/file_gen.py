#project_list_ori
import random
import json
import pandas as pd
with open('project_features.json') as json_file:
    temp_project_dic = json.load(json_file)
project_features = pd.DataFrame(temp_project_dic)
pro_cate_ls = []
pro_cate_type = ['economy','environment','education','social services','finance','politics','health']
for i in range (200):
    temp = random.choice(pro_cate_type)
    pro_cate_ls.append(temp)
project = project_features[['index','title']]
project.columns = [['project_id','title']]
project['categories'] = pro_cate_ls
project.to_csv('../output/project_fake.csv',index = False)
#project_title_ls = project_features['title'].to_list

project_id_list = project_features['index'].values.tolist()

publisher_id = []
for i in range(200):
    publisher_id.append(random.randrange(1, 40000))
#upload_project = project_features['index']
#upload_project = project_features[['index']].copy()
upload_project_fake = pd.DataFrame(project_id_list)
upload_project_fake['publisher_id'] = publisher_id
upload_project_fake.columns = ['project_id','publisher_id']
upload_project_fake.to_csv('../output/upload_project.csv',index=False)

project_tf = []
for i in range (200):
    project_tf.append("True")
project_list_fake = dict(zip(project_id_list, project_tf))

project_list_fake_js = json.dumps(project_list_fake)
f = open("../output/project_list.json","w")
f.write(project_list_fake_js)
f.close()