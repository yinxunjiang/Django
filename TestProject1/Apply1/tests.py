#encoding=utf-8
from django.test import TestCase
# Create your tests here.
from selenium import webdriver
import time
class TestScript(TestCase):
    def setUp(self):
        self.driver=webdriver.Chrome(executable_path="e:/chromedriver.exe")
    def test1(self):
        self.driver.get("http://www.baidu.com")
        self.driver.find_element_by_id("kw").send_keys("jd")
        time.sleep(3)
        self.driver.find_element_by_id("su").click()
        time.sleep(3)
    def tearDown(self):
        self.driver.quit()

