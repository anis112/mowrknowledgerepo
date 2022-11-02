
from distutils.log import debug
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as logout_view
#from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import OuterRef, Q, Subquery
from django.shortcuts import redirect, render

from .forms import ArticleDetailForm, DocumentForm, OrganizationForm
from .models import (Article, ArticleCategory, ArticleDetail, ArticlePublishCategory,
                     DataCategory, Document, Organization)
from accounts.models import CustomUser

import traceback

# Create your views here.


def home(request):
    count_organization = Organization.objects.count()
    count_categories = DataCategory.objects.filter(parent__isnull=True).count()

    pub_cat_ids = [5, 14]
    count_publication = Document.objects.filter(
        data_category__id__in=pub_cat_ids).count()
    count_reports = Document.objects.filter(
        Q(data_category__id=10) | Q(data_category__parent=10)).count()

    law_act_policy_cat_ids = [1, 7, 9, 11, 19]
    count_law_act_policy = Document.objects.filter(
        data_category__id__in=law_act_policy_cat_ids).count()

    plan_cat_ids = [33, 51]
    count_plan = Document.objects.filter(
        data_category__id__in=plan_cat_ids).count()

    context = {'organization': count_organization,
               'categories': count_categories, 'publication': count_publication, 'reports': count_reports, 'law_act_policy': count_law_act_policy, 'plan': count_plan}

    return render(request, 'home.html', context)


def home2(request):
    return render(request, 'home2.html')


def home3(request):
    return render(request, 'home3.html')


def test(request):
    return render(request, 'test.html')


def dashboard(request):
    count_organization = Organization.objects.count()

    count_categories = DataCategory.objects.filter(parent__isnull=True).count()

    pub_cat_ids = [5, 14]
    count_publication = Document.objects.filter(
        data_category__id__in=pub_cat_ids).count()
    count_reports = Document.objects.filter(
        Q(data_category__id=10) | Q(data_category__parent=10)).count()

    law_act_policy_cat_ids = [1, 7, 9, 11, 19]
    count_law_act_policy = Document.objects.filter(
        data_category__id__in=law_act_policy_cat_ids).count()

    plan_cat_ids = [33, 51]
    count_plan = Document.objects.filter(
        data_category__id__in=plan_cat_ids).count()

    context = {'organization': count_organization,
               'categories': count_categories, 'publication': count_publication, 'reports': count_reports, 'law_act_policy': count_law_act_policy, 'plan': count_plan}

    return render(request, 'dashboard.html', context)


def orgsearch(request):
    return render(request, 'orgsearch.html')


def docsearch(request):
    return render(request, 'docsearch.html')


def national_international(request):
    return render(request, 'national-international-search.html')


def SearchResult1(request):
    return render(request, 'SearchResult1.html')

def doc_details(request):
    return render(request, 'doc-details.html')

def article(request):
    #article_obj = Article.objects.get(pk=1)
    query_set = ArticlePublishCategory.objects.all()
    # query_set = Article.objects.select_related(
    #     'article_category', 'publish_category').order_by('id')

    # articles = Article.objects.filter(article_category=OuterRef('pk'))
    # ArticleCategory.objects.all().annotate(
    #     article_under_cat=Subquery(articles.values('article_category')))

    article_cat_queryset = ArticleCategory.objects.all()
    context = {'article_categories': article_cat_queryset,
               'atr_pub_cat': query_set}

    return render(request, 'article.html', context)


def article_detail(request, pk):
    article = Article.objects.get(id=pk)
    context = {'article': article}

    return render(request, 'article-detail.html', context)


def addOrganization(request):
    form = OrganizationForm()
    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'organization/add.html', context)


def viewOrganization(request):
    organizations = Organization.objects.all().order_by('sorting_order')
    context = {'organizations': organizations}

    return render(request, 'organization/view.html', context)


def addDocument(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(pk=request.user.id)
    #org_id = DocumentForm['organization'].value()
    #data_cat_id = DocumentForm['data_category'].value()

    form = DocumentForm()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                form.save()
                return redirect('/')
        except Exception as e:
            message = traceback.format_exc()
            # print(message)

    context = {'form': form}
    return render(request, 'document/add.html', context)

# def addDocument(request):
#     if request.user.is_authenticated:
#         user = CustomUser.objects.get(pk=request.user.id)

    form = DocumentForm()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'document/add.html', context)


