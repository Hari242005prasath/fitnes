from django.urls import path
from . import views
from .views import generate_fitness_plan,dashboard
from django.conf import settings
from django.conf.urls.static import static


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
    path('',views.login_view,name='login'),
    path("save_fitness_plan/", views.save_fitness_plan, name="save_fitness_plan"),
    path("fitness_plan/", views.display_fitness_plan, name="ourOldschedule"),
    path('generate_fitness_pdf/',views.generate_fitness_pdf,name='generate_fitness_pdf'),
    path('streak/',views.streak,name='streak')




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
