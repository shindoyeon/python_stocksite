from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('tables',views.tables),
    path('chartsModify',views.chartsModify),
    path('test',views.test),
]
