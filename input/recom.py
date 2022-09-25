import pandas as pd
import json
import json
with open('../output/project_list.json') as json_file:
    project_list = json.load(json_file)
with open('../output/title_list.json') as json_file:
    title_list = json.load(json_file)    
with open('../output/desc_list.json') as json_file:
    desc_list = json.load(json_file)

all_data_df = pd.read_csv('../output/all_data_fake.csv')
top_click_all_pd = pd.read_csv('../output/top_click_all.csv')
upload_project_fake = pd.read_csv('../output/upload_project.csv')
user_id_ls = top_click_all_pd['uid'].tolist()

import pandas as pd

class dataset_recom(object):
    def __init__(self):
        self.general_list = self.get_general_dataset_list()
        self.category_match = pd.read_csv('../output/project_fake.csv')

    def click_projects(self, uid):
        data = top_click_all_pd[top_click_all_pd['uid']==uid]
        if len(data)==0:
            return []
        uid_click = data.set_index('uid')
        ordered_list = uid_click.loc[uid,'node']
        sequence = []
        for elem in reversed(ordered_list):
            if project_list.get(elem.split('/')[-1]) != None:
                sequence.append(elem)
    
        return sequence
    
    def get_project_list(self, uid):
        # recent click
        history = self.click_projects(uid)[:3]
        history = [int(x.split('/')[-1]) for x in history]
        # publish
        data = upload_project_fake[upload_project_fake['publisher_id']==uid]

        publish_list = list(data['project_id'])
        return list(set(history+publish_list))
    
    def get_match_dataset_list(self, uid):
        project = self.get_project_list(uid)
        df = self.category_match
        dataset_list = set()
        max_threshold = 50

        for elem in project:
            category = df[df['project_id'] == elem]['categories'].values[0]
            if type(category) is str:
                # number of views rank
                fit_data = all_data_df[all_data_df['categories'].isin([category])]
                threshold = min(max_threshold, len(fit_data))
                top_view = fit_data.iloc[:threshold]
                view_list = set()
                for id in top_view.dataset_id:
                    view_list.add(id)
                    
                # number of downloads rank

                #top_downloads = fit_data.sort_values(by='num_download', ascending = False).iloc[:threshold]
                #download_list = set()
                #for id in top_downloads.dataset_id:
                #    download_list.add(id)
                    
                # number of last month view rank

                top_recency = fit_data.sort_values(by='last_month_views', ascending = False).iloc[:threshold]
                recent_list = set()
                for id in top_recency.dataset_id:
                    recent_list.add(id)
                    
                #intersection
                #dataset_list.update(view_list.intersection(download_list, recent_list))
                dataset_list.update(view_list.intersection(recent_list))
        return list(dataset_list)
        
    
    def get_general_dataset_list(self):
        threshold = 10
        #top views
        top_list = set(all_data_df.reset_index(drop=True).loc[:threshold]['dataset_id'])
            
        #top downloads
        #for id in socrata_by_view.sort_values(by='num_download', ascending = False).iloc[:threshold]['dataset_id']:
        #    top_list.add(id)
            
        #top last month views
        for id in all_data_df.sort_values(by='last_month_views', ascending = False).iloc[:threshold]['dataset_id']:
            top_list.add(id)
        
        return list(top_list)
    
    def merge_and_select(self, uid):
        general_list = x.get_general_dataset_list()
        general_filter = []
        for id in all_data_df.dataset_id:
            general_filter.append(id in general_list)
        general_datasets = all_data_df[general_filter]
        general_datasets['general_last_month_view_percentile'] = general_datasets['last_month_views'].rank(pct=True)
        general_datasets = general_datasets.sort_values(by='general_last_month_view_percentile',ascending=False)[['dataset_id', 'general_last_month_view_percentile']]
        general_datasets = general_datasets.reset_index(drop=True)
        #number of last month view


        match_list = x.get_match_dataset_list(uid)
        match_filter = []
        for id in all_data_df.dataset_id:
            match_filter.append(id in match_list)
        match_datasets = all_data_df[match_filter]       
        match_datasets['last_month_view_percentile'] = match_datasets['last_month_views'].rank(pct=True)
        match_datasets = match_datasets.sort_values(by='last_month_view_percentile',ascending=False)[['dataset_id', 'last_month_view_percentile']]
        match_datasets = match_datasets.reset_index(drop=True)

        final_datasets = pd.merge(match_datasets, general_datasets,on='dataset_id',how='outer')

        final_datasets = final_datasets.fillna(0)
        final_datasets['rec_score'] = final_datasets['last_month_view_percentile'] * 0.5 + final_datasets['general_last_month_view_percentile'] * 0.5

        final_datasets = final_datasets.sort_values(by='rec_score',ascending=False)
        final_datasets = final_datasets.reset_index(drop = True)
        return final_datasets
    
    def refresh_all(self, number):
        table = []
        count = 0
        for user in user_id_ls:
            count += 1
            if count%2==0:
                print(user)
            recom = self.merge_and_select(user)
            for dataset in recom.dataset_id[:number]:
                table.append({'uid': user, 'dataset_id': dataset, 'rec_score':recom[recom['dataset_id']==dataset]['rec_score'].values[0]})
        df = pd.DataFrame(table)
        df_output = df.merge(all_data_df[['dataset_id', 'title','last_month_views','link']], how='left')
        #engine = create_engine('mysql+mysqlconnector://grmds_analyst:Cmethods1@54.189.68.146/grmds054_drup881',echo=False)
        #df.to_sql(name='dr_recom_socrata_dataset_to_user', con=engine, if_exists = 'replace', index=False)
        return df_output
        
    

#if __name__ == "__main__":
#    x = dataset_recom()
#    data = x.refresh_all()
        
    

#if __name__ == "__main__":
#    x = dataset_recom()
#    data = x.refresh_all()

x = dataset_recom()

recom_table = x.refresh_all(20)
recom_table.to_csv('../output/dataset_recommendation.csv',index=False)