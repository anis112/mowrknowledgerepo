from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),

    #path('dashboard/', views.dashboard, name="dashboard"),
    path('', views.dashboard, name="dashboard"),
    path('orgsearch/', views.orgsearch, name="orgsearch"),
    path('docsearch/', views.docsearch, name="docsearch"),
    path('national_international/', views.national_international,
         name="national_international"),
    path('SearchResult1/', views.SearchResult1, name="SearchResult1"),
    path('doc-details/', views.doc_details, name="doc-details"),
    path('imp_links/', views.imp_links, name="imp_links"),


    path('org_countings/', views.org_counting, name="org-countings"),
    path('cat_countings/', views.cat_counting, name="cat-countings"),



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
    #path('article/view', views.viewArticleDetail, name="view_article"),
    path('search/doc-details/<int:id>',
         views.document_detail, name="document_detail"),

    path('document/document_list/<int:organization_id>',
         views.document_list, name="document_list"),


    # ahi

    path('search/', views.search_document, name="search"),
    path('search/<search_term>', views.search_document, name="search"),
    #path('search/<string:search_term>', views.search_document, name="search"),

    path('search-by-org/', views.search_doc_by_org_test, name="search-by-org"),
    path('search-by-org/<search_term>', views.search_doc_by_org_test, name="search-by-org"),

    path('search-by-cat/', views.search_doc_by_cat_test, name="search-by-cat"),
    path('search-by-cat/<search_term>', views.search_doc_by_cat_test, name="search-by-cat"),

    path('search-by-nat/', views.search_doc_by_nat, name="search-by-nat"),
    path('search-by-nat/<search_term>', views.search_doc_by_nat, name="search-by-nat"),
    
    path('document-details/', views.document_details, name="document-details"),
    path('document-details/<int:id>', views.document_details, name="document-details"),
   
    

]
