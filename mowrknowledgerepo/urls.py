from django.contrib import admin
from django.urls import include, path
from . import views

admin.site.site_header = 'Knowledge Repository Admin Panel'
admin.site.index_title = 'Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('knowledgebase.urls')),
    path('knowledgebase/', include('knowledgebase.urls')),
    path('accounts/', include('accounts.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    #path('', include('django.contrib.auth.urls')),

    
    path('search/', views.search_document, name="search"),
    path('search/<search_term>', views.search_document, name="search"),
    #path('search/<string:search_term>', views.search_document, name="search"),
]
