import requests  
import csv 
import time 
from bs4 import BeautifulSoup 
import pandas as pd 
import os 
import gspread 
from google.oauth2.service_account import Credentials 
import pandas as pd
import glob


today = time.strftime('%m-%d')  
year = time.strftime('%Y') 
month = time.strftime('%m') 
month = (month[1]) 
sheet_work = int(month) - 1 
master_df = pd.DataFrame() 


path = 'D:/python/csv'
merge_path = 'D:/python/csv/六合csv_merge'
csvmonth_path = f'D:/python/csv/六合csv_merge/{year}年{month}月'

def create_dir ():
    isExists=os.path.exists(merge_path)
    if not isExists:
        os.mkdir(merge_path)

    isExists=os.path.exists(csvmonth_path)    
    if not isExists:
        os.mkdir(csvmonth_path)
 
def delete_csv():
    csvdir = os.listdir(path) 
    for fname in csvdir: 
        if fname.endswith(".csv"): 
           os.remove(f'{path}/{fname}')

def check_url(): 
    urllist = ["16c25.com","16c26.com","16c21.com","608tk5.com","608tk3.com","608tk17.com","608tk18.com",'16c.com','16c22.com','16c4.com','16c13.com','676813.com','676360.com','608tk16.com','608tk.com','608tk2.com','608tk6.com','676813a.com','676360a.com','16c45.com'] 
    headers  = ["日期","16c25.com","16c26.com","16c21.com","608tk5.com","608tk3.com","608tk17.com","608tk18.com",'16c.com','16c22.com','16c4.com','16c13.com','676813.com','676360.com','608tk16.com','608tk.com','608tk2.com','608tk6.com','676813a.com','676360a.com','16c45.com'] 
    tmp = [] 
    with open(f'{path}/{today}六合.csv', 'w' ,newline='' ,encoding='utf-8-sig') as csvfile:  
        writer = csv.writer(csvfile) 
        writer.writerow(headers) 
        

        for check in urllist :  
            url = f'https://www.boce.com/hijack/{check}'  
            html = requests.get(url)  
            html.encoding="utf-8"  
            soup = BeautifulSoup(html.text, 'html.parser') 
            link2 = soup.find('b', class_='font18 font18s').get_text() 
            link2 = int(link2)

            if  link2 != 0 :   
                link1 = soup.find('span', class_='font18').get_text() 
                link2 = soup.find('b', class_='font18 font18s').get_text() 
                link3_tmp = soup.find_all('b', class_='font18') 
                link3_tmp2 = (link3_tmp[2]) 
                link3 = (link3_tmp2).get_text() 
                 
                urlstr =  ''.join(check) 
                writer = csv.writer(csvfile) 
                urlno = (f"{link1}\n劫持节点数:{link2}個\n劫持占比:{link3}") 
                tmp.append(urlno) 
     
            if link2 == 0 :      
                urlok = soup.find('span', class_='page10c').get_text() 
                writer = csv.writer(csvfile)    
                tmp.append(urlok)

        writer.writerow([f"{today}"] + tmp) 
               
def merge_csv(): 
    csvdir = os.listdir(path) 
    merdir = os.listdir(csvmonth_path) 
    csv_list = [] 

    for fname in merdir :    # 先讀取當月的CSV合併的CSV 檔案放入列表
        if fname.endswith(".csv"): 
            fname = f'{csvmonth_path}/{fname}'
            csv_list.append(pd.read_csv(f'{fname}'))

    for fname in csvdir :  # 再把當日讀取到的劫持,加在後面  ( 假設先讀取合併裡的 1~5日資料 , 再把讀到的6日資料放在同一個列表 )
        if fname.endswith(".csv"): 
            fname = f'{path}/{fname}'
            csv_list.append(pd.read_csv(f'{fname}'))


    csv_all = pd.concat(csv_list ,axis = 0 ,join='outer',)  # 0 = row  1 = colume 
    csv_all.to_csv( f'{csvmonth_path}/六合{month}月合併.csv' ,index=False , encoding="utf_8_sig" )  # utf_8_sig  sig才能辨識亂碼

def gswrite(): 
    scope = ['https://www.googleapis.com/auth/spreadsheets'] 
    cred_path = f"{path}/pandas-376711-c5147153f890.json" 
    creds = Credentials.from_service_account_file( cred_path, scopes=scope) 
    gs = gspread.authorize(creds) 
    sheet = gs.open_by_url('https://docs.google.com/spreadsheets/d/1f8DMfBRL_qmfETKdLC7t_EzCXLJwmivQBN7wLDpnxPU/edit#gid=0') 
     
    worksheet = sheet.get_worksheet(sheet_work) 
    df = pd.read_csv(f'{csvmonth_path}/六合{month}月合併.csv') 
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())


create_dir ()
delete_csv()
time.sleep(2)
check_url()
merge_csv()
# gswrite()






