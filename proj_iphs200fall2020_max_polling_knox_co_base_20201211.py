# -*- coding: utf-8 -*-
"""proj_iphs200fall2020_max_polling_knox_co_base_20201211.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1efmGaS1NfS-2gGT8rppsOZK1wSD93VSa

# **Step 0. Setup Environment, Download Files and Outline Project**

Note:

* There are two code cells that require input before continuing automatic execution (#2 gdrive auth) and (#7 unzip [A]ll)
* The DataFrame knox_2006_addr_df contains the address and computed (long, lat) coordinates because only 2006 dataset has address info
* The DataFrame knox_2006_2012_df contains columns that track the changes in voter registration over the period 2006 to 2012
* More polling stations were added beween 2006 and 2012 but we don't have any address information on them
* Rows/records on polling addresses are incomplete in the 2006 dataset
* Some data cells are blank or have bad data in the original datasets
"""

# Commented out IPython magic to ensure Python compatibility.
# %load_ext google.colab.data_table

# Allows interactive filtering/scrolling of DataFrame
# %unload_ext google.colab.data_table # To unload interative DataFrame widget
# Ref: https://colab.research.google.com/notebooks/data_table.ipynb#scrollTo=JgBtx0xFFv_i

# Commented out IPython magic to ensure Python compatibility.
# GIVE AUTHORIZATION to access your gdrive

from google.colab import drive
drive.mount('/gdrive')
# %cd /gdrive

# Commented out IPython magic to ensure Python compatibility.
# CUSTOMIZE to your working directory

# %cd ./MyDrive/courses/2020f_iphs200_programming_humanity/code/knox_vote/

!pwd

!wget https://www.co.knox.oh.us/taxmap/FilestoDownload/vote_precincts.zip

!ls *.zip

# MANUALLY Click on promt and enter [A]ll option in text input below

!unzip vote_precincts.zip

!ls vote_precincts.*

# Make sure we have the source polling *.xls datafile

!ls knox*

# url_file = 'knox_co_oh_polling_addr_2006_2012_20201210.xlsx'
url_file = 'knox_co_oh_polling_2006-2012.xls'

