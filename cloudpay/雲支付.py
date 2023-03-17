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

project = '雲支付'
# tg發送 -593254743 截圖bot   -851230000 測試   -863091203
chat_id = -851230000


today = time.strftime('%m-%d')  
year = time.strftime('%Y') 
month = time.strftime('%m') 
month = (month[1]) 
sheet_work = int(month) - 1 
master_df = pd.DataFrame() 


path = 'C:/Users/截圖test/Desktop/表單填寫'
merge_path = f'C:/Users/截圖test/Desktop/表單填寫/{project}csv_merge'
csvmonth_path = f'C:/Users/截圖test/Desktop/表單填寫/{project}csv_merge/{year}年{month}月'


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

def check_url(domainlist): 
    headers  = ['日期'] + domainlist
    tmp = [] 
    with open(f'{path}/{today}{project}.csv', 'w' ,newline='' ,encoding='utf-8-sig') as csvfile:  
        writer = csv.writer(csvfile) 
        writer.writerow(headers) 
        
        for check in domainlist :    # 把所有domain放入迴圈 去做檢測
            url = f'https://www.boce.com/hijack/{check}'  
            html = requests.get(url)  
            html.encoding="utf-8"  
            soup = BeautifulSoup(html.text, 'html.parser') 
            link2 = soup.find('b', class_='font18 font18s').get_text()    # 判斷劫持數量 轉化成文字
            link2 = int(link2)

            if  link2 != 0 :   
                link1 = soup.find('span', class_='font18').get_text() 
                link2 = soup.find('b', class_='font18 font18s').get_text() 
                link3_tmp = soup.find_all('b', class_='font18') 
                link3_tmp2 = (link3_tmp[2]) 
                link3 = (link3_tmp2).get_text() 
                 
                urlstr =  ''.join(check) 
                writer = csv.writer(csvfile) 
                urlno = (f"{link1}\n劫持节点数: {link2}個\n劫持占比: {link3}%") 
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
    for fname in merdir :   
        if fname.endswith(".csv"): 
            fname = f'{csvmonth_path}/{fname}'
            csv_list.append(pd.read_csv(f'{fname}'))

    for fname in csvdir :  
        if fname.endswith(".csv"): 
            fname = f'{path}/{fname}'
            csv_list.append(pd.read_csv(f'{fname}'))

    
    csv_all = pd.concat(csv_list ,axis = 0 ,join='outer',)  # 0 = row  1 = colume 
    csv_all.to_csv( f'{csvmonth_path}/{project}{month}月合併.csv' ,index=False , encoding="utf_8_sig" )  # utf_8_sig  sig才能辨識亂碼

def gswrite(): 
    
    scope = ['https://www.googleapis.com/auth/spreadsheets'] 
    cred_path = f"{path}/pandas-376711-c5147153f890.json" 
    creds = Credentials.from_service_account_file( cred_path, scopes=scope) 
    
    gs = gspread.authorize(creds) 
    sheet = gs.open_by_url('https://docs.google.com/spreadsheets/d/1xRK_Q4Eb_j9qSJEXLi5ERNBsa1MuwhlKJawG2cg6hCg/edit#gid=0') 
     
    worksheet = sheet.get_worksheet(sheet_work)  
    df = pd.read_csv(f'{csvmonth_path}/{project}{month}月合併.csv') 
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

def check_csv ():
    try:
        data = pd.read_csv(f'{csvmonth_path}/{project}{month}月合併.csv')
        date = data['日期'].max()
        if date == today :
            raise ValueError ("資料已填寫完成")
        else:
            merge_csv()

    except FileNotFoundError as err:
        print ("未找到檔案正在創建中")
        merge_csv()

def tg_send(message , chat_id ):
    text = (f"{today} - {message}")
    send_text = requests.post(f'https://api.telegram.org/bot5945260654:AAHmq9cVBqGMD5BTTs7vcNTKiYVPBTz2taM/sendMessage?chat_id={chat_id}&&parse_mode=Markdown&text={text}')
    print(send_text.status_code) 



# 在此更換 domain
domainlist = ["07786aaa.com","07786bbb.com","07786ccc.com","07786ddd.com","07786eee.com","07786fff.com","07786ggg.com","07786hhh.com","07786jjj.com","07786kkk.com","07786mmm.com","07786nnn.com","07786ppp.com","07786qqq.com"] 


try : 
    create_dir ()
    delete_csv()
    time.sleep(2)
    check_url(domainlist)
    check_csv ()
    gswrite()

except ValueError :
    tg_send(f"{project}表單已填寫完成", chat_id)

except:
    tg_send(f"{project}劫持表單填寫失敗", chat_id)

else:
    tg_send(f"{project}劫持表單填寫成功\nhttps://docs.google.com/spreadsheets/d/1f8DMfBRL\_qmfETKdLC7t\_EzCXLJwmivQBN7wLDpnxPU/edit#gid=1770078190", chat_id)

