# setup
import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_ipos():
    ipos = pd.DataFrame()
    for year in ['2022','2023']:
        text = requests.get(f'https://stockanalysis.com/ipos/{year}/').text
        ipos_temp = pd.read_html(text)[0]
        ipos = pd.concat([ipos,ipos_temp])
    return ipos

def get_cik_df(headers):
    # CIK df
    tickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers)
    df = pd.DataFrame.from_dict(tickers.json(), orient='index')
    df['cik_str'] = df['cik_str'].astype(str).str.zfill(10)
    return df

def get_s1(ticker,df):
    headers = {'user-agent': 'sprintboy207@gmail.com'}

    # find current ticker
    cik = df[df['ticker'] == ticker].cik_str[0]
    print(cik)

    # Get S-1 URL
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    fillings = requests.get(url, headers=headers).json()
    s1_index = fillings['filings']['recent']['form'].index('S-1')
    acn_num = fillings['filings']['recent']['accessionNumber'][s1_index].replace('-', '')
    doc = fillings['filings']['recent']['primaryDocument'][s1_index]
    s1_url = f'https://www.sec.gov/Archives/edgar/data/{cik}/{acn_num}/{doc}'
    return s1_url

def get_text(url,headers):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content,'html.parser')
    text = soup.text.strip().replace('/n','')

# main
headers = {'user-agent': 'sprintboy207@gmail.com'}
cik_df = get_cik_df(headers)
ipos = get_ipos()[:2]
print(len(ipos))
for ticker in ipos.Symbol.values:
    print(ticker)
    url = get_s1(ticker,cik_df)
    print(url)
    text = get_text(url,headers)

print('done')
