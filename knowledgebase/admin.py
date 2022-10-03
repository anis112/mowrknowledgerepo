from django.contrib import admin
from .models import Article, ArticleCategory, ArticlePublishCategory

# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    autocomplete_fields = ['article_category']
    #list_display = ['title', 'get_article_category_name', 'entry_date']
    list_display = ['id', 'title', 'parent_id', 'article_category',
                    'publish_category', 'entry_date', 'updated_date']
    list_editable = ['parent_id', 'article_category', 'publish_category']
    list_per_page = 50
    list_filter = ['article_category', 'entry_date', 'updated_date']
    search_fields = ['title__istartswith']


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'logo_name']
    list_editable = ['category_name', 'logo_name']
    list_per_page = 50
    search_fields = ['category_name']


@admin.register(ArticlePublishCategory)
class ArticlePublishCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']
    list_editable = ['category_name']
    list_per_page = 50


#admin.site.register(Article, ArticleAdmin)
# admin.site.register(ArticleCategory)
# admin.site.register(ArticlePublishCategory)
