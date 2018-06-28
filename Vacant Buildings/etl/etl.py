
# coding: utf-8

# In[4]:


get_ipython().system('pip install tabula-py')


# In[28]:


get_ipython().system('pip install pygeocoder')


# In[6]:


get_ipython().system('ls')


# In[18]:


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

# In[26]:


result = Geocoder.geocode("1600 amphiteather parkway, mountain view, CA 94043")


# In[27]:


result.latitude, result.longitude, result.valid_address


# In[32]:


all_data.dtypes


# In[33]:


' '.join(['a', 'b'])


# In[37]:


all_data['address_full'] = all_data.apply(lambda x: ' '.join([x['street_number'], x['street_type'], x['quadrant'], 'Washington, DC'], axis=1))


# In[44]:


all_data['address_full'] = all_data.apply(lambda x: x['street_number'] + ' ' + x['street_name'] + ' ' + x['street_type'] + ' ' + x['quadrant'] + ' ' + 'Washington, DC', axis=1)


# In[48]:


all_data['geocode_object'] = all_data.address_full.apply(Geocoder.geocode)


# In[47]:


Geocoder.geocode('2002 11TH ST NW Washington, DC').valid_address

