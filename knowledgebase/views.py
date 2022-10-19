from django.shortcuts import render
from django.db.models import OuterRef, Subquery
from .models import Article, ArticleCategory, ArticlePublishCategory, Organization, DataCategory
from .forms import OrganizationForm

# Create your views here.


def home(request):
    count_organization = Organization.objects.count()
    #count_categories = DataCategory.objects.filter(parent__isnull=True).count()
    count_categories = DataCategory.objects.count()

    context = {'organization': count_organization,
               'categories': count_categories}
    return render(request, 'home.html', context)


def home2(request):
    return render(request, 'home2.html')


def home3(request):
    return render(request, 'home3.html')


def dashboard(request):
    count_organization = Organization.objects.count()
    #count_categories = DataCategory.objects.filter(parent__isnull=True).count()
    count_categories = DataCategory.objects.count()

    context = {'organization': count_organization,
               'categories': count_categories}
    return render(request, 'dashboard.html', context)


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
