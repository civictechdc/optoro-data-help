
# coding: utf-8

# # Summary
# 
# This script ingests pdfs of DC's vacant buildings data (e.g. https://dcra.dc.gov/sites/default/files/dc/sites/dcra/publication/attachments/Vacant%20Buildings%20%20as%20of%20February%207%202018.pdf) and gets it into a readable CSV format. We also dumped it into a google map as a demo (https://drive.google.com/open?id=15QCg36tt1y3aqp52yoeAliOwxRtiUjkh&usp=sharing).
# 
# This was a prety straightforward ETL using tabula (https://blog.chezo.uno/tabula-py-extract-table-from-pdf-into-python-dataframe-6c7acfa5f302. We then did some manual cleanup, some of which is generic and some is custom to this version of the file.

# # Load and Standardize File

# In[5]:


from tabula import read_pdf # tabula-py==1.2.0
import pandas as pd # pandas==0.20.2


# In[6]:


page_one_data = read_pdf('../Vacant Buildings  as of February 7 2018.pdf')


# In[7]:


# Manually confirmed that page 1 has 42 rows plus header
# Some pages have 43 plus header ¯\_(ツ)_/¯
page_one_data.shape


# In[9]:


all_data = read_pdf('../Vacant Buildings  as of February 7 2018.pdf', pages='all')


# In[10]:


# The file is 23 pages, so 981 seems about right
all_data.shape


# In[11]:


all_data.head().T


# In[12]:


# clean up column names
all_data.columns = [c.replace(' ', '_').lower() for c in all_data.columns]


# In[13]:


all_data.ward.value_counts()


# In[14]:


# remove extra page header rows
all_data = all_data[all_data.ward != 'WARD']


# In[15]:


all_data.shape


# # Clean up some bad data

# In[50]:


# some unit numbers are in the quadrant field
# unit numbers don't exist anywhere else, so we're going to just nuke them
all_data[all_data.quadrant.apply(lambda x: x[:2]) != all_data.quadrant]


# In[51]:


# use only the first two characters of the quadrant field
all_data.quadrant = all_data.quadrant.apply(lambda x: x[:2])


# In[60]:


# tidy up miscellaneous stuff I spotted
all_data[all_data.street_name != all_data.street_name.apply(lambda x: x.upper())]


# In[61]:


all_data.street_name = all_data.street_name.apply(lambda x: x.upper())


# In[69]:


all_data.loc[109].street_type = 'ST'


# In[41]:


# make a field with the full address
all_data['full_address'] = all_data.apply(lambda x: x['street_number'] + ' ' + x['street_name'] + ' ' + x['street_type'] + ' ' + x['quadrant'] + ' Washington, DC', axis=1)


# In[71]:


all_data.head().T


# # Output
# 
# This csv was uploaded to Google Maps to make this: https://drive.google.com/open?id=15QCg36tt1y3aqp52yoeAliOwxRtiUjkh&usp=sharing. Another use might be to geocode the addresses and pin on the ANC using a spatial join with a shapefile.

# In[43]:


all_data.to_csv('gmaps_out.csv', index=False)

