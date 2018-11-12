from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from Apply1.models import Event,Guest #导入模型文件中的模型类

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