"""## **Step 0 (a) GeoPandas for Knox County Ohio**

References:
* (Data Sources) https://www.co.knox.oh.us/index.php/files-to-download
* (DataCamp) https://campus.datacamp.com/courses/visualizing-geospatial-data-in-python/
* (Tutorial) https://towardsdatascience.com/geopandas-101-plot-any-data-with-a-latitude-and-longitude-on-a-map-98e01944b972
* (w/github) https://github.com/rylativity/identifying_wnv_locations-raw_repo- (20180924 18s)

```
I've updated the colab notebook we found and corrected a few typos, etc. You can see it at this link with the voting precints mapped in color:
https://colab.research.google.com/drive/1iVyX6dIpoBDisjW2nb_a-GN2V-uJ7Y2p?usp=sharing
At the top of this file I list references you can use to expand upon this. In particular, the first two chapters of the DataCamp on GeoPandas shows how you can sjoin several geopandas dataframes like sql joins on different database tables.
One idea is for you to generate two more *.shp files which plot the (longitude, latitude) coordinates for??
a) current polling stationsb) potential better/more central/easier to access polling stations.
You can use this website to get the (lng, lat) geo coordinates for any existing or proposed polling address from sites like this:
https://www.latlong.net/convert-address-to-lat-long.html
You would then manually compile a *.shp file using Point datatype as explained in DataCamp.
If you could get some data on population centers or ease of access routes/traffic flows that we discussed today, you could do some interesting work like suggesting more accessible polling locations:
https://medium.com/@sumit.arora/plotting-weighted-mean-population-centroids-on-a-country-map-22da408c1397https://geopandas.org/geometric_manipulations.html
Check these resources out and let me know if you have more questions,
```

![alt text](https://vignette.wikia.nocookie.net/genealogy/images/e/e7/Map_of_Knox_County_Ohio_With_Municipal_and_Township_Labels.PNG/revision/latest?cb=20071118214504)

## **Step 0. (b) How to Analyze Geographic Data in Shapefiles**

---

From empty Dorrito bags and fast food cups lining the curb, to plastic bags stuck in trees, litter mars too many L.A. neighborhoods. In response, in 2016 Mayor Eric Garcetti implemented a scoring system to [quantify cleanliness](https://www.citylab.com/solutions/2016/05/how-los-angeles-is-using-data-to-tackle-street-cleanliness/481722/) of city streets. How does your neighborhood stack up? Are you forced to hop over abandoned mattresses, or strolling down a sparkling sidewalk? To answer this question, we will look at cleanliness ratings for various neighborhoods in Los Angeles County. 

While programming experience helps for this instructable, it is not required.* (Please see our [first](https://colab.research.google.com/drive/1102rYgCZMWIPa0HdezbiiEx-t5Ikct0s#scrollTo=bu7i1hbHvGzW) and [second](https://colab.research.google.com/drive/1QKoElHpzqC0wf7T4oBFbZ4QQXgXRSXMr#scrollTo=w4D-Jd8tgvBQ) instructables for information on the tools used in this exercise, and the [final](https://colab.research.google.com/drive/1NyiS1KsojrsGxBSf5zxeil-M4R_ffD-2#scrollTo=l6t7XEUgDGZY) instructable for information on APIs)*

# Step 1: Gather and Understand Ingredients Used in This Notebook

In this instructable we'll be exploring another way to map geographic data: using the [shapefile format](http://desktop.arcgis.com/en/arcmap/10.3/manage-data/shapefiles/what-is-a-shapefile.htm) created by ESRI. Shapefiles are vector format files about geographic coordinates or polygons that are stored in a compressed zip file. Vector formats store information about graphics as mathematical formulas, rather than pixels, which makes the files small and portable. About 2127 entries on [LA Counts](http://lacounts.org/) feature shapefiles, making it one of the more popular formats. When you use shapefiles, Mapbox converts the data from the compressed zip file to vector tiles. From there, you can create styles using this geographic data to generate map visualizations, similar to the last Instructable, which mapped geographic coordinates. 

For this exercise, you will need: 

*  Download a Shapefile dataset from [LA Counts ](https://lacounts.org). In this exercise we will use a dataset for the [Clean Streets Index](https://www.lacounts.org/dataset/clean-streets-index-grids-2018-quarter-3) created by the city of Los Angeles. We selected this file becuase it was well-documented through metadata, and featured a Shapefile. 
*  A Jupyter Notebook like this one, hosted on [Google's colab.](http://colab.research.google.com/) 
*   Free Python Libraries (pyshp [link text](https://pypi.org/project/pyshp/
), [numpy](http://www.numpy.org/), [pandas](https://pandas.pydata.org/), and [plotly](https://plot.ly/python/)), and [Mapbox](https://www.mapbox.com/). These are accessible within Jupyter Notebooks, so you don't need to download them. 
*   Your smarts! ????

# Step 2: Upload Shapefile Data to Jupyter Notebook 

First, unzip your shapefile package that you downloaded from LA Counts. Next, upload all the files in the zip file to the Jupyter Notebook. Do this by: 

1. If necessary, click on the arrow in your upper-left corner to open the sidebar. 

![alt text](http://www.civictechs.com/wp-content/uploads/2019/06/step-1-arrow.png)

2. Click on "Files," then "upload." 

![alt text](http://www.civictechs.com/wp-content/uploads/2019/06/steps-2-and-three.png)

3. Select and upload your files. You should then see them appear in the file window.

# Step 2: Configuration and Download Packages
"""

# First install missing Python packages

print("Installing geopandas...")

# We need to install geopandas and descartes using PIP because they are 
# not installed on Jupyter by default. 

!pip install geopandas
!pip install descartes 

!pip install geopy

# Python library to parse us addresses from text strings
# https://github.com/datamade/usaddress

!pip install usaddress

# Start importing Python packages from core to special purpose with more dependencies

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import re
import json
from collections import OrderedDict

import usaddress

import geopandas as gpd
from shapely.geometry import Point, Polygon

import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

import folium
from folium.plugins import FastMarkerCluster

"""# Step 3: Load and Print The Shapefile  

Next, load your shapefile and print it out. 

The Los Angeles Clean Streets Index is a grading system for every street in Los Angeles. The Bureau of Sanitation drove and scored over 9,000 miles of streets and alleys - each segment received a "cleanliness score" from 1-3. Each street score is based on four factors: litter (Seg_LL_Sco), weeds (Seg_Wd_Sco), bulky items (Seg_Bk_Sco), and illegal dumping (Seg_ID_Sco) that are aggregated into CSCatScore, a value that designates overall cleanliness. This assessment is repeated every quarter. This assessment is for Quarter 2 of 2018. Los Angeles is leading the way as the only big city in the US conducting a regular cleanliness assessment of every City street. 
"""

