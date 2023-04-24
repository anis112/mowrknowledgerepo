import traceback
from distutils.log import debug

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as logout_view
#from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import OuterRef, Q, Subquery, Count
from django.http import JsonResponse
from django.shortcuts import redirect, render

from accounts.models import CustomUser

from .forms import ArticleDetailForm, DocumentForm, OrganizationForm
from .models import (Article, ArticleCategory, ArticleDetail,
                     ArticlePublishCategory, DataCategory, DataCommonCategory,
                     Document, Organization, OrganizationType)
from django.http import HttpResponse


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

    count_reports = Document.objects.filter(Q(data_category__data_common_category_id=3)).count()
    # count_reports = Document.objects.filter(Q(data_category__id=10) | Q(data_category__parent=10)).count()

    law_act_policy_rule_guidline_cat_ids = [1, 3, 4, 6, 7, 9, 11, 19, 50]
    count_law_act_policy = Document.objects.filter(
        data_category__id__in=law_act_policy_rule_guidline_cat_ids).count()

    plan_cat_ids = [33, 34, 51]
    count_plan = Document.objects.filter(
        data_category__id__in=plan_cat_ids).count()

    agreements_mous = [2, 12, 13, 63]
    count_agreements_mous = Document.objects.filter(
        data_category__id__in=agreements_mous).count()         # Q(data_category__data_common_category_id=5)).count()  

    modeling_tools = [59, 60]
    count_modeling_tools = Document.objects.filter(
        data_category__id__in=modeling_tools).count()

    # workshops_seminar = [7]
    count_workshops_seminar = Document.objects.filter(
        Q(data_category__data_common_category_id=7)).count()                


    count_docs = Document.objects.count()
    count_bwdb = Document.objects.filter(organization__id=1).count()
    count_warpo = Document.objects.filter(organization__id=2).count()
    count_rri = Document.objects.filter(organization__id=3).count()
    count_jrc = Document.objects.filter(organization__id=4).count()
    count_dbhwd = Document.objects.filter(organization__id=5).count()
    count_iwm = Document.objects.filter(organization__id=6).count()
    count_cegis = Document.objects.filter(organization__id=7).count()

    category_name_map = DataCategory.objects.filter(parent__isnull = True).order_by('data_common_category')

    orgranization_name = Organization.objects.all()             # .only()('short_name', 'organization_name')  # Organization.objects.values_list('organization_name')    
    acts_policy_rules_guidelines_docs = Document.objects.filter(Q(data_category__data_common_category_id=1)).order_by('data_category_id')        
    plans_docs = Document.objects.filter(data_category__id__in=plan_cat_ids).order_by('data_category_id')
    # plans_docs = Document.objects.filter(Q(data_category__data_common_category_id=4)).order_by('data_category_id')
    research_pub_docs = Document.objects.filter(data_category__id__in=pub_cat_ids).order_by('data_category_id')
    report_docs = Document.objects.filter(Q(data_category__data_common_category_id=3)).order_by('data_category_id')
    # report_docs = Document.objects.filter(Q(data_category__id=10) | Q(data_category__parent=10)).order_by('data_category_id') 

    context = {'organization': count_organization,
               'categories': count_categories, 'no_of_research_publications': count_publication, 'no_of_reports': count_reports, 'no_of_acts_policy_rules_gdlines': count_law_act_policy, 'no_of_plans': count_plan, 'no_of_agreements_mous': count_agreements_mous, 'no_of_modeling_tools': count_modeling_tools, 'no_of_workshops_seminar': count_workshops_seminar,
               'total_docs': count_docs, 'bwdb_docs': count_bwdb, 'rri_docs': count_rri, 'jrc_docs': count_jrc, 'dbhwd_docs': count_dbhwd, 'warpo_docs': count_warpo,
               'iwm_docs': count_iwm, 'cegis_docs': count_cegis, 'cat_map': category_name_map, 'org_names': orgranization_name, 'acts_policy_rules_guidelines_docs' : acts_policy_rules_guidelines_docs, 'plans_docs' : plans_docs, 'research_pub_docs' : research_pub_docs, 'report_docs' : report_docs }


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


def imp_links(request):
    return render(request, 'imp_links.html')

def help_info(request):
    return render(request, 'help.html')


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


def viewArticleDetail(request):
    article = ArticleDetail.objects.all()
    context = {'articles': article}

    return render(request, 'articledetail/view.html', context)


def document_detail(request, id):
    document = Document.objects.get(id=id)
    context = {'document': document}

    return render(request, 'doc-details.html', context)


