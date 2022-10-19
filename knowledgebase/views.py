
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as logout_view
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import OuterRef, Q, Subquery
from django.shortcuts import redirect, render

from .forms import OrganizationForm
from .models import (Article, ArticleCategory, ArticlePublishCategory,
                     DataCategory, Document, Organization)

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




def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            uname=form.cleaned_data['username']
            upassword=form.cleaned_data['password']           
            user = authenticate(username=uname, password=upassword)
            if user.is_active:
                if user.is_superuser or user.is_staff:
                    auth_login(request,user)
                    return redirect('/knowledgebase/dashboard/')  # or your url name
                else:
                    auth_login(request,user)
                    return redirect('/')

    else:
        form=AuthenticationForm()
        return render(request, 'login.html',{'form':form})    

def logout(request):
    logout_view(request)
    return redirect('login')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {
        'form': form
    })

def orgsearch(request):
    return render(request, 'orgsearch.html')


def docsearch(request):
    return render(request, 'docsearch.html')


def national_international(request):
    return render(request, 'national-international-search.html')


def SearchResult1(request):
    return render(request, 'SearchResult1.html')


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
    context = {'form': form}

    return render(request, 'Organization/add.html', context)