# Next, print out the shapefile. 
# It won't look like much because we are looking at geographic coordinates. 

print("Loading Shapefile...")

# If using your files, replace below filename ("Clean_Streets_Index_Grids_2018_Quarter_3.shp") with the 
# shapefile filename you uploaded. 

shapefile = gpd.read_file("vote_precincts.shp")

# The "head" function prints out the first five rows in full, so you can see
# the columns in the data set too! 

shapefile.head(1)

"""# Step 4: Load Polling Data and Locations

## Step 4. (a) Combine core data from every year into one consistent DataFrame knox_all_df
"""

# TODO: clean up and standardize the column headers to be exactly the same across all tabs
#       with no embedded spaces:
# 
# instead of "Registered R" and "R Registered" use "Registered_R" everywhere

!ls -al *.xls

# CUSTOMIZE: Set this variable to the name of your Excel file with polling data

knox_poll_data_xls = 'knox_co_oh_polling_2006-2012.xls'

# Read the sheet named '2006_addr' which has address string in column 'addresses'

# knox2006_df = pd.read_excel(url_file, sheet_name='2006', names=['precinct', 'reg_total', 'reg_dem', 'reg_rep'])
knox2006_df = pd.read_excel(knox_poll_data_xls, sheet_name='2006', names=['precinct', 'reg_total', 'reg_dem', 'reg_rep'])

knox2006_df['year'] = '2006'
knox2006_df.head()

# Read the sheet named '2008_addr' which has address string in column 'addresses'

# knox2008_df = pd.read_excel(url_file, sheet_name='2008', names=['precinct', 'reg_total', 'reg_dem', 'reg_rep'])
knox2008_df = pd.read_excel(knox_poll_data_xls, sheet_name='2008', names=['precinct', 'reg_total', 'reg_dem', 'reg_rep'])
knox2008_df['year'] = '2008'

knox2008_df.head()

# Read the sheet named '2010_addr' which has address string in column 'addresses'

# knox2010_df = pd.read_excel(url_file, sheet_name='2010', names=['precinct', 'reg_total', 'reg_dem', 'reg_rep'])
knox2010_df = pd.read_excel(knox_poll_data_xls, sheet_name='2010', names=['precinct', 'reg_total', 'reg_dem', 'reg_rep'])
knox2010_df['year'] = '2010'

knox2010_df.head()

# Read the sheet named '2012_addr' which has address string in column 'addresses'

# knox2012_df = pd.read_excel(url_file, sheet_name='2012', names=['precinct', 'reg_total', 'reg_dem', 'reg_rep'])
knox2012_df = pd.read_excel(knox_poll_data_xls, sheet_name='2012', names=['precinct', 'reg_total', 'reg_dem', 'reg_rep'])
knox2012_df['year'] = '2012'

knox2012_df.head()

# Concatenate all polling data DataFrames into one master
#
# CHECK visually inspect for bad, missing or other malformed data (e.g. typos, outliners, impossible values)
# if found, GOBACK to your source xls files and clean up!

knox_dfs = [knox2006_df, knox2008_df, knox2010_df, knox2012_df]
knox_2006_2012_df = pd.concat(knox_dfs)

# Drop rows where 'precinct' is 'NaN' or some variant of 'Totals'
knox_2006_2012_df = knox_2006_2012_df[knox_2006_2012_df['precinct'].str.strip().str.len() > 8]

knox_2006_2012_df

knox_2006_2012_df.info()

# DO Clean your source xls datafile by adding missing 'reg_total' (Registered voters total has one blank cell)

# Drop rows where 'precinct' is 'NaN' or some variant of 'Totals'
# knox_2006_2012_df = knox_2006_2012_df[knox_2006_2012_df['reg_total'].notnull()] # astype(str).str.strip() != '']

# Drop rows with 'NaN' entries
knox_2006_2012_df = knox_2006_2012_df[knox_2006_2012_df.notnull()] # astype(str).str.strip() != '']


knox_2006_2012_df.info()

# Split out the precinct string into precinct_no and precint_name

knox_2006_2012_df['precinct_no'] = knox_2006_2012_df['precinct'].str.split(' ').str.get(0).astype(int)
knox_2006_2012_df['precinct_name'] = knox_2006_2012_df['precinct'].str.split(' ').str[1:].str.join(' ').str.title()

