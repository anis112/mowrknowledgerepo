from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'Knowledge Repository Admin Panel'
admin.site.index_title = 'Admin'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('knowledgebase.urls')),
    path('knowledgebase/', include('knowledgebase.urls')),
    path('accounts/', include('accounts.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    #path('', include('django.contrib.auth.urls')),
]