def editDocument(request, id):
    document = Document.objects.get(id=id)

    context = {'document': document}
    return render(request, 'document/edit.html', context)


def updateDocument(request, id):
    document = Document.objects.get(id=id)
    form = DocumentForm(request.POST, instance=document)
    if form.is_valid():
        form.save()
        return redirect("/document/view")

    return render(request, 'document/edit.html', document)


def viewDocument(request):
    documents = Document.objects.all().order_by('id')
    context = {'documents': documents}

    return render(request, 'document/view.html', context)


def addArticleDetail(request):
    form = ArticleDetailForm()
    if request.method == 'POST':
        form = ArticleDetailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'articledetail/add.html', context)


# -------ahi------------

    """ keywords = ['funny', 'old', 'black_humor']
    qs = [Q(title__icontains=keyword) | Q(author__icontains=keyword)
          | Q(tags__icontains=keyword) for keyword in keywords]

    query = qs.pop()  # get the first element

    for q in qs:
        query |= q
    filtered_user_meme = Meme.objects.filter(query, user=current_user)
    publish_date__lte = timezone.now() """

    #req_query = request.GET | request.POST
    #    req_query = request.POST
    # if req_query is not None & req_query.get("search_term") is not None:


def search_document(request, search_term='water', org_ids=None, data_category_ids=None, access_category_ids=None):

    if request.method == "POST" or request.method == "GET":
        req_query = request.GET | request.POST

        if req_query and req_query.get("search_term"):
            search_term = req_query.get("search_term", None)
            org_ids = req_query.get("src_orgs", None)
            data_category_ids = req_query.get("src_doc_cats", None)

    if not isinstance(search_term, str):
        search_term = search_term[0]

    documents = Document.objects.all()

    user_organization_id = None  # request.user.organization_id

    if user_organization_id:
        cond_user = Q(organization_id=user_organization_id)

        documents = documents.filter(cond_user)

        # cond = Q(title__icontains=search_term) | Q(subject__icontains=search_term) | Q(
        #    description__icontains=search_term) | Q(keywords__icontains=search_term)
    if search_term is not None and search_term != '':
        cond = Q(title__icontains=search_term) | Q(
            subject__icontains=search_term) | Q(keywords__icontains=search_term)

        documents = documents.filter(cond)

    if org_ids and org_ids[0]:
        org_ids = [int(id) for id in org_ids]

        cond_org = Q(organization_id__in=org_ids)

        documents = documents.filter(cond_org)

    if data_category_ids and data_category_ids[0] != '':
        
        data_category_ids = [int(id) for id in data_category_ids]

        cond_cat = Q(data_category_id__in=data_category_ids)

        documents = documents.filter(cond_cat)

    if access_category_ids and access_category_ids[0] != '':
        
        access_category_ids = [int(id) for id in access_category_ids]

        cond_accat = Q(access_category_id__in=access_category_ids)

        documents = documents.filter(cond_accat)

    # org_list = documents.values_list(
    #     'organization__id', 'organization__organization_name').distinct()

    # cat_list = documents.values_list(
    #     'data_category__id', 'data_category__category_name').distinct()

    # for o in org_list:
    #     print(o)

    # for c in cat_list:
    #     print(c)

    doc_count = len(documents)

    if len(documents) < 1:
        documents = Document.objects.none()

    #doc_count = documents.order_by('organization_id', 'data_category_id')

    # print(len(documents))
    # for d in documents:
    #     print(d)

    org_infos = Organization.objects.all().order_by('id')

    doc_cats = DataCategory.objects.all().order_by('id')

    context = {'doc_count': doc_count, 'documents': documents.order_by('organization_id', 'data_category_id'),
               'search_term': search_term, 'src_orgs': org_ids, 'src_doc_cats': data_category_ids,
               'org_infos': org_infos, 'doc_cats': doc_cats}

    # context = {'doc_count': doc_count, 'documents': documents.order_by('organization_id', 'data_category_id'),
    #            'search_term': search_term, 'org_ids': org_ids, 'category_ids': data_category_ids, }
    # #    'category_ids': data_category_ids, 'org_list': org_list, 'cat_list': cat_list}

    return render(request, 'search_document.html', context)
