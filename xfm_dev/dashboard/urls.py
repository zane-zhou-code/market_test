from django.urls import path, include
from django.conf.urls import url
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('base', views.base, name='base'),
    path('echarts', views.echarts, name='echarts'),
    path('echarts2', views.echarts2, name='echarts2'),
    path('echarts3', views.echarts3, name='echarts3'),
    path('echarts4', views.echarts4, name='echarts4'),
    path('analysis', views.analysis, name='analysis'),
    path('filter', views.filter, name='filter'),
    path('query', views.query, name='query'),
    path('query2', views.query2, name='query2'),
    path('query3', views.query3, name='query3'),
    path('query4', views.query4, name='query4'),
    path('query5', views.query5, name='query5'),
    path('query6', views.query6, name='query6'),
    path('select_query', views.select_query, name='select_query'),
    path('market_dates', views.market_dates, name='market_dates'),
    path('market_dates2', views.market_dates2, name='market_dates2'),
    path('market_dates3', views.market_dates3, name='market_dates3'),
    path('text', views.text, name='text'),
    path('text2', views.text2, name='text2'),
    path('text3', views.text3, name='text3'),
    path('text4', views.text4, name='text4'),
    path('semantic', views.semantic, name='semantic-ui'),
    path('test/', views.test, name='test'),
    path('zzzzzz', views.zzzzzz, name='zzzzzz'),
    # path('api/666', view=lambda request: HttpResponse('戏说不是胡说')),
    # url(regex='^$', view=lambda request:
    #     TemplateView.as_view(template_name='vue.html')),
]