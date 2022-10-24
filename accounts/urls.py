from django.urls import path

from . import views

# URLConf
urlpatterns = [
    path('login/', views.login, name="accounts/login"),     
    path('logout/', views.logout, name="accounts/logout"),    
    path('signup/', views.signup, name="accounts/signup"),
    path('profile/<username>', views.user_profile,name="accounts/user_profile"),
]