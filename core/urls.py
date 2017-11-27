from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^q1$', views.q1, name='q1'),
    url(r'^q2$', views.q2, name='q2'),
    url(r'^q3$', views.q3, name='q3'),
    url(r'^q4$', views.q4, name='q4'),
    url(r'^q5_6$', views.q5_6, name='q5_6'),
]