from django.urls import path

from . import views

# URLConf
urlpatterns = [
    path('login/', views.login, name="accounts/login"),     
    path('logout/', views.logout, name="accounts/logout"),    
    path('signup/', views.signup, name="accounts/signup"),
    path('profile/<username>', views.user_profile,name="accounts/user_profile"),
    path('user_list/<organization_id>', views.user_list,name="accounts/user_list"),
    path('edit_user/<id>', views.edit_user,name="accounts/edit_user"), 
]

# from django.contrib import admin
# admin.site.site_header = 'knowledgebase'                    # default: "Django Administration"
# admin.site.index_title = 'knowledgebase'                 # default: "Site administration"
# admin.site.site_title = 'knowledgebasem Adminsitration' # default: "Django site admin"