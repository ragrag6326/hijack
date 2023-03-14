from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests  
import time 
from bs4 import BeautifulSoup
import subprocess 


today = time.strftime('%m-%d')  
day = time.strftime('%m月%d號')

vpn_path = 'C:/Users/hengyi/Desktop/雲支付劫持檢測/vpn'
PATH = "C:/Users/AllenHsu許鼎/Desktop/截圖/騰訊/driver/chromedriver.exe"
driver = webdriver.Chrome(PATH)
wait = WebDriverWait(driver, 10)  


# -593254743 截圖bot  -851230000 測試 
chat_id = -863091203



# --------- 連openvpn -------------
def connect_openvpn():

    subprocess.call([rf'{vpn_path}/connect_vpn.bat'])
    time.sleep(10)

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
        tg_send('雲支付檢測 login時發生錯誤 , 請重新檢查元素' , chat_id)

# 放入域名跑劫持
def domain (domains):
    times = 0                  #  times=0 用來辨識現在執行到多少次 到哪條域名
    long = int(len(domains))   #  long 用來辨識 傳進來的 domains 有多少條
    
    for domain in domains :    # 執行迴圈檢測域名 
        try :                  # 使用 try 檢測代碼是否有異常 
            field = wait.until(lambda driver: driver.find_element(By.NAME ,'host'))   
            field.clear()
            field.send_keys(f'{domain}')
            field.send_keys(Keys.RETURN)

            time.sleep(2)
            check = wait.until(lambda driver: driver.find_element(By.XPATH ,'/html/body/div[1]/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[1]/b'))
            check.click()

            time.sleep(70)
            times += 1 
    
        except BaseException :   # 代碼執行失敗時會直接跳到 except ,然而 times 不會+1 此時就能判斷是在哪條域名執行失敗
            tg_send(f"雲支付劫持檢測 執行到 {domains[times]} 時失敗 , 正在重新嘗試" , chat_id)
            raise ValueError ('network delay or element not found')  # 發起錯誤接著跳到 retry 中,再嘗試一次
    
        if times == long :      # (times 執行次數) 如果 等於 (long 傳進來domains N條)  , 就代表執行成功
                                # 由於 try 執行成功 times會+1 , +1後就會大於long長度 , 所以要再把它-1 扣回去
            tg_send(f"雲支付劫持檢測執行成功 到 {domains[times-1]} 時結束" , chat_id)
            

def retry (retry):

    tmp = []
    for domains in retry :
        url = f'https://www.boce.com/hijack/{domains}'  
        html = requests.get(url)  
        html.encoding="utf-8"  
        soup = BeautifulSoup(html.text, 'html.parser') 
        day = soup.find('span', class_='font14 color999 rs_detail_checktime').get_text() 
        hijack_today = day[5:10]   # 看域名劫持的日期 

        if hijack_today != today :    # 如果列表中劫持沒跑成功的話 , 劫持檢測日期不會是今天日期 , 就不會放入列表中
            tmp.append(domains)     # 日期不是今天的才會放入此list中
        
    try:
        time.sleep(20)
        domain (tmp)    # 再把還沒檢測的過的域名重新跑一次劫持

    except:         # 如果重新檢測又失敗則報錯
        tg_send('重新嘗試失敗' , chat_id)

    else:
        tg_send('重新嘗試成功,所有域名檢測已檢測完成' , chat_id)


def tg_send (message ,chat_id):
    # -593254743截圖bot   -851230000 測試 
    text = (f"{day} - {message}")
    send_text = requests.post(f'https://api.telegram.org/bot5945260654:AAHmq9cVBqGMD5BTTs7vcNTKiYVPBTz2taM/sendMessage?chat_id={chat_id}&&parse_mode=Markdown&text={text}')
    print(send_text.status_code) 





# 放入需要檢測劫持的 domain
urlist = ["07786aaa.com","07786bbb.com","07786ccc.com","07786ddd.com","07786eee.com","07786fff.com","07786ggg.com","07786hhh.com","07786jjj.com","07786kkk.com","07786mmm.com","07786nnn.com","07786ppp.com","07786qqq.com"] 
# urlist = ["07786qqq.com"]

try :
    login ()
    domain(urlist)

except ValueError:
    retry(urlist)

else:
    tg_send('雲支付劫持檢測完成' , chat_id)




# os.system('taskkill /F /IM conhost.exe')