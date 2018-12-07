# -*- coding: utf-8 -*-
from selenium import webdriver
from datetime import datetime
import requests,re,urllib

payload={}
payload["os_username"]="yinxunjiang"
payload["os_password"]="Woainini@520"

result=requests.post("http://jira.jd.com/rest/gadget/1.0/login",data=payload)
#print(result.content.decode("utf-8"))
cookies=result.cookies
#print(cookies)
jira_id="NEWPOPV-7286"
result=requests.post("http://jira.jd.com/browse/{jiraid}".format(jiraid=jira_id),cookies=cookies)

#print(result.content.decode("utf-8"))
r=re.findall(r"<span title=\"(NEWPOPV.*?)\">",str(result.content,encoding="utf-8"))
for i in r:
    print(i)