knox_2006_2012_df.reset_index(drop=True, inplace=True)

knox_2006_2012_df

# CLEAN: last row in dataset has 'NaN' for RegDem and RegRep
#        go back and fix, for now we have to drop entire row for 0059 FREDERICKTOWN C

knox_2006_2012_df = knox_2006_2012_df.dropna()
knox_2006_2012_df

# Assign more narrow/accurate types for robustness and better error detection

knox_2006_2012_df['precinct'] = knox_2006_2012_df['precinct'].astype('string')
knox_2006_2012_df['reg_total'] = knox_2006_2012_df['reg_total'].astype('int')
knox_2006_2012_df['reg_dem'] = knox_2006_2012_df['reg_dem'].astype('int')
knox_2006_2012_df['reg_rep'] = knox_2006_2012_df['reg_rep'].astype('int')
knox_2006_2012_df['year'] = knox_2006_2012_df['year'].astype('int')
knox_2006_2012_df['precinct_name'] = knox_2006_2012_df['precinct_name'].astype('string') 
knox_2006_2012_df.info()

# Rearrange column by importance

knox_2006_2012_df = knox_2006_2012_df[['precinct_no', 'precinct_name', 'reg_total', 'reg_dem', 'reg_rep', 'year', 'precinct']]

# CHECK for that we have no missing data by comparing Non-Null Count

knox_2006_2012_df.info()

# CHECK Visually inspect entire knox_2006_2012_df DataFrame to find 
# bad rows with missing data, make sure each change does not introduce errors/bad data

knox_2006_2012_df

"""## Step 4. (b) Extract out sub-components from address string"""

# Parse address string into separate components/columns (incomplete, only exists for 2006 and even then has 5 empty addresses)
#
# NOTE: (Dataset profile) 
#
# - 58 rows/polling sites with 5 blank '054 DANVILLE', '055 WAYNE', '056 FREDERICKTOWN A', '057 FREDERICKTOWN B', '058 FREDERICKTOWN C'
# - row may be blank
# - state = ['', 'OH', 'OHIO']
# - city = ['MT. VERNON', 'MOUNT VERNON', 'FREDRICKTOWN', 'DANVILLE', 'HOWARD', 'GAMBIER', 'CENTERBERG', 'BLADENSBERG', 'GLENMONT', 'UTICA']
# - address (ends with, with/without final '.') = ['ROAD', 'RD.', 'STREET', 'ST.', 'DRIVE', 'DR.', 'AVE.', 'LANE']
# - address no. = [/d]{2,5} (2-5 digit integer)

knox2006_addr_df = pd.read_excel(knox_poll_data_xls, sheet_name='2006_addr', names=['precinct', 'address', 'reg_total', 'reg_dem', 'reg_rep'], dtype={'address':str})
knox2006_addr_df['year'] = '2006'

knox2006_addr_df

# BUG in Pandas

type(knox2006_addr_df.iloc[6]['reg_total'])   # str (empty)
# type(knox2006_addr_df.iloc[7]['reg_total']) # int

# Test 

test_str = 0
print(isinstance(test_str, str))

# CLEAN: Previous cell show issing reg_total for 0007 MOUNT VERNON 2-C 
#        so drop row index=6

# knox2006_addr_df.drop(6, inplace=True) # 20201210 fixed in original Excel spreadsheet

# index_reg_total = knox2006_addr_df.reg_total.apply(lambda x : isinstance(x, str))
# print(index_reg_total)

# knox2006_addr_df.drop(index_reg_total, inplace=True, axis=0)
# index_names = (isinstance(knox2006_addr_df['reg_total'],str)) | (isinstance(knox2006_addr_df['reg_dem'],str)) | (isinstance(knox2006_addr_df['reg_rep'],str))
# type(index_names)

# drop these given row 
# indexes from dataFrame 
# df.drop(index_names, inplace = True, axis=0)

# CLEAN: Previous cell show the last 6 rows with 'NaN' so have to drop
#        Go back and fix, for now we have to drop these rows
#       
# Drop rows where 'precinct' is 'NaN' or some variant of 'Totals'

# knox2006_addr_df = knox2006_addr_df[knox2006_addr_df['precinct'].str.strip().str.len() > 8]
knox2006_addr_df = knox2006_addr_df.dropna()
knox2006_addr_df

# Split out the precinct string into precinct_no and precint_name

