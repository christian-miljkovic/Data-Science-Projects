
# coding: utf-8

# In[1]:

import MySQLdb as mdb
import sys

con = mdb.connect(host = 'localhost', 
                  user = 'root', 
                  passwd = 'dwdstudent2015', 
                  charset='utf8', use_unicode=True);


# In[2]:

def SQLquery(query):
    import MySQLdb as mdb
    import sys
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def SQLquery_df(query):
    import pandas
    import MySQLdb as mdb
    import sys
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(query)
    rows = cur.fetchall()
    rows
    df_from_sql = pandas.DataFrame(list(rows))
    return df_from_sql


# In[7]:

Top_Brands = SQLquery_df('SELECT * FROM Top_Brands.Val_of_brands;')

Top_Brands_df = SQLquery('SELECT * FROM Top_Brands.Val_of_brands;')


# In[8]:

import pandas

Top_Brands_df = pandas.DataFrame(list(Top_Brands_df))
Top_Brands_df


# In[9]:

import matplotlib.pyplot as plt
plt.style.use('ggplot')
get_ipython().magic('matplotlib inline')


# In[13]:

Top_Brands_df.plot.bar(x='brand_name', y='val_change', color="green") 
Top_Brands_df.plot.area(x='brand_name', y='brand_val_2016', color="blue") 
Top_Brands_df.plot.scatter(x='rank', y='brand_val_2015', color="yellow") 


# In[ ]:



