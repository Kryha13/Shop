
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

app_name = 'Common'

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

]