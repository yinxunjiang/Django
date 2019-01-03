from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from Apply1.models import Event,Guest #导入模型文件中的模型类
from django.db.models import Q,F
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from datetime import datetime
import requests,re

def index(request):
    return render(request,"index.html")

# 登录动作
def login_action(request):
    if request.method=="POST":
        username=request.POST.get("username","")
        password=request.POST.get("password","")
        user=auth.authenticate(username=username,password=password)  # 获取登录信息
        if user is not None:
            auth.login(request,user)  # 登录
            request.session["user"]=username
            response=HttpResponseRedirect("/event_manage/")
            return response
        else:
            return render(request,"index.html",{"error":"用户名或密码错误"})
# 发布会管理页面
@login_required
def event_manage(request):
    # 获取所有发布会对象数据
    event_list=Event.objects.all()
    # 获取浏览器中的session
    username=request.session.get("user","")
    return render(request,"event_manage.html",{"user":username,"events":event_list})
#发布会搜索视图
@login_required
def search_name(request):
    username = request.session.get("user", "")
    search_name=request.GET.get("name","")
    event_list=Event.objects.filter(name__contains=search_name)
    return render(request,"event_manage.html",{"user":username,"events":event_list})
#嘉宾页面
@login_required
def guest_manage(request):
     # 获取所有嘉宾数据
    guest_list=Guest.objects.all()
    # 获取浏览器中的user session
    username=request.session.get("user","")
     #定义分页类对象
    paginator=Paginator(guest_list,5)
     #根据get请求中url的参数page获取当前的页数
    page=request.GET.get("page")
    try:
        #根据获取到的页数来获取某一页的对象数据
        contacts=paginator.page(page)
    except PageNotAnInteger:
        #如果没有page页，则会抛出PageNotAnInteger异常，此时让其返回第一页数据
        contacts=paginator.page(1)
    except EmptyPage:
        #如果page超出范围，将会抛出EmptyPage异常，此时让其返回最后一页数据
        contacts=paginator.page(paginator.num_pages)
    return render(request,"guest_manage.html",{"user":username,"guests":contacts})
#嘉宾搜索视图
@login_required
def search_guest(request):
    # 获取session中获取user信息
    username = request.session.get("user", "")
    #获取浏览器中的搜索关键词
    search_name=request.GET.get("key","")
    #将关键词信息存到session里，起名keyword
    request.session["keyword"] = search_name
    #从session中获取关键词信息
    keyword=request.session.get("keyword")
    #获取搜索结果
    guest_list=Guest.objects.filter(Q(realname__contains=search_name)|Q(phone__contains=search_name))
    # 定义分页类对象
    paginator = Paginator(guest_list, 5)
    # 根据get请求中url的参数page获取当前的页数
    page = request.GET.get("page")
    try:
        # 根据获取到的页数来获取某一页的对象数据
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果没有page页，则会抛出PageNotAnInteger异常，此时让其返回第一页数据
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果page超出范围，将会抛出EmptyPage异常，此时让其返回最后一页数据
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts, "keyword":keyword})

#签到页面
@login_required
def sign_index(request,eid):
    event=get_object_or_404(Event,id=eid)
    return render(request,"sign_index.html",{"event":event})
#签到动作
@login_required
def sign_index_action(request,eid):
    event = get_object_or_404(Event, id=eid)
    phone=request.POST.get("phone","")
    result=Guest.objects.filter(phone=phone)
    if not result:
        return render(request,"sign_index.html",{"event":event,"hint":"没有此手机号信息"})
    result=Guest.objects.filter(phone=phone,event_id=eid)
    if not result:
        return render(request,"sign_index.html",{"event":event,"hint":"手机号与发布会信息不匹配"})
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, "sign_index.html", {"event": event, "hint": "嘉宾已签到"})
    else:
        Guest.objects.filter(phone=phone,event_id=eid).update(sign=1)
        return render(request, "sign_index.html", {"event": event, "hint": "签到成功","guest":result})

#退出登录
@login_required
def logout(request):
    auth.logout(request)
    response=HttpResponseRedirect('/index/')
    return response

#添加嘉宾
def add_guest(request):
    event_list=Event.objects.all()
    if request.method == "POST":
        selected = request.POST.get("dropdown","")
        realname=request.POST.get("realname","")
        phone=request.POST.get("phone","")
        email=request.POST.get("email","")
        sign=request.POST.get("sign","")
        #print(selected,realname,phone,email,sign)
        if sign:
            sign=True
        else:
            sign=False
        #print(selected, realname, phone, email, sign)
        guest=Guest.objects.filter(phone=phone,event_id=selected)
        #guest=get_object_or_404(Guest,phone=phone,event_id=selected)
        print(guest)
        if guest:
            return render(request, "add_guest.html", {"events": event_list,"hint":"用户已登记此发布会","flag":"red"})
        else:
            Guest.objects.create(event_id=selected,realname=realname,phone=phone,email=email,sign=sign)
            return render(request, "add_guest.html", {"events": event_list, "hint": "用户登记成功","flag":"green"})
    else:
        return render(request,"add_guest.html",{"events":event_list})


#获取bug列表
def jira(request):
    if request.method == "POST":
        jira_name = request.POST.get("jiraname","")
        jira_password=request.POST.get("jirapassword","")
        # jd_user = auth.authenticate(username=jira_name, password=jira_password)  # 获取登录信息
        # request.session["jd_user"] = jira_name
        jira_id=request.POST.get("jiraid","")
        payload = {}
        payload["os_username"] = jira_name
        payload["os_password"] = jira_password
        jira_id =jira_id
        result = requests.post("http://jira.jd.com/rest/gadget/1.0/login", data=payload)
        cookies = result.cookies
        result = requests.post("http://jira.jd.com/browse/NEWPOPV-{jiraid}".format(jiraid=jira_id), cookies=cookies)
        bug_list = re.findall(r"<span title=\"(NEWPOPV.*?)\">", str(result.content, encoding="utf-8"))
        return render(request, "jira.html", {"bugs":bug_list})
    else:
        bug_list=[]
        return render(request, "jira.html", {"bugs":bug_list})