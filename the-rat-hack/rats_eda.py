
# coding: utf-8

# ## Exploring (flat) rats
# 
# **June 2018**. As part of the Optoro data team's hack day, I took a look at [codefordc/the-rat-hack](https://github.com/codefordc/the-rat-hack) - specifically, the 2016 311 calls relating to rodents.
# 
# The majority of this notebook is just some initial exploratory data analysis, to get a sense of the frequency - for example - of rodent calls versus all 311 calls. I then started looking at time series models for predicting rodents (my prior is that it's very seasonal; more rats during hotter months?).
# 
# The data used in this notebook can be found [here](https://www.dropbox.com/sh/4j7q53lltasez3h/AADzLTkEys24HW_YLqrkWI5ia/single_year?dl=0&preview=dc_311-2016.csv).
# 

# In[220]:


import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import statsmodels.tsa as ts
from matplotlib import pyplot as plt

plt.style.use('bmh')

mpl.rcParams['agg.path.chunksize'] = 10000
mpl.rcParams['figure.figsize'] = (12,8)


# In[221]:


def df_shape(dataframe: pd.DataFrame) -> str:
    """Print the df shape nicely"""
    print(f'rows\t{dataframe.shape[0]:,.0f}')
    print(f'cols\t{dataframe.shape[1]:,.0f}')


# In[222]:


df = pd.read_csv('data/single_year/dc_311-2016.csv')
print(df_shape(df))
df.head()


# In[218]:


(df['SERVICECODEDESCRIPTION'].value_counts() / len(df)).head()


# In[219]:


(df['SERVICECODEDESCRIPTION'].value_counts() / len(df)).tail()


# In[74]:


df[df['SERVICECODE']=='S0311']['SERVICECODEDESCRIPTION'].value_counts()


# In[75]:


rats = df[df['SERVICECODE']=='S0311']
print(df_shape(rats))
rats.head()


# So `S0311` is the service code for rats.

# In[3]:


df.columns


# In[211]:


plt.scatter(df['LONGITUDE'], df['LATITUDE'], s=1, alpha=0.075, label='All 311 calls')
plt.scatter(rats['LONGITUDE'], rats['LATITUDE'], s=3, label='Calls about rats')
plt.legend()
plt.show()


# In[80]:


date_cols = ['SERVICEORDERDATE', 'INSPECTIONDATE', 'RESOLUTIONDATE']
df[date_cols].head()


# In[81]:


for col in date_cols:
    for data in [df, rats]:
        data[col] = pd.to_datetime(data[col])


# In[82]:


df.sort_values(by='SERVICEORDERDATE', inplace=True)
for data in [df, rats]:
    rats['time_to_resolve'] = (rats['RESOLUTIONDATE'] - rats['SERVICEORDERDATE']).dt.days


# In[90]:


plt.plot(df['SERVICEORDERDATE'], df['time_to_resolve'], 'o', alpha=0.3, label='All 311')
plt.plot(rats['SERVICEORDERDATE'], rats['time_to_resolve'], 'o', label='Rats')
plt.legend()
plt.show()


# In[93]:


df['time_to_resolve'].hist(bins=100)
plt.show()


# # Rats per day

# In[101]:


df.head()


# In[181]:


df['date'] = df['SERVICEORDERDATE'].dt.date
rats['date'] = rats['SERVICEORDERDATE'].dt.date
days = df[['date', 'SERVICEREQUESTID']].groupby('date').count().rename(columns={'SERVICEREQUESTID': 'all'})
rat_days = rats[['date', 'SERVICEREQUESTID']].groupby('date').count().rename(columns={'SERVICEREQUESTID': 'rats'})
days = pd.merge(days, rat_days, left_index=True, right_index=True).reset_index()
days.head()


# In[182]:


days.sort_values(by='date', inplace=True)
days['rat_rate'] = days['rats'] / days['all']
days['rat_rate_rolling'] = days['rat_rate'].rolling(7).mean()


# In[183]:


plt.plot(days['date'], days['rat_rate'], label='Raw')
plt.plot(days['date'], days['rat_rate_rolling'], label='Rolling (7 days)')
plt.axhline(days['rat_rate'].mean(), color='gray', label=f'Average: {days["rat_rate"].mean()*100:.0f}%')
plt.title('What % of calls are rat calls?')
plt.legend()
plt.show()


# # Predicting rats 
# 
# `rats = f(season)`
# 
# Data:
# `number of rat calls, number of total calls, date`
# 
# Time series?

# In[144]:


days.head()


# In[151]:


train = days[days['date'] < datetime(2016,8,1).date()][['rat_rate']].copy().as_matrix()
test = days[days['date'] >= datetime(2016,8,1).date()][['rat_rate']].copy().as_matrix()
train.shape, test.shape


# In[187]:


ar_model = ts.ar_model.AR(train)
ar_model_fitted = ar_model.fit()

# Forecasting
preds = ar_model_fitted.predict(start=len(train), end=len(train)+len(test)-1, dynamic=False)
preds_df = pd.DataFrame(preds, index=days.iloc[-len(preds):].index).rename(columns={0: 'preds'})
preds_df.head()


# In[205]:


days_p = pd.merge(days, preds_df, left_index=True, right_index=True)
days_p['preds_ma'] = days_p['preds'].rolling(window=14, center=False).mean()
days_p['rat_rate_ma'] = days_p['rat_rate'].rolling(window=14, center=False).mean()
days_p['rat_rate_std'] = days_p['rat_rate'].rolling(window=14, center=False).std()
days_p.tail()


# In[204]:


days.tail()


# In[209]:


plt.plot(days_p['date'], days_p['rat_rate'], alpha=0.2, color='red')
plt.plot(days_p['date'], days_p['rat_rate_ma'], color='red')
plt.plot(days_p['date'], days_p['rat_rate_std'], color='orange')
plt.plot(days_p['date'], days_p['preds'], alpha=0.2, color='blue')
plt.plot(days_p['date'], days_p['preds_ma'], color='blue')
plt.axhline(days_p['rat_rate'].mean(), color='gray')
plt.title('Terrible fit!')
plt.legend()
plt.show()


# Some reading on time series models (since it's been a looong time): [Seasonal ARIMA with Python](http://www.seanabu.com/2016/03/22/time-series-seasonal-ARIMA-model-in-python/)

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




