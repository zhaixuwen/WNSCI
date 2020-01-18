import requests
from selenium import webdriver
from common import utility


def test_login_gui():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('http://localhost:8080/woniusales/')
    driver.find_element_by_id('username').send_keys('admin')
    driver.find_element_by_id('password').send_keys('admin123')
    driver.find_element_by_id('verifycode').send_keys('0000')
    driver.find_element_by_xpath('/html/body/div[4]/div/form/div[6]/button').click()
    if driver.current_url == 'http://localhost:8080/woniusales/sell':
        utility.write_report('登录（GUI）', '成功')
    else:
        utility.write_report('登录（GUI）', '失败')
        print(driver.current_url)
    driver.close()

def test_login_http():
    data = {'username': 'admin', 'password': 'admin123', 'verifycode': '0000'}
    resp = requests.post('http://localhost:8080/woniusales/login', data=data)
    if resp.status_code == 200:
        utility.write_report('登录（HTTP）', '成功')
    else:
        utility.write_report('登录（HTTP）', '失败')