# -------ahi------------

    # keywords = ['funny', 'old', 'black_humor']
    # qs = [Q(title__icontains=keyword) | Q(author__icontains=keyword)
    #       | Q(tags__icontains=keyword) for keyword in keywords]

    # query = qs.pop()  # get the first element

    # for q in qs:
    #     query |= q
    # filtered_user_meme = Meme.objects.filter(query, user=current_user)
    # publish_date__lte = timezone.now()

    #req_query = request.GET | request.POST
    #    req_query = request.POST
    # if req_query is not None & req_query.get("search_term") is not None:


def search_document(request, search_term='', org_ids=None, data_category_ids=None, access_category_ids=None):

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

        #cond_cat = Q(data_category_id__in=data_category_ids)

        cond_cat = Q(
            data_category__data_common_category_id__in=data_category_ids)

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

    #doc_cats = DataCategory.objects.all().order_by('id')
    doc_cats = DataCommonCategory.objects.all().order_by('id')

    context = {'doc_count': doc_count, 'documents': documents.order_by('organization_id', 'data_category_id'),
               'search_term': search_term, 'src_orgs': org_ids, 'src_doc_cats': data_category_ids,
               'org_infos': org_infos, 'doc_cats': doc_cats}

    # context = {'doc_count': doc_count, 'documents': documents.order_by('organization_id', 'data_category_id'),
    #            'search_term': search_term, 'org_ids': org_ids, 'category_ids': data_category_ids, }
    # #    'category_ids': data_category_ids, 'org_list': org_list, 'cat_list': cat_list}

    return render(request, 'search_document.html', context)


def search_doc_by_org(request, search_term='', org_ids=None, data_category_ids=None, access_category_ids=None):

    if request.method == "POST" or request.method == "GET":
        req_query = request.GET | request.POST

        if req_query and req_query.get("search_term"):

            search_term = req_query.get("search_term", None)
            # org_ids = req_query.get("src_org_list", None)
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

        #cond_cat = Q(data_category_id__in=data_category_ids)

        cond_cat = Q(
            data_category__data_common_category_id__in=data_category_ids)

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

    #doc_cats = DataCategory.objects.all().order_by('id')
    doc_cats = DataCommonCategory.objects.all().order_by('id')

    context = {'doc_count': doc_count, 'documents': documents.order_by('organization_id', 'data_category_id'),
               'search_term': search_term, 'src_orgs': org_ids, 'src_doc_cats': data_category_ids,
               'org_infos': org_infos, 'doc_cats': doc_cats}

    # context = {'doc_count': doc_count, 'documents': documents.order_by('organization_id', 'data_category_id'),
    #            'search_term': search_term, 'org_ids': org_ids, 'category_ids': data_category_ids, }
    # #    'category_ids': data_category_ids, 'org_list': org_list, 'cat_list': cat_list}

    return render(request, 'search_doc_by_org.html', context)


def search_doc_by_cat(request, search_term='', org_ids=None, data_category_ids=None, access_category_ids=None):

    if request.method == "POST" or request.method == "GET":
        req_query = request.GET | request.POST

        if req_query and req_query.get("search_term"):

            search_term = req_query.get("search_term", None)
            org_ids = req_query.get("src_orgs", None)
            data_category_ids = req_query.get("src_doc_cats", None)

    if not isinstance(search_term, str):
        search_term = search_term[0]

    documents = Document.objects.all()
    # documents = Document.objects.values_list('id', 'title', 'subject')
    # print(documents)

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

        #cond_cat = Q(data_category_id__in=data_category_ids)

        cond_cat = Q(
            data_category__data_common_category_id__in=data_category_ids)

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

    #doc_cats = DataCategory.objects.all().order_by('id')
    doc_cats = DataCommonCategory.objects.all().order_by('id')

    context = {'doc_count': doc_count, 'documents': documents.order_by('data_category__data_common_category_id', 'organization_id'),
               'search_term': search_term, 'src_orgs': org_ids, 'src_doc_cats': data_category_ids,
               'org_infos': org_infos, 'doc_cats': doc_cats}

    # context = {'doc_count': doc_count, 'documents': documents.order_by('organization_id', 'data_category_id'),
    #            'search_term': search_term, 'org_ids': org_ids, 'category_ids': data_category_ids, }
    # #    'category_ids': data_category_ids, 'org_list': org_list, 'cat_list': cat_list}

    return render(request, 'search_doc_by_cat.html', context)