knox2006_addr_df['precinct_no'] = knox2006_addr_df['precinct'].str.split(' ').str.get(0).astype(int)
knox2006_addr_df['precinct_name'] = knox2006_addr_df['precinct'].str.split(' ').str[1:].str.join(' ').str.title()

knox2006_addr_df.reset_index(drop=True, inplace=True)

knox2006_addr_df

# Assign more narrow/accurate types for robustness and better error detection

knox2006_addr_df['precinct'] = knox2006_addr_df['precinct'].astype('string')
knox2006_addr_df['address'] = knox2006_addr_df['address'].astype('string') 
knox2006_addr_df['reg_total'] = knox2006_addr_df['reg_total'].astype('int')
knox2006_addr_df['reg_dem'] = knox2006_addr_df['reg_dem'].astype('int')
knox2006_addr_df['reg_rep'] = knox2006_addr_df['reg_rep'].astype('int')
knox2006_addr_df['year'] = knox2006_addr_df['year'].astype('int')
knox2006_addr_df.info()

# Drop rows where 'address' is 'NaN' or other issues
# TODO Goback to original xls file and fix source of these errors

knox2006_addr_df = knox2006_addr_df[pd.notnull(knox2006_addr_df['address'])]
knox2006_addr_df

# TODO Visually inspect for errors, bad data, missing data, etc.
#      then correct in source xls files (missing address for precincts >= 54 or indexes >= 53)

knox2006_addr_df.info()

# DEBUGGING ONLY:
# test cell: edge case with street name prefix ('StreetNamePreDirectional') variants and edge cases

addr_err = '505 S YELLOW JACKET ST. DANVILLE, OHIO, 43014'

try:
    tagged_address, address_type = usaddress.tag(addr_err)
except usaddress.RepeatedLabelError as e :
    some_special_instructions(e.parsed_string, e.original_string)

tagged_address

# DEBUGGING ONLY:

tagged_address['AddressNumber']
tagged_address['StateName']

# DEBUGGING ONLY

address_type

# DEBUGGING ONLY: 
# knox2006_addr_df.drop('addr_parsed', axis=1, inplace=True)

knox2006_addr_df.head()

knox2006_addr_df['addr_parsed'] = knox2006_addr_df.apply(lambda row: usaddress.parse(row['address']), axis=1)

knox2006_addr_df.info()

# NOTE: addr_parsed is a pd.Series containing a list of tuples

print(knox2006_addr_df['addr_parsed'][0])

knox2006_addr_df = knox2006_addr_df[['precinct_no', 'precinct_name', 'address', 'reg_total', 'reg_dem', 'reg_rep' ,'year', 'addr_parsed', 'precinct']]

knox2006_addr_df.head()

# CLEAN: Previous cell shows inconsistent format for 'address' which causes
#        parse errors in cells below

# FIX: Data in 'address' column of Excel notebook to be consisent
#      e.g. first 2 precints above (Mount Vernon 1-A, 1-B) are malformed
#      with missing street number or street number after instead of before street name

def split_addr(str):
  try:
    tagged_address, address_type = usaddress.tag(string)
  except usaddress.RepeatedLabelError as e :
    some_special_instructions(e.parsed_string, e.original_string)

# Create a temp working DataFrame addr_df to help parse address components

addr_df = knox2006_addr_df.apply(lambda row: usaddress.tag(row['address']), axis=1)
addr_df.head(7)

# In the following cells, create separate DataFrames for all parts of the address
# These DataFrames will then be horizontally concatenated with the original DataFrame
# so we can later extract clean text to make GeoPy REST API calls
# to obtain (long, lat) values for each polling station

# TODO: convert these to def fn(df) to be able to handle multiple year datasets when
#       they become available

addr_parts_ls = []

for num, row in enumerate(addr_df):
  # print(f"Working on row #: {num}")

  if 'Recipient' not in row[0]:
    if ('AddressNumber' in row[0]) & ('StreetName' in row[0]) & ('StreetNamePostType' in row[0]):
      if ('StreetNamePreDirectional' in row[0]):
        FullAddress = ' '.join([row[0]['AddressNumber'].strip(), row[0]['StreetNamePreDirectional'].strip().title(), row[0]['StreetName'].strip().title(), row[0]['StreetNamePostType'].strip().title()])
      else:
        FullAddress = ' '.join([row[0]['AddressNumber'].strip(), row[0]['StreetName'].strip().title(), row[0]['StreetNamePostType'].strip().title()])
    else:
      FullAddress = ''
  else:
    # print('Record missing.')
    FullAddress = ''
  
  addr_parts_ls.append(FullAddress)

