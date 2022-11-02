from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name="home"),

    path('dashboard/', views.dashboard, name="dashboard"),
    path('orgsearch/', views.orgsearch, name="orgsearch"),
    path('docsearch/', views.docsearch, name="docsearch"),
    path('national_international/', views.national_international, name="national_international"),
    path('SearchResult1/', views.SearchResult1, name="SearchResult1"),
    path('doc-details/', views.doc_details, name="doc-details"),
    path('home2/', views.home2, name="home2"),
    path('home3/', views.home3, name="home3"),
    path('test/', views.test, name="test"),

    path('article/', views.article, name="article"),
    path('article/<int:pk>/', views.article_detail, name="article_detail"),

    path('organization/add', views.addOrganization, name="add_organization"),
    path('organization/view', views.viewOrganization, name="view_organization"),

    path('document/add', views.addDocument, name="add_document"),
    path('document/edit/<int:id>', views.editDocument, name="edit_document"),
    path('document/update/<int:id>', views.updateDocument, name="update_document"),
    path('document/view', views.viewDocument, name="view_document"),
    
    # path('document/view', views.viewDocument, name="view_document"),

    path('article/add', views.addArticleDetail, name="add_article"),
    path('article/view', views.viewArticleDetail, name="view_article"),

    path('search/', views.search_document, name="search"),
    path('search/<search_term>', views.search_document, name="search"),
    #path('search/<string:search_term>', views.search_document, name="search"),
]