def search_doc_by_nat(request, search_term='', org_ids=None, data_category_ids=None, access_category_ids=None):

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

        #cond_cat = Q(data_category_id__in=data_category_ids)

        cond_cat = Q(
            data_category__data_common_category_id__in=data_category_ids)

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

    #doc_cats = DataCategory.objects.all().order_by('id')
    doc_cats = DataCommonCategory.objects.all().order_by('id')

    context = {'doc_count': doc_count, 'documents': documents.order_by('organization_id', 'data_category_id'),
               'search_term': search_term, 'src_orgs': org_ids, 'src_doc_cats': data_category_ids,
               'org_infos': org_infos, 'doc_cats': doc_cats}

    # context = {'doc_count': doc_count, 'documents': documents.order_by('organization_id', 'data_category_id'),
    #            'search_term': search_term, 'org_ids': org_ids, 'category_ids': data_category_ids, }
    # #    'category_ids': data_category_ids, 'org_list': org_list, 'cat_list': cat_list}

    return render(request, 'search_doc_by_nat.html', context)

def search_doc_by_other(request, search_term='',s_doc_type=None, data_category_ids=None):

    if request.method == "POST" or request.method == "GET":
        req_query = request.GET | request.POST

        if req_query and req_query.get("search_term"):
            search_term = req_query.get("search_term", None)
            data_category_ids = req_query.get("src_doc_cats", None)
            s_doc_type = req_query.get("src_doc_type", None)                  
            # print(s_doc_type)

        if not isinstance(search_term, str):
            search_term = search_term[0]
        
        if not request.user.is_authenticated:
            public_documents = Document.objects.filter(access_category=1).exclude(organization__organization_type=1)
            context = show_search_results_for_other_doc(public_documents, search_term, s_doc_type, data_category_ids)
        else:
            if request.user.is_superuser:
                all_documents = Document.objects.exclude(organization__organization_type=1)
                context = show_search_results_for_other_doc(all_documents, search_term, s_doc_type, data_category_ids)
            else:
                user_id = request.user
                user_organization_id = user_id.organization_id

                public_documents = Document.objects.filter(access_category=1).exclude(organization__organization_type=1)
                user_org_documents = Document.objects.filter(organization = user_organization_id)
                documents = user_org_documents | public_documents
                context = show_search_results_for_other_doc(documents, search_term, s_doc_type, data_category_ids), {'s_doc_type': s_doc_type}

    return render(request, 'search_doc_by_nat.html', context)

def document_list(request, organization_id=None):
    # if request.method == "POST":
    organization_id = organization_id  # request.POST.get('id_organization')
    other_instances = Document.objects.filter(
        organization_id=organization_id).values('id', 'title')
    return JsonResponse({'data': list(other_instances)})


def get_related_keywords(title, keyword):
    r_keywords = []

    keywords = keyword.split(',|;')
    keywords = keyword.replace(',', ';').split(';')

    for kw in keywords:
        if kw in title:
            r_keywords.append(kw)
    return r_keywords


def document_details(request, id):

    document = Document.objects.get(id=id)

    documents = Document.objects.all()

    related_keywords = get_related_keywords(document.title, document.keywords)

    ####cond_cat = Q(data_category_id__in=data_category_ids)
    ##data_category_id = document.data_category.data_common_category_id
    ##cond_cat = Q(data_category__data_common_category_id=data_category_id)

    conds = Q(title__in=related_keywords) | Q(data_category_id=document.data_category_id) | Q(
        data_category__data_common_category_id=document.data_category.data_common_category_id)
    documents = documents.filter(conds)

    important_links = [{'title': "First Assessment of Transboundary Rivers, Lakes and Groundwaters", 'link': "https://unece.org/DAM/env/water/blanks/assessment/assessmentweb_full.pdf"},
                       {'title': "The Second Assessment of Transboundary Rivers, Lakes and Groundwaters in the UNECE Region",
                           'link': "https://unece.org/fileadmin/DAM/env/europe/monitoring/10thMeeting/Informal/ppp/TransboundaryWaters_2ndAssessment.pdf"},
                       ]

    context = {'document': document, 'documents': documents.order_by(
        'organization_id', 'data_category_id')[:25], 'important_links': important_links}

    return render(request, 'document_details.html', context)


# Driver code
#sentence = ['python coder', 'geeksforgeeks', 'coder in geeksforgeeks']
#words = ['coder', 'geeksforgeeks']
#print(check(sentence, words))



#=================================================================  HUD ==============================================================================
def org_counting(request):
    orgranization_name = Organization.objects.values_list('organization_name')
    org_count = len(orgranization_name)
    context = {'org_names': orgranization_name, 'org_count': org_count}
    return render(request, 'org_countings.html', context)  

