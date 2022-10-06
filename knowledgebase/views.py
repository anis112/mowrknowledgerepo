from django.shortcuts import render
from django.db.models import OuterRef, Subquery
from .models import Article, ArticleCategory, ArticlePublishCategory

# Create your views here.


def home(request):
    return render(request, 'home.html')


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