from django.conf.urls import url
from django.shortcuts import render,HttpResponse
class StarkConfig(object) :
    def __init__(self,model_class,site) :
        self.model_class = model_class
        self.site = site

    def get_urls(self) :
        app_model_name = (self.model_class._meta.app_label,self.model_class._meta.model_name,)
        url_patterns = [
            url(r'^$',self.changelist_view,name="%s_%s_changlist" %app_model_name),
            url(r'^add/$', self.add_view, name="%s_%s_add" % app_model_name),
            url(r'^(\d+)/delete/$', self.delete_view, name="%s_%s_delete" % app_model_name),
            url(r'^(\d+)/change/$', self.change_view, name="%s_%s_change" % app_model_name),
        ]
        return url_patterns

    @property
    def urls(self) :
        return self.get_urls()

##############视图函数################
    def changelist_view(self,request,*args,**kwargs) :
        head_list = []
        new_data_list = []
        data_list = self.model_class.objects.all()
        if (self.list_display) :
            for field_name in self.list_display:
                if isinstance(field_name,str):
                    # 根据类和字段名称，获取字段对象的verbose_name
                    verbose_name = self.model_class._meta.get_field(field_name).verbose_name
                else:
                    verbose_name = field_name(self,is_header=True)
                head_list.append(verbose_name)

            # 处理表中的数据
            for row in data_list:
                temp = []
                for field_name in self.list_display :
                    if isinstance(field_name,str):
                        val = getattr(row,field_name) # # 2 alex2
                    else:
                        val = field_name(self,row)
                    temp.append(val)
                new_data_list.append(temp)
        else :
            for data in data_list :
                temp = []
                temp.append(data)
                new_data_list.append(temp)
        return render(request,'changelist.html',{'data_list':new_data_list,'head_list':head_list})
    def add_view(self,request,*args,**kwargs) :
        return HttpResponse("添加")
    def delete_view(self,request,*args,**kwargs) :
        return HttpResponse("删除")
    def change_view(self,request,*args,**kwargs) :
        return HttpResponse("修改")

class StarkSite() :
    def __init__(self) :
        self._registry = {}

    def register(self,model_class,stark_config_class=None) :
        if not stark_config_class :
            stark_config_class = StarkConfig
        self._registry[model_class] = stark_config_class(model_class,self)

    def get_urls(self) :
        url_pattern = []
        for model_class,stark_config_obj in self._registry.items() :
            app_name = model_class._meta.app_label
            model_name = model_class._meta.model_name

            curd_url = url(r'^%s/%s/' %(app_name,model_name,),(stark_config_obj.urls,None,None))
            url_pattern.append(curd_url)
        return url_pattern
    
    @property
    def urls(self) :
        return (self.get_urls(),None,'stark')

site = StarkSite()