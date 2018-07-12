
# coding: utf-8

# In[16]:


import pandas as pd
import numpy as np


# In[62]:


from datetime import datetime, timedelta
import requests
import pdftables_api
import glob


# # 1) Get PDF

# In[ ]:


# This part of the code goes to the site and gets all pdfs that were posted on the site in the past 800 days(approx 2 years). 
#If we want to go further back, just change the num_days_to_go_behind variable and run again


# In[358]:


default_url = 'https://doc.dc.gov/sites/default/files/dc/sites/doc/publication/attachments/'
initial_start_date = datetime.now().date() - timedelta(days=12)
initial_end_date = datetime.now().date() - timedelta(days=6)
num_days_to_go_behind = 800

for i in np.arange(1, num_days_to_go_behind):
    
    start_date =  initial_start_date - (i*timedelta(days=1))
    end_date = initial_end_date -  (i*timedelta(days=1))
    
    start_month = start_date.strftime('%B')
    end_month = end_date.strftime('%B')
    
    custom_url = default_url + str(start_month) + '%20'+ str(start_date.day) + '%20through%20'                   + str(end_month) + '%20' + str(end_date.day) + '%202018.pdf'
    
    r = requests.get(url=custom_url)
    if r.status_code == 200:
        filename = 'weekly_corrections_data/pdf/corrections_data' + str(start_date) + '_' + str(end_date) +  '_.pdf'
        with open(filename, 'wb') as infile:
            infile.write(r.content)
'Number of files written = '+str(i)


# # 2) Convert to Excel

# In[361]:


#Go to https://pdftables.com/pdf-to-excel-api and create a token as shown on the site. 
#Go to https://github.com/pdftables/python-pdftables-api and see how the api can be used to convert pdf to excel
pdftables = pdftables_api.Client('insert token here', timeout=(60, 3600))


# In[381]:


for file in glob.glob("weekly_corrections_data/pdf/*.pdf"):
    out_file = file.replace('pdf', 'excel').replace('.excel', '.xlsx')
    pdftables.xlsx(file, out_file)


# # 3) Read Excel

# In[7]:


def read_excel(file):
    xl = pd.ExcelFile(file)
    xl.sheet_names
    df = pd.read_excel(xl, 'Page 1', header=1)
    return df


# # 4) Clean and Write it to csv

# In[31]:


def get_gender(x):
    if 'Male' in x:
        return 'Male'
    elif 'Female' in x:
        return 'Female'
    else:
        return None
    return x

def clean_file(df):
    if 'Indicator' not in df.columns:
        df[['Indicator', 'SEX']] = pd.DataFrame(df['Indicator SEX'].fillna('-').str.split(' ',1).tolist(),
                                   columns = ['Indicator','SEX'])
    else:
        df['Indicator'] = df.Indicator.fillna('-')
    
    df['Location'] = df.Location.fillna('-')
    df.columns = [col.replace('\n', '_') for col in df.columns]
    df = df[~df.Indicator.str.contains('Total')].reset_index(drop=True).copy()
    df = df[~df.Location.str.contains('Total')].reset_index(drop=True).copy()

    df['gender'] = df.Indicator.apply(lambda x: get_gender(x), 1)
    df.loc[(df.SEX.isnull() & (df.gender.notnull())), 'SEX'] = df.gender
    df.drop(['gender'], 1, inplace=True)
    return df


# # 5) Reshaping dataframe

# In[9]:


def reshape_dataframe(df):
    
    df_reshape = pd.melt(df, id_vars=["Location", "Indicator", "SEX", "Operating_Capacity"], 
                      var_name="date_day", value_name="num_people").reset_index(drop=True).copy()
    df_reshape['date'] = df_reshape.date_day.apply(lambda x: x.split('_')[0])
    df_reshape['Location'] = df_reshape.Location.replace('-', np.nan).ffill()
    df_reshape['Operating_Capacity'] = df_reshape.Operating_Capacity.fillna('-')
    
    return df_reshape


# ## 6) Write to csv

# In[56]:


def write_csv(df_reshape, file):
    outfile = file.replace('.xlsx', '').replace('excel', 'csv')
    filename = outfile + '_' + str(df_reshape.date.min()).replace('/', '-') + '_' + str(df_reshape.date.max()).replace('/', '-') + '.csv'
    df_reshape.to_csv(filename , sep=',')


# # 7) Calling All functions

# In[57]:


i = 1
for file in glob.glob("weekly_corrections_data/excel/*.xlsx"):
    df = read_excel(file)
    df = clean_file(df)
    df_reshape = reshape_dataframe(df)
    write_csv(df_reshape, file)
    i = i + 1

