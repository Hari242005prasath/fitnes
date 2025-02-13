from django.urls import path
from . import views
from .views import generate_fitness_plan,dashboard

urlpatterns = [
    path('home/', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('generate_fitness_plan/', generate_fitness_plan, name='generate_fitness_plan'),
    path('dashboard/', dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('joinin/', views.joinin, name='joinin'),
    path('new-schedule/', views.newSchedule, name='newSchedule'),
    path('Our-schedule/', views.ourSchedule, name='ourSchedule'),
    path('streal/', views.streak, name='streak'),
    path('',views.login_view,name='login'),



]
