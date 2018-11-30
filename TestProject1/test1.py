# -*- coding: utf-8 -*-
from selenium import webdriver
import time,os

def Input_Cookies(username):
    driver = webdriver.Chrome(executable_path='e://chromedriver.exe')
    driver.get('http://jsf.th.jd.com/')
    driver.implicitly_wait(10)
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys("!Conglin01")
    time.sleep(1)
    driver.find_element_by_xpath(".//input[@type='submit']").click()
    time.sleep(3)
    assert "退出" in driver.page_source
    time.sleep(1)
    Cookies=driver.get_cookies()
    print(Cookies)
    project_path=os.path.dirname(os.path.dirname(__file__))
    cookie_path=os.path.join(project_path,username+'.txt')
    cookies={}
    for tmp_dict in Cookies:
        cookies[tmp_dict["name"]]=tmp_dict["value"]
    with open(cookie_path,'w') as f:
        f.write(str(cookies))
    time.sleep(2)
    driver.quit()



def Get_Cookies(username):
    project_path=os.path.dirname(os.path.dirname(__file__))
    cookie_path=os.path.join(project_path,username+'.txt')
    with open(cookie_path,'r') as f:
        cookies=eval(f.read())
    return cookies



if __name__=="__main__":
    Input_Cookies("conglin8")
    print("-----------------------")
    print (Get_Cookies("conglin8"))