from django.contrib.auth import authenticate, login as auth_login, logout as logout_view
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import OuterRef, Subquery
from django.shortcuts import redirect, render

from .forms import OrganizationForm
from .models import Article, ArticleCategory, ArticlePublishCategory

# Create your views here.


def home(request):
    return render(request, 'home.html')


def home2(request):
    
    return render(request, 'home2.html')


def home3(request):
    return render(request, 'home3.html')


def dashboard(request):
    return render(request, 'dashboard.html')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request,data=request.POST)
        valuenext= request.POST.get('next')
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
