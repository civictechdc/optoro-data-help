
# coding: utf-8

# In[4]:


get_ipython().system('pip install tabula-py')


# In[28]:


get_ipython().system('pip install pygeocoder')


# In[6]:


get_ipython().system('ls')


# In[2]:


from tabula import read_pdf
from pygeocoder import Geocoder


# In[5]:


page_one_data = read_pdf('../Vacant Buildings  as of February 7 2018.pdf')


# In[6]:


# manually confirmed that page 1 has 42 rows plus header
# another one I checked has 43
page_one_data.shape


# In[7]:


# the file is 23 pages
42*23


# In[8]:


all_data = read_pdf('../Vacant Buildings  as of February 7 2018.pdf', pages='all')


# In[9]:


# 981 seems about right
all_data.shape


# In[10]:


all_data.head().T


# In[11]:


all_data.columns = [c.replace(' ', '_').lower() for c in all_data.columns]


# In[12]:


all_data.ward.value_counts()


# In[16]:


all_data = all_data[all_data.ward != 'WARD']


# In[17]:


all_data.shape


# # Let's Geocode these Addresses
# 
# Good intro at https://chrisalbon.com/python/data_wrangling/geocoding_and_reverse_geocoding/
