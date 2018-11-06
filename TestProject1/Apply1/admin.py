from django.contrib import admin
from Apply1.models import Event,Guest  # 导入models.py模块定义的模型类
# Register your models here.
#定义列表显示的字段
class EventAdmin(admin.ModelAdmin):
    list_display = ['id','name','status','address','start_time','limit']
    search_fields = ['name'] #定义搜素栏
    list_filter = ['status']#定义过滤器
class GuestAdmin(admin.ModelAdmin):
    list_display = ['id','realname','phone','email','sign']
    search_fields = ['realname','phone']#定义搜素栏,可定义多个值
    list_filter = ['sign']#定义过滤器,可定义多个值
#将列表应用于模块
admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuestAdmin)

