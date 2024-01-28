"""
URL configuration for aisproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from aisfeedbackapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.loginpage),
    path('loginpage',views.loginpage,name='loginpage'),
    path('feedbackpage',views.feedbackpage,name='feedbackpage'),
    path('submissionpage',views.submissionpage,name='submissionpage'),
    path('registration',views.registration,name='registration'),
    path('successpage',views.successpage,name='successpage'),
    path('logoutpage',views.logoutpage,name='logoutpage'),
    path('admin_tools_stats', include('admin_tools_stats.urls')),
    path('admin_panel', views.admin_panel, name='admin_panel'),
    path('admin_panel1', views.admin_panel1, name='admin_panel1'),
    path('clients_data',views. clients_data, name='clients_data'),
    path('clients_feedback',views. clients_feedback, name='clients_feedback'),
    
]