def cat_counting(request):
    category_name = DataCategory.objects.filter(parent__isnull = True).values_list('category_name')
    cat_count = len(category_name)
    context = {'cat_names': category_name, 'cat_count': cat_count}
    return render(request, 'cat_counting.html', context)

def category_mapping(request):
    # category_name_map = DataCategory.objects.filter(parent__isnull = True).values('data_common_category', 'category_name', 'organization').order_by('data_common_category')
    category_name_map = DataCategory.objects.filter(parent__isnull = True).order_by('data_common_category')
    context = {'cat_map': category_name_map}   
    return render(request, "category_mapping_with_common_category.html", context)
#============================ START Data Search Code Common====================================
def document_count_organization_wise(data):
    cat_lst = []
    org_lst = []
    for item in data:
        temp_cat = item['data_category__data_common_category']
        if temp_cat in cat_lst:
            continue
        else:
            cat_lst.append(item['data_category__data_common_category']) 
    for item in data:
        temp_org = item['organization']
        if temp_org in org_lst:
            continue
        else:
            org_lst.append(item['organization'])  
    org_wise_count_lst = []
    for cat in cat_lst:
        for org in org_lst:
            temp = 0
            for item in data:
                if cat == item['data_category__data_common_category'] and org == item['organization']:
                    temp = temp + item['count']
            if temp == 0:
                continue
            temp_dict = {'organization': org, 'data_category__data_common_category': cat, 'count': temp}
            org_wise_count_lst.append(temp_dict)
    return org_wise_count_lst

def show_search_results(documents, search_term='', org_ids=None, data_category_ids=None):
    doc_count = len(documents)
    if len(documents) < 1:
        documents = Document.objects.none()
    
    if (search_term == '' and org_ids == None and data_category_ids == None):
         documents = documents.all()[:100]

    else:
        if search_term is not None and search_term != '':
            cond = Q(title__icontains=search_term) | Q(
                subject__icontains=search_term) | Q(keywords__icontains=search_term)

            documents = documents.filter(cond)
            doc_count = len(documents)

        if org_ids and org_ids[0]:
            org_ids = [int(id) for id in org_ids]
            cond_org = Q(organization_id__in=org_ids)

            documents = documents.filter(cond_org).order_by('data_category_id')
            doc_count = len(documents)

        if data_category_ids and data_category_ids[0] != '':
            data_category_ids = [int(id) for id in data_category_ids]
            cond_cat = Q(data_category__data_common_category_id__in=data_category_ids)

            documents = documents.filter(cond_cat).order_by('organization_id', 'data_category_id')
            doc_count = len(documents)
    

    #cond_org_fixed = Q(id__range=(1, 7))                                          # Added by MNH/ARH

    document_cat_wise_count = documents.values('data_category').annotate(count=Count('data_category'))
    document_org_wise_query = documents.values('organization', 'data_category__data_common_category').annotate(count=Count('data_category__data_common_category'))
    document_org_wise_count = document_count_organization_wise(document_org_wise_query)
    org_infos = Organization.objects.filter(organization_type=1).order_by('id')   # Added by MNH/ARH
    all_org_infos = Organization.objects.all().order_by('id')                     # Added by MNH/ARH
    # org_infos = Organization.objects.all().order_by('id')                       # Comment by MNH/ARH
    doc_cats = DataCommonCategory.objects.all().order_by('id')

    context = {'doc_count': (len(documents)==100 and ("100 out of "+str(doc_count)) or len(documents)), 'documents': documents,
                'search_term': search_term, 'src_orgs': org_ids, 'src_doc_cats': data_category_ids,
                'org_infos': org_infos, 'all_org_infos': all_org_infos, 'doc_cats': doc_cats, 'doc_cat_wise_count':document_cat_wise_count, 
                'doc_org_wise_count': document_org_wise_count}
    
    # context = {'doc_count': doc_count, 'documents': documents.order_by('data_category__data_common_category_id', 'organization_id'),
        #            'search_term': search_term, 'src_orgs': org_ids, 'src_doc_cats': data_category_ids,
        #            'org_infos': org_infos, 'doc_cats': doc_cats}

    return context


