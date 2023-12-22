from django.urls import path 
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('course/<str:pk>/', views.course, name="course"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-course/', views.createCourse, name="create-course"),
    path('update-course/<str:pk>/', views.updateCourse, name="update-course"),
    path('delete-course/<str:pk>/', views.deleteCourse, name="delete-course"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),   

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
] 