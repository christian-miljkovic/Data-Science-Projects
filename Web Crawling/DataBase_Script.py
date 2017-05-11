
# coding: utf-8

# In[86]:

#!/usr/bin/python3

def GetHTML(urL):
    import requests
    from lxml import html 
    return html.fromstring((requests.get(url)).text)

url = "http://brandirectory.com/league_tables/table/global-500-2016"
brand_html = GetHTML(url)

#pull the data for the top 50 companies and store it in the array 
brand_array = []
brand_val_2016_array = []
brand_val_2015_array = []
brand_rank_array = []

#use this function clean up the data and convert it into ints

def strip_comma(str_a):
    return int(str_a.replace(',',''))

for i in range(0,50):
    company = '//*[contains(concat( " ", @class, " " ), concat( " ", "table_name", " " ))]//a'
    company = brand_html.xpath(company)[i].text_content()
    brand_array.append(company)
    
    
    brand_val_2016 = '//*[contains(concat( " ", @class, " " ), concat( " ", "v1", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "o", " " ))]'
    brand_val_2016 = strip_comma(brand_html.xpath(brand_val_2016)[i].text_content())
    brand_val_2016_array.append(brand_val_2016)
    
    brand_val_2015 = '//*[contains(concat( " ", @class, " " ), concat( " ", "v2", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "o", " " ))]'
    brand_val_2015 = strip_comma(brand_html.xpath(brand_val_2015)[i].text_content())
    brand_val_2015_array.append(brand_val_2015)
    
    brand_rank_array.append(i+1)


# In[99]:

print(type(brand_val_2015_array[1]))


# In[90]:

#now create the database

import MySQLdb as mdb
import sys

con = mdb.connect(host = 'localhost', 
                  user = 'root', 
                  passwd = 'dwdstudent2015', 
                  charset='utf8', use_unicode=True);


# Create the Ebola database
db_name = 'Top_Brands'
create_db_query = "CREATE DATABASE IF NOT EXISTS {db} DEFAULT CHARACTER SET 'utf8'".format(db=db_name)

# Create a database
cursor = con.cursor()
cursor.execute(create_db_query)
cursor.close()


# In[94]:

cursor = con.cursor()
db_name = 'Top_Brands'
table_name = 'Val_of_brands'
# Create a table

create_table_query = '''CREATE TABLE IF NOT EXISTS {db}.{table} 
                                (val_change int,
                                brand_name varchar(250),
                                rank int,
                                brand_val_2016 int,
                                brand_val_2015 int,
                                PRIMARY KEY(rank)
                                )'''.format(db=db_name, table=table_name)
cursor.execute(create_table_query)
cursor.close()


# In[102]:

query_template = '''INSERT INTO 
    Top_Brands.Val_of_brands(val_change, brand_name, rank, brand_val_2016,brand_val_2015) 
    VALUES (%s, %s, %s, %s, %s)'''

cursor = con.cursor()

for i in range(0,50):
    print("Inserting each brand",i)
    val_change = ((brand_val_2016_array[i]-brand_val_2015_array[i])/brand_val_2015_array[i])*100
    parameters = (val_change,brand_array[i],brand_rank_array[i],brand_val_2016_array[i],brand_val_2015_array[i])
    cursor.execute(query_template,parameters)

con.commit()
cursor.close()