def show_search_results_for_other_doc(documents, search_term='', src_org_types=None, data_category_ids=None):
    doc_count = len(documents)
    if len(documents) < 1:
        documents = Document.objects.none()
    
    if (search_term == '' and data_category_ids == None and src_org_types == None):
         documents = documents.all()[:100]


    else:
        if search_term is not None and search_term != '':
            cond = Q(title__icontains=search_term) | Q(
                subject__icontains=search_term) | Q(keywords__icontains=search_term)

            documents = documents.filter(cond)
            doc_count = len(documents)
        
        
        if src_org_types and src_org_types[0] != '':
            src_org_types = [int(id) for id in src_org_types]
            cond_org_type = Q(organization__organization_type_id__in=src_org_types)

            documents = documents.filter(cond_org_type)
            doc_count = len(documents)


        if data_category_ids and data_category_ids[0] != '':
            data_category_ids = [int(id) for id in data_category_ids]
            cond_cat = Q(data_category__data_common_category_id__in=data_category_ids)

            documents = documents.filter(cond_cat).order_by('organization_id', 'data_category_id')
            doc_count = len(documents)

    document_cat_wise_count = documents.values('data_category').annotate(count=Count('data_category'))
    org_types = OrganizationType.objects.exclude(id=1).order_by('id')                   
    doc_cats = DataCommonCategory.objects.all().order_by('id')

    context = {'doc_count': (len(documents)==100 and ("100 out of "+str(doc_count)) or len(documents)), 'documents': documents,
                'search_term': search_term, 'src_doc_cats': data_category_ids, "src_doc_type": src_org_types, 'org_types': org_types, 'doc_cats': doc_cats, 'doc_cat_wise_count':document_cat_wise_count}

    return context


#============================ END Data Search Code Common ================================================================

def search_doc_by_org_test(request, search_term='', org_ids=None, data_category_ids=None):
     if request.method == "POST" or request.method == "GET":
        req_query = request.GET | request.POST

        if req_query and req_query.get("search_term"):
            search_term = req_query.get("search_term", None)
            data_category_ids = req_query.get("src_doc_cats", None)
            #org_ids = req_query.get("src_org_list", None)
            org_ids = req_query.get("src_orgs", None)
            org_list_ids = req_query.get("src_org_list", None)           

            # # # #if  not null or empty
            # # # #if org_list_ids and org_list_ids.strip :
            # if org_list_ids:
            #     org_ids = org_ids
            # else:
            #     org_ids = org_list_ids

            if (org_list_ids == '' or org_list_ids == None):
                org_ids = org_ids
            else:
                org_ids = org_list_ids

     if not isinstance(search_term, str):
        search_term = search_term[0]
    
     if not request.user.is_authenticated:
         public_documents = Document.objects.filter(access_category=1)
        #  print(type(public_documents))
         context = show_search_results(public_documents, search_term, org_ids, data_category_ids)
     else:
          if request.user.is_superuser:
            all_documents = Document.objects.all()
            context = show_search_results(all_documents, search_term, org_ids, data_category_ids)
          else:
            user_id = request.user
            user_organization_id = user_id.organization_id

            public_documents = Document.objects.filter(access_category=1)
            user_org_documents = Document.objects.filter(organization = user_organization_id)
            documents = user_org_documents | public_documents
            context = show_search_results(documents, search_term, org_ids, data_category_ids)
      
     return render(request, 'search_doc_by_org_hud.html', context)

def search_doc_by_cat_test(request, search_term='', org_ids=None, data_category_ids=None, access_category_ids=None):

    if request.method == "POST" or request.method == "GET":
        req_query = request.GET | request.POST

        if req_query and req_query.get("search_term"):
            search_term = req_query.get("search_term", None)
            org_ids = req_query.get("src_orgs", None)
            data_category_ids = req_query.get("src_doc_cats", None)

    if not isinstance(search_term, str):
        search_term = search_term[0]

    if not request.user.is_authenticated:
        public_documents = Document.objects.filter(access_category=1)
        # print(len(public_documents))
        context = show_search_results(public_documents, search_term, org_ids, data_category_ids)  
    else:
        if request.user.is_superuser:
            all_documents = Document.objects.all()
            context = show_search_results(all_documents, search_term, org_ids, data_category_ids)
        else:      
            # Currently logged in username and id Start
            user_id = request.user
            user_organization_id = user_id.organization_id
            # print(user_organization_id)
            # user_name = user_id.username
            # user_name = user_name.split('_')[-1]
            # print(user_name)   
            #end
            # user_org_documents = Document.objects.filter(Q(organization__short_name__icontains = user_name))

            public_documents = Document.objects.filter(access_category=1)
            user_org_documents = Document.objects.filter(organization = user_organization_id)
            documents = (user_org_documents | public_documents)

            # print(documents)
            # print(len(documents))
            context = show_search_results(documents, search_term, org_ids, data_category_ids)
    return render(request, 'search_doc_by_cat_hud.html', context)

#====================================== END HUD ==========================================================================