print(addr_parts_ls)
# usaaddr = useaddress.tag(row['address'])
# print(usaaddr['StreetName'])

city_parts_ls = []

for num, row in enumerate(addr_df):
  # print(f"Working on row #: {num}")

  if 'Recipient' not in row[0]:
    if 'PlaceName' in row[0]:
      FullCity = row[0]['PlaceName'].strip().title()
    else:
      FullCity = ''
  else:
    # print('Record missing.')
    FullCity = ''
  
  city_parts_ls.append(FullCity)

print(city_parts_ls)
  # usaaddr = useaddress.tag(row['address'])
  # print(usaaddr['StreetName'])

state_parts_ls = []

for num, row in enumerate(addr_df):
  # print(f"Working on row #: {num}")

  if 'Recipient' not in row[0]:
    if 'StateName' in row[0]:
      FullState = row[0]['StateName'].strip().title()
    else:
      FullState = ''
  else:
    # print('Record missing.')
    FullState = ''
  
  state_parts_ls.append(FullState)

print(state_parts_ls)
  # usaaddr = useaddress.tag(row['address'])
  # print(usaaddr['StreetName'])

zip_parts_ls = []

for num, row in enumerate(addr_df):
  # print(f"Working on row #: {num}")

  if 'Recipient' not in row[0]:
    if 'ZipCode' in row[0]:
      FullZip = int(row[0]['ZipCode'].strip())
    else:
      FullZip = ''
  else:
    # print('Record missing.')
    FullZip = ''
  
  zip_parts_ls.append(FullZip)

print(zip_parts_ls)
  # usaaddr = useaddress.tag(row['address'])
  # print(usaaddr['StreetName'])

addr_all_parts_df = pd.DataFrame(
    {'addr_full': addr_parts_ls,
     'city': city_parts_ls,
     'state': state_parts_ls,
     'zip': zip_parts_ls
    })

# Set defaults for Knox County Ohio, USA

addr_all_parts_df['state'] = "OH"
addr_all_parts_df['country'] = "USA"

# Assign more narrow/accurate types for robustness and better error detection

addr_all_parts_df['addr_full'] = addr_all_parts_df['addr_full'].astype('string')
addr_all_parts_df['city'] = addr_all_parts_df['city'].astype('string') 
addr_all_parts_df['state'] = addr_all_parts_df['state'].astype('string')
addr_all_parts_df['zip'] = addr_all_parts_df['zip'].astype('int')
addr_all_parts_df['country'] = addr_all_parts_df['country'].astype('string')
addr_all_parts_df.info()

# knox_2006_addr_df will be our master DataFrame with all years concatenated together

knox_2006_addr_df = pd.concat([knox2006_addr_df, addr_all_parts_df], axis=1)

knox_2006_addr_df.info()

# Reorder columns

knox_2006_addr_df = knox_2006_addr_df[['precinct_no', 'precinct_name', 'address', 'addr_full', 'reg_total', 'reg_dem', 'reg_rep', 'year', 'city', 'state', 'zip', 'country', 'addr_parsed', 'precinct']]

knox_2006_addr_df.info()

# Visually inspect for errors, missing, malformed, etc data

knox_2006_addr_df

"""## Step 4. (c) Calculate new column values for each (Polling Station + Year) data point

Current Over/Under Served Polling areas
* %Knox Co Reg Voters = (Poll Station Registered Voters)/(Total Reg Voters in Knox Co)
* %Democrat = (Poll Station Registered Democrats)/(Poll Station Registered Republicans + Poll Station Registered Republicans)
* %Republican = (Poll Station Registered Republicans)/(Poll Station Registered Republicans + Poll Station Registered Republicans)

Trends over Time
* %Democrat Growth = (2012 Reg Dem - 2006 Reg Dem)/(2006 Reg Dem)
* %Republican Growth = (2012 Reg Rep - 2006 Reg Rep)/(2006 Reg Rep)

Use Seaborn graphs to represent 3 additional dimensions of data:
* Color = Republican (Red) or Democrat (Blue) - Hue reflect % dominance
* Size = Relative number of registered voters
* Shape = UP (Growing) or Down (Shrinking) number of registered voters

"""

knox_2006_2012_df

knox_2006_2012_df.info()

# ERROR: Need to recalc these broken out by each year, not over all 4 years

knox_2006_2012_df['per_knox'] = knox_2006_2012_df['reg_total']/knox_2006_2012_df['reg_total'].sum() * 100

# ERROR: Need to recalc these broken out by each year, not over all 4 years

knox_2006_2012_df['per_dem'] = knox_2006_2012_df['reg_dem']/knox_2006_2012_df['reg_total']
knox_2006_2012_df['per_rep'] = knox_2006_2012_df['reg_rep']/knox_2006_2012_df['reg_total']

knox_2006_2012_df.info()

knox_2006_2012_df

# ERROR: Need to recalc these broken out by each year, not over all 4 years

# Check math

print(knox_2006_2012_df['per_knox'].sum())
print(knox_2006_2012_df['per_dem'].sum())
print(knox_2006_2012_df['per_rep'].sum())

knox2012_df.head()

# Commented out IPython magic to ensure Python compatibility.
# %whos
# Show all the variable defined in the current environment

# Calculate the change in Knox Co. registered voters between 2006 and 2012

knox_2006_2012_df['incr_voters_since_2006'] = knox2012_df['reg_total'] - knox2006_addr_df['reg_total']

knox_2006_2012_df.head()

# Calculate the numerical change in Knox Co registered voters by party affiliation 2006 to 2012

knox_2006_2012_df['incr_dem_since_2006'] = knox2012_df['reg_dem'] - knox2006_addr_df['reg_dem']
knox_2006_2012_df['incr_rep_since_2006'] = knox2012_df['reg_rep'] - knox2006_addr_df['reg_rep']
knox_2006_2012_df['incr_3rd_since_2006'] = (knox2012_df['reg_total'] - knox2012_df['reg_dem'] - knox2012_df['reg_rep']) - (knox2006_addr_df['reg_total'] - knox2006_addr_df['reg_dem'] - knox2006_addr_df['reg_rep'])

knox_2006_2012_df.head(20)

# Calculate the percent change in Knox Co registered voters by party affiliation 2006 to 2012

knox_2006_2012_df['per_incr_dem_since_2006'] = knox_2006_2012_df['incr_dem_since_2006']/knox2006_addr_df['reg_dem']
knox_2006_2012_df['per_incr_rep_since_2006'] = knox_2006_2012_df['incr_rep_since_2006']/knox2006_addr_df['reg_rep']
knox_2006_2012_df['per_incr_3rd_since_2006'] = knox_2006_2012_df['incr_3rd_since_2006']/(knox2006_addr_df['reg_total'] - knox2006_addr_df['reg_dem'] - knox2006_addr_df['reg_rep'])

knox2012_df.head(20)

knox_2006_2012_df.info()

# Drop rows where 'precinct' is 'NaN' or some variant of 'Totals'

knox2006_addr_df = knox2006_addr_df[knox2006_addr_df['precinct'].str.strip().str.len() > 8]

# Split out the precinct string into precinct_no and precint_name

knox2006_addr_df['precinct_no'] = knox2006_addr_df['precinct'].str.split(' ').str.get(0).astype(int)
knox2006_addr_df['precinct_name'] = knox2006_addr_df['precinct'].str.split(' ').str[1:].str.join(' ').str.title()

knox2006_addr_df.reset_index(drop=True, inplace=True)

knox2006_addr_df

# Visually inspect and look for non_dull

knox2012_df.info()

knox2012_df

# DO Clean your source xls datafile by adding missing 'reg_total', 'reg_dem' (Registered voters total has one blank cell)

# Drop rows where 'precinct' is 'NaN' or some variant of 'Totals'
"""
# FIXED in latest Excel input file 20201211
knox2012_df = knox2012_df[knox2012_df['reg_total'].notnull()] # astype(str).str.strip() != '']
knox2012_df = knox2012_df[knox2012_df['dem_total'].notnull()] # astype(str).str.strip() != '']
"""
knox2012_df.info()

# Assign more narrow/accurate types for robustness and better error detection

knox2012_df['precinct'] = knox2012_df['precinct'].astype('string')
knox2012_df['reg_total'] = knox2012_df['reg_total'].astype('int')
knox2012_df['reg_dem'] = knox2012_df['reg_dem'].astype('int')
knox2012_df['reg_rep'] = knox2012_df['reg_rep'].astype('int')
knox2012_df['year'] = knox2012_df['year'].astype('int')
# BUG: 'precinct_name' was changed to 'precinct' in the source Excel file for some reason 20201211
#      do not change the column names in the Excel notebook!
# knox2012_df['precinct_name'] = knox2012_df['precinct_name'].astype('string') 
knox2012_df['precinct'] = knox2012_df['precinct'].astype('string') 
knox2012_df.info()

