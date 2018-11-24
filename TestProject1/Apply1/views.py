from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from Apply1.models import Event,Guest #导入模型文件中的模型类
from django.db.models import Q,F
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

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
    paginator=Paginator(guest_list,2)
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
    paginator = Paginator(guest_list, 2)
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

