from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.admin.views.decorators import staff_member_required

app_name = 'Qa'
PERMISSION_DENIED = 'Qa:permission_denied'
urlpatterns = [
    url(r'^qa/$', views.qa_list, name='qa'),
]
