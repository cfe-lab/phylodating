from django.urls import path

from . import views

app_name = 'phylodating'

urlpatterns = [
    path('', views.index, name='index'),
    path('jobs/<int:job_id>/', views.details, name='details'),
    path('results/', views.results, name='results'),
    path('download/<int:job_id>/', views.download, name='download'),
]