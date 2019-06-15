# -*- coding: utf-8 -*-
str="123456789"
s1=str[0:3]
s2=str[3:6]
s3=str[6:]
print(s1[::-1]+s2[::-1]+s3[::-1])

tmp=[]
result=[]
n=0
for i in range(len(str)):
    n+=1
    tmp.append(str[i])
    if n==3:
        str_tmp=''.join(tmp[::-1])
        result.append(str_tmp)
        tmp=[]
        n=0
print(''.join(result))






