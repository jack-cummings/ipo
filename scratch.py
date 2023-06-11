# set up
import requests
import pandas as pd

headers = {'user-agent':'sprintboy207@gmail.com'}

# CIK df
tickers = requests.get("https://www.sec.gov/files/company_tickers.json",headers=headers)
df = pd.DataFrame.from_dict(tickers.json(),orient='index')
df['cik_str'] = df['cik_str'].astype(str).str.zfill(10)

# find current ticker
cik = df[df['ticker']=='LIPO'].cik_str[0]
print(cik)

# Get S-1 URL
url = f"https://data.sec.gov/submissions/CIK{cik}.json"
fillings = requests.get(url, headers=headers).json()
s1_index = fillings['filings']['recent']['form'].index('S-1')
acn_num = fillings['filings']['recent']['accessionNumber'][s1_index].replace('-','')
doc = fillings['filings']['recent']['primaryDocument'][s1_index]
s1_url = f'https://www.sec.gov/Archives/edgar/data/{cik}/{acn_num}/{doc}'
print(s1_url)



# # # Forms Endpoint
# # url = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}.json"
# # forms = requests.get(url, headers=headers)
#
# print('t')