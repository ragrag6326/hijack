from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time
import requests  
import datetime 
import time 
import glob 
from PIL import Image 
import pytesseract
import pyotp
from bs4 import BeautifulSoup



today = time.strftime('%m-%d')  
day = time.strftime('%m月%d號')

PATH = "C:/Users/AllenHsu許鼎/Desktop/截圖/騰訊/driver/chromedriver.exe"
driver = webdriver.Chrome(PATH)
wait = WebDriverWait(driver, 10)  


# --------- check_vpn -------------
def vpn_check () :
    url = f'https://iplocation.com/' 
    html = requests.get(url) 
    html.encoding="utf-8" 
    soup = BeautifulSoup(html.text, 'html.parser')
    
    global ip
    ip = soup.find('b', class_='ip').get_text()

    if ip != "18.163.58.218" :
        raise ValueError ("vpn錯誤")

# --------- login -------------
def login ():

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


def domain (domains):
    times = 0
    
    for domain in domains :
        try :
            field = wait.until(lambda driver: driver.find_element(By.NAME ,'host'))
            field.clear()
            field.send_keys(f'{domain}')
            field.send_keys(Keys.RETURN)

            time.sleep(70)
            times += 1 
    
        except :
            tg_send(f"六合劫持檢測 執行到 {domains[times]} 時失敗") 
            break




def retry (retry):
    tmp = []
    for domains in retry :
        url = f'https://www.boce.com/hijack/{domains}'  
        html = requests.get(url)  
        html.encoding="utf-8"  
        soup = BeautifulSoup(html.text, 'html.parser') 
        time = soup.find('span', class_='font14 color999 rs_detail_checktime').get_text() 
        hijack_today = time[5:10]   # 看域明劫持的日期 

        if hijack_today != today :    # 如果列表中劫持沒跑成功的話 , 劫持檢測日期不會是今天日期 , 就不會放入列表中
            tmp.append(domains)

    try:
        domain (tmp)    # 再把還沒檢測的過的域名重新跑一次劫持

    except:
        tg_send('六合劫持重新嘗試失敗')

    else:
        tg_send('六合劫持重新嘗試成功')


def tg_send (message):
    # -593254743截圖bot   -851230000 測試 
    text = (f"{day} - {message}")
    send_text = requests.post(f'https://api.telegram.org/bot5945260654:AAHmq9cVBqGMD5BTTs7vcNTKiYVPBTz2taM/sendMessage?chat_id=-851230000&&parse_mode=Markdown&text={text}')
    print(send_text.status_code) 


# 放入需要檢測劫持的 domain
urlist = ["16c25.com","16c26.com","16c21.com","608tk5.com","608tk3.com","608tk17.com","608tk18.com","16c.com","16c22.com","16c4.com","16c13.com","676813.com","676360.com","608tk16.com","608tk.com","608tk2.com","608tk6.com","676813a.com","676360a.com"] 

try :
    login ()
    domain(urlist)

except:
    retry(urlist)

else:
    tg_send('六合劫持檢測完成')




# os.system('taskkill /F /IM conhost.exe')