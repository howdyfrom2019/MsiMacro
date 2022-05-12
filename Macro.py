import re
import time
import easyocr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome('./chromedriver.exe')
driver_time = webdriver.Chrome('./chromedriver.exe')

driver.set_window_size(720, 620)
driver.get(
    'https://ticket.interpark.com/Gate/TPLogin.asp?CPage=B&MN=Y&tid1=main_gnb&tid2=right_top&tid3=login&tid4=login')

time.sleep(1)
driver.switch_to.frame(driver.find_element(By.XPATH, "//div[@class='leftLoginBox']/iframe[@title='login']"))
userId = driver.find_element(By.ID, 'userId')
userId.send_keys('ID')
userPwd = driver.find_element(By.ID, 'userPwd')
userPwd.send_keys('PWD')
userPwd.send_keys(Keys.ENTER)

# driver.get('https://tickets.interpark.com/goods/22005090')
driver.get('https://tickets.interpark.com/goods/22005185')

# driver.find_element(By.XPATH, "//div[@class='popupWrap']/div[@class='popupFooter']/button").click()

driver_time.get("https://time.navyism.com/?host=ticket.interpark.com")
driver_time.find_element(By.ID, 'msec_title').click()

while True:
    a = driver_time.find_element(By.XPATH, "//*[@id='time_area']").text
    b = driver_time.find_element(By.XPATH, "//*[@id='msec_area']").text

    timer = re.findall("[0-9]+", a)
    # if timer[4] == '59' and timer[5] == '59':
    if timer[5] == '59':
        msec = re.findall("[0-9]+", b)
        if int(msec[0]) >= 800:
            # driver.get('https://tickets.interpark.com/goods/22005090')
            driver.get('https://tickets.interpark.com/goods/22005185')
            driver.find_elements(By.XPATH, "//ul[@data-view='days']/li")[15].click()
            driver.find_element(By.XPATH, "//div[@class='sideBtnWrap']/a[@class='sideBtn is-primary']").click()

            time.sleep(1)
            driver.switch_to.window(driver.window_handles[1])
            driver.switch_to.frame(driver.find_element(By.ID, 'ifrmSeat'))
            try:
                capcha = driver.find_element(By.ID, 'imgCaptcha')
                reader = easyocr.Reader(['en'])
                result = reader.readtext(capcha.screenshot_as_png, detail=0)
                capchaValue = result[0].replace(' ', '').replace('5', 'S').replace('0', 'O').replace('$', 'S').replace(
                    ',', '') \
                    .replace(':', '').replace('.', '').replace('+', 'T').replace("'", '').replace('`', '') \
                    .replace('1', 'L').replace('e', 'Q').replace('3', 'S').replace('€', 'C').replace('{', '').replace(
                    '-', '')
                driver.find_element_by_class_name('validationTxt').click()
                capchaText = driver.find_element_by_id('txtCaptcha')
                capchaText.send_keys(capchaValue)
                capchaText.send_keys(Keys.ENTER)
            except NoSuchElementException:
                print("capcha doesn't exist")
            time.sleep(1)
            driver.switch_to.frame(driver.find_element(By.ID, 'ifrmSeatDetail'))
            seats = driver.find_elements(By.CLASS_NAME, "stySeat")

            count = 0
            for seat in seats:
                seat.click()
                count += 1
                if count == 2:
                    break
            driver.switch_to.parent_frame()
            driver.find_element(By.XPATH, "//div[@class='btnWrap']/a").click()
            break
