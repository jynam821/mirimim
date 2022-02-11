from django.urls import path
from . import views
from home.views import *

app_name = 'home'

urlpatterns= [
  path('', views.index, name='index'),
  path('ban/', views.ban, name='ban'),
  path('sub/', views.sub, name='sub'),
  path('detail/<int:pk>/', NoticeDetailView.as_view(),name='detail'),
  path('update/<int:pk>/', views.update, name='update'),
  path('delete/<int:pk>/', views.notice_delete, name='delete'),
  path('add/', views.add,name='add'),
  path('submit/<int:pk>/', views.submit,name='submit'),
  path('my_submitlist/',views.submitlist,name='submitlist'),
  path('submitlists/<int:pk>/',views.submitlists,name='submitlists'),
  path('submit_detail/<int:pk>/',SubmitDetailView.as_view(),name='submit_detail'),
  path('submit_delete/<int:pk>/',SubmitDeleteView.as_view(),name='submit_delete'),
  path('submit_update/<int:pk>/',views.submit_update,name='submit_update'),
  path('addclass/',views.addclass, name="addclass"),
  path('class_index/<int:pk>/',views.class_index, name='class_index'),
  path('refer/<int:pk>/',views.refer,name='refer'),
]