"""# Step 5: Display Trends over Time with Seaborn/Plotly

Use lineplots to show the relative growth/decline in both 
* (a) overall voter registration
* (b) Dem vs Rep voter registration
* (c) voter registration broken out by polling station 

Reference:

* https://seaborn.pydata.org/generated/seaborn.lineplot.html
"""

knox_2006_2012_df.info()

knox_2006_2012_df

knox_2006_2012_df.shape

knox_2006_2012_df.precinct_name.nunique()

"""### Visualize Precincts with Highest Total Number of Registered Voters"""

knox_2006_2012_df.precinct_name.unique()

# Top 10 Percent fo Total Registered voters by polling station

knox_2006_2012_regtot_df = knox_2006_2012_df.sort_values(['reg_total'], ascending=False).head(10) # groupby('precinct_name').head(10)
knox_2006_2012_regtot_df

knox_2006_2012_regtot_df.info() # plot(x='year', y='reg_total')

knox_2006_2012_regtot_df.plot(x='precinct', y='reg_total', label='precinct', kind='bar') 
plt.title('Top 10 Percent Total Voter Registration by Polling Station')
plt.show()

"""### Visualize Precincts with Highest Percentage of (a) Democratic and (b) Republican Registered Voters"""

# Top 10 Percent fo Democratic Registered voters by polling station

knox_2006_2012_regdem_df = knox_2006_2012_df.sort_values(['reg_dem'], ascending=False).head(10) # groupby('precinct_name').head(10)
knox_2006_2012_regdem_df

knox_2006_2012_regdem_df.plot(x='precinct', y='reg_dem', label='precinct', kind='bar') 
plt.title('Top 10 Percent Democratic Voter Registration by Polling Station')
plt.show()

# Top 10 Percent fo Republican Registered voter by polling station

knox_2006_2012_regrep_df = knox_2006_2012_df.sort_values(['reg_rep'], ascending=False).head(10) # groupby('precinct_name').head(10)
knox_2006_2012_regrep_df

knox_2006_2012_regrep_df.plot(x='precinct', y='reg_rep', label='precinct', kind='bar') 
plt.title('Top 10 Percent Republican Voter Registration by Polling Station')
plt.show()

"""### Visualize The Average (Mean) and Variation (Std Dev) of (a) Total Registered Voters (b) Percent Registered Dems and (c) Percent Registered Reps"""

knox_2006_2012_gb = knox_2006_2012_df.groupby(['precinct', 'year'])
knox_2006_2012_gb

# Find the mean and standard deviation for (a) Total, (b) Dem and (c) Rep
#   registered voters over the period 2006-2012

knox_2006_2012_agg = knox_2006_2012_df.agg({
    'reg_total' : ['mean', 'std'],
    'reg_dem' : ['mean', 'std'],
    'reg_rep' : ['mean', 'std']
})

knox_2006_2012_agg

knox_2006_2012_gb = knox_2006_2012_df.groupby(['year', 'precinct']).agg({'reg_total':'sum'})
knox_2006_2012_gb

"""### Visualize the Change in Total Registered Voters by Precinct"""

# FIX BAD DATA: Fill in data for all the NaN in the table below

knox_2006_2012_us = knox_2006_2012_gb.unstack()
knox_2006_2012_us

type(knox_2006_2012_us)

len(knox_2006_2012_us.columns.values[0])

if (re.search('MOUNT VERNON', knox_2006_2012_us.columns.values[0][1])):
  print("Found It!")

list(knox_2006_2012_us.columns.values[0][1]) # .tolist())

for i in range(knox_2006_2012_us.shape[1]):
  knox_2006_2012_us.T.iloc[i].plot(kind='line')
  # knox_2006_2012_regrep_df.plot(x='precinct', y='reg_rep', label='precinct', kind='bar') 
  precinct_str = knox_2006_2012_us.T.index[i]
  title_str = f"Change in Total Registered Voters in {precinct_str} (2008-2012)"
  plt.title(title_str) # 'Top 10 Percent Republican Voter Registration by Polling Station')
  plt.show()

knox2006_2012_pt = pivot_table(knox_2006_2012_df[]