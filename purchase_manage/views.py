from django.shortcuts import render
from xadmin.views import CommAdminView
# Create your views here.

class TestView(CommAdminView):
    def get(self, request):
        # context = super().get_context()  # 这一步是关键，必须super一下继承CommAdminView里面的context，不然侧栏没有对应数据，我在这里卡了好久
        # title = "下单商品明细"  # 定义面包屑变量
        # context["breadcrumbs"].append({'url': '/admin/', 'title': title})  # 把面包屑变量添加到context里面
        # context["title"] = title  # 把面包屑变量添加到context里面

        # 下面你可以接着写你自己的东西了，写完记得添加到context里面就可以了

        # return render(request, 'hello.html', context)  # 最后指定自定义的template模板，并返回context
        test['test'] = "下单商品明细"
        context["title"] = title
        # context["title"]  = "下单商品明细"
        return render(request, 'hello.html',context)


