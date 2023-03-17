from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import requests  
import time 
from bs4 import BeautifulSoup
import subprocess 



# -593254743 截圖bot  -851230000 測試  863091203
chat_id = -851230000
project = '雲支付'


today = time.strftime('%m-%d')  
day = time.strftime('%m月%d號')

vpn_path = f'C:/Users/hengyi/Desktop/{project}劫持檢測/vpn'
PATH = f"C:/Users/hengyi/Desktop/{project}劫持檢測/driver/chromedriver.exe"
driver = webdriver.Chrome(PATH)
wait = WebDriverWait(driver, 10)  


# --------- 連openvpn -------------
def connect_openvpn():

    subprocess.call([rf'{vpn_path}/connect_vpn.bat'])
    time.sleep(15)

# ------------- 關openvpn -------------
def disconnect_openvpn():

    subprocess.call([rf'{vpn_path}/disconnect_vpn.bat'])
    time.sleep(5)

# --------- login -------------
def login ():
    try:
        driver.get("https://boce.com/user/#/login") 
        time.sleep(1)
        driver.maximize_window()
        time.sleep(1)


        username = wait.until(lambda driver: driver.find_element(By.XPATH , '//*[@id="pane-account"]/form/div[1]/div/div/input'))
        username.clear()
        username.send_keys('13643860728')
    

        password = wait.until(lambda driver: driver.find_element(By.XPATH , '//*[@id="pane-account"]/form/div[2]/div/div[1]/input'))
        password.clear()
        password.send_keys('A13643860728z')


        login = wait.until(lambda driver: driver.find_element(By.XPATH ,'//*[@id="app"]/div[1]/div[2]/div/div[2]/div/div[1]/div[3]/div/button'))
        login.click()
        time.sleep(1)

        logo = wait.until(lambda driver: driver.find_element(By.XPATH ,'//*[@id="app"]/section/header/div/div[1]/a'))
        logo.click()
        time.sleep(1)

        check = wait.until(lambda driver: driver.find_element(By.XPATH ,'/html/body/div[1]/div[3]/div[1]/div[2]/form[2]/div[1]/span[4]/a'))
        check.click()
        time.sleep(1)
    except:
        tg_send(f'{project}檢測 login時發生錯誤 , 請重新檢查元素' , chat_id)

# 放入域名跑劫持
def domain (domains):

    check_date = check(domains)
    
    times = 0
    long = int(len(check_date))

    for domain in check_date :
        try :
            field = wait.until(lambda driver: driver.find_element(By.NAME ,'host'))
            field.clear()
            field.send_keys(f'{domain}')
            field.send_keys(Keys.RETURN)
            
            time.sleep(2)
            check = wait.until(lambda driver: driver.find_element(By.XPATH ,'/html/body/div[1]/div[1]/div[1]/div[1]/div/div[2]/div[2]/div[1]/b'))
            check.click()
            
            time.sleep(80)
            times += 1 
    
        except BaseException:
            disconnect_openvpn()
            tg_send(f"{project}劫持檢測 執行到 {check_date[times]} 時失敗 , 正在重新嘗試" , chat_id)
            raise ValueError ('network delay or element not found')

        
        if times == long :
            tg_send(f"{project}劫持檢測執行成功 到 {check_date[times-1]} 時結束" , chat_id)


def check (check):

    tmp = []
    for domains in check :
        url = f'https://www.boce.com/hijack/{domains}'  
        html = requests.get(url)  
        html.encoding="utf-8"  
        soup = BeautifulSoup(html.text, 'html.parser') 
        day = soup.find('span', class_='font14 color999 rs_detail_checktime').get_text() 
        hijack_today = day[5:10]   

        if hijack_today != today :   
            tmp.append(domains)     
        
    return tmp


def retry (retry):

    try:
        time.sleep(20)
        domain (retry)  

    except ValueError:
        tg_send(f'{project}劫持檢測,重新嘗試失敗' , chat_id)

    else:
        tg_send(f'{project}劫持檢測,重新嘗試成功,所有域名劫持日期為{today}檢查完畢正確' , chat_id)


def tg_send (message , chat_id ):
    # -593254743截圖bot   -851230000 測試 
    text = (f"{day} - {message}")
    send_text = requests.post(f'https://api.telegram.org/bot5945260654:AAHmq9cVBqGMD5BTTs7vcNTKiYVPBTz2taM/sendMessage?chat_id={chat_id}&&parse_mode=Markdown&text={text}')
    print(send_text.status_code) 





# 放入需要檢測劫持的 domain
urlist = ["07786aaa.com","07786bbb.com","07786ccc.com","07786ddd.com","07786eee.com","07786fff.com","07786ggg.com","07786hhh.com","07786jjj.com","07786kkk.com","07786mmm.com","07786nnn.com","07786ppp.com","07786qqq.com"] 


try :
    connect_openvpn()
    login ()
    domain(urlist)

except ValueError:
    retry(urlist)

else:
    disconnect_openvpn()
    tg_send(f'{project}劫持檢測完成' , chat_id)




os.system('taskkill /F /IM conhost.exe')