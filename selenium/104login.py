from selenium import webdriver
# ActionChains是模擬滑鼠操作的套件
from selenium.webdriver.common.action_chains import ActionChains

# 進入首頁
url='https://www.104.com.tw/jobs/main/'
path='C:\\Users\\Jeffery\\.conda\\envs\\Bot_training\\chromedriver.exe'
driver = webdriver.Chrome(executable_path=path)
driver.get(url)
# 點擊登入進到登入頁面
login = driver.find_element_by_link_text('登入')
ActionChains(driver).click(login).perform()
# 輸入帳號密碼
driver.find_element_by_id('username').send_keys('your email or ID')
driver.find_element_by_id('password').send_keys('your p@ssword')
# 點擊登入按鈕
driver.find_element_by_id('submitBtn').submit()
