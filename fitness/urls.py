"""
URL configuration for fitness project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),  
    #path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='myapp/login.html',
        redirect_field_name='next'
    ), name='login'),
    path("", include("myapp.urls")),  
    path('generate_fitness_pdf/', views.generate_fitness_pdf, name='generate_fitness_pdf'),
    path('newSchedule/', views.newSchedule, name='newSchedule'),
    path('ourOldschedule/', views.ourSchedule, name='ourOldschedule'),
    path('save_fitness_plan/', views.save_fitness_plan, name='save_fitness_plan'),
    path('streak', views.streak),
    path('analytics', views.analytics),
    path('log_workout/', views.log_workout, name='log_workout'),
    path('chatbot_response/', views.chatbot_response, name='chatbot_response'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
