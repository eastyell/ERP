# from django.conf.urls import include, url,static
from purchase_manage import views
from django.urls import path

urlpatterns = [
    # url(r"admin/purchase_manage/purchase_order/cgdj2020002/update/ShowDetail/", views.TestView),
    path("admin/purchase_manage/purchase_order/cgrk20200001/update/ShowDetail/", views.TestView),]
