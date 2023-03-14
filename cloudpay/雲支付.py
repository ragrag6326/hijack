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
merge_path = 'D:/python/csv/雲支付csv_merge'
csvmonth_path = f'D:/python/csv/雲支付csv_merge/{year}年{month}月'

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
    urllist = ["07786aaa.com","07786bbb.com","07786ccc.com","07786ddd.com","07786eee.com","07786fff.com","07786ggg.com","07786hhh.com","07786jjj.com","07786kkk.com","07786mmm.com","07786nnn.com","07786ppp.com","07786qqq.com",] 
    headers  = ["日期","07786aaa.com","07786bbb.com","07786ccc.com","07786ddd.com","07786eee.com","07786fff.com","07786ggg.com","07786hhh.com","07786jjj.com","07786kkk.com","07786mmm.com","07786nnn.com","07786ppp.com","07786qqq.com"] 
    tmp = [] 
    with open(f'{path}/{today}雲支付.csv', 'w' ,newline='' ,encoding='utf-8-sig') as csvfile:  
        writer = csv.writer(csvfile) 
        writer.writerow(headers) 
        

        for check in urllist :    # 把所有domain放入迴圈 去做檢測
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
    for fname in merdir :   # 先讀取當月的CSV合併的CSV 檔案放入列表
        if fname.endswith(".csv"): 
            fname = f'{csvmonth_path}/{fname}'
            csv_list.append(pd.read_csv(f'{fname}'))

    for fname in csvdir :  # 再把當日讀取到的劫持,加在後面  ( 假設先讀取合併裡的 1~5日資料 , 再把讀到的6日資料放在同一個列表 )
        if fname.endswith(".csv"): 
            fname = f'{path}/{fname}'
            csv_list.append(pd.read_csv(f'{fname}'))

    # 最後把 今日跟 ~至今寫入csv_list列表 ,再將合併完成的列表寫入新的csv檔案
    csv_all = pd.concat(csv_list ,axis = 0 ,join='outer',)  # 0 = row  1 = colume 
    csv_all.to_csv( f'{csvmonth_path}/雲支付{month}月合併.csv' ,index=False , encoding="utf_8_sig" )  # utf_8_sig  sig才能辨識亂碼

def gswrite(): 
    # 於 Google 擁有許多的雲端服務，所以需要定義存取的Scope(範圍)，也就是 Google Sheets(試算表)：
    scope = ['https://www.googleapis.com/auth/spreadsheets'] 

    # 指定剛下載的JSON憑證檔位置 , 與 Scope(範圍)傳入 google-auth 套件的 Credentails 模組，來建立憑證物件
    cred_path = f"{path}/pandas-376711-c5147153f890.json" 
    creds = Credentials.from_service_account_file( cred_path, scopes=scope) 
    
    # gspread模組的authorize()方法進行驗證
    gs = gspread.authorize(creds) 

    # 驗證沒問題，就可以呼叫 gspread 模組的open_by_url()方法，傳入Google Sheets試算表的網址，來執行開啟的動作
    sheet = gs.open_by_url('https://docs.google.com/spreadsheets/d/1xRK_Q4Eb_j9qSJEXLi5ERNBsa1MuwhlKJawG2cg6hCg/edit#gid=0') 
     

    # 如果要以月份來做工作表區分 , 以當(月month) - 1 , 因為python是從0開始算起 工作表
    worksheet = sheet.get_worksheet(sheet_work)  

    # 模擬 Pandas DataFrame 寫入資料到 Google Sheets 試算表，所以 Pandas DataFrame 今天蒐集的域名劫持 "合併.csv"，透過read_csv()方法進行讀取
    df = pd.read_csv(f'{csvmonth_path}/雲支付{month}月合併.csv') 

    # Pandas DataFrame 中有了資料後，就可以呼叫gspread模組的 update()方法，分別將欄位 "名稱" 與資料 "內容" 寫入Google Sheets試算表
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())


create_dir ()
delete_csv()
time.sleep(2)
check_url()
merge_csv()
# gswrite()





