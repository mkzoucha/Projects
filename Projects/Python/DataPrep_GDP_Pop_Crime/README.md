Data Preparation - World Stats (GDP info, murder rate, population)
By Michael Zoucha


Description: A data preparation project using GDP, murder rate, and population data that includes interactive graphs


File Dependencies: 

world_gdp_historical.csv


Required Packages:

Pandas - For data frame processing of location list
Numpy - For advanced mathematical and statistical analysis
Re - For string regex
google.cloud - For querying BigQuery data
google.oauth2 - For setting up BigQuery credentials
fuzzywuzzy - For fuzzy matching
sqlite3 - To store final data sets in SQL 
matplotlib - For creating graphs
seaborn - For creating graphs
ipywidgets - For interactive graphs
os - For file handling


NOTE: REQUIRES GOOGLE BIGQUERY API KEY JSON FILE IN ORDER TO RUN

Cell 21, Line 4:
credentials = service_account.Credentials.from_service_account_file(r'C:\Users\michaelzoucha\OneDrive - Bellevue University\zzKEYS\Google keys', scopes=['https://www.googleapis.com/auth/bigquery'])


Screenshot examples of the interactive graphs can been seen in 'interactive_graphs.pdf' and 'interactive_graphs.mp4'