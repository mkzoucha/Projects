Data Preparation - World Stats (GDP info, murder rate, population)
By Michael Zoucha


Description: A data preparation project using GDP, murder rate, and population data that includes interactive graphs


File Dependencies: 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;world_gdp_historical.csv


Required Packages:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Pandas - For data frame processing of location list

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Numpy - For advanced mathematical and statistical analysis

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Re - For string regex

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;google.cloud - For querying BigQuery data

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;google.oauth2 - For setting up BigQuery credentials

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;fuzzywuzzy - For fuzzy matching

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sqlite3 - To store final data sets in SQL 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;matplotlib - For creating graphs

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;seaborn - For creating graphs

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ipywidgets - For interactive graphs

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;os - For file handling


NOTE: REQUIRES GOOGLE BIGQUERY API KEY JSON FILE IN ORDER TO RUN

Cell 21, Line 4:
credentials = service_account.Credentials.from_service_account_file(r'C:\Users\michaelzoucha\OneDrive - Bellevue University\zzKEYS\Google keys', scopes=['https://www.googleapis.com/auth/bigquery'])


Screenshot examples of the interactive graphs can been seen in 'interactive_graphs.pdf' and 'interactive_graphs.mp4'
