from django.conf.urls import url
from . import views
from ..message_app import views as message_views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register_user$', views.register_user), 
    url(r'^login_user$', views.login_user), 
    url(r'^logout_user$', views.logout_user),
    
    url(r'^session_test$', views.session_test),

    url(r'^timeline$', message_views.index),
]