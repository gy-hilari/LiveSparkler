from django.conf.urls import url
from . import views
from ..login_app import views as login_views

urlpatterns = [
    url(r'^$', login_views.index),
    url(r'^logout_user$', login_views.logout_user),

    url(r'^timeline$', views.index),
    url(r'^new_message$', views.new_message),
    url(r'^delete_message/(?P<message_id>\d+)$', views.delete_message),
    url(r'^view_message/(?P<message_id>\d+)$', views.view_message),

    url(r'^get_fireworks$', views.get_fireworks),
    url(r'^view_user_fireworks$', views.view_user_fireworks),
    url(r'^deploy_firework/(?P<message_id>\d+)/(?P<firework_name>\w+)$', views.deploy_firework),

]
