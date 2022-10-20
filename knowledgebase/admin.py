from django.contrib import admin

from .models import Article, ArticleCategory, ArticleDetail, ArticlePublishCategory, DataAccessCategory, DataCategory, Document, Organization

# Register your models here.




@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization_name', 'short_name',
                    'chief_designation', 'focal_person', 'email', 'phone_no']
    list_editable = ['organization_name', 'short_name']
    list_per_page = 50
    list_filter = ['organization_name']
    search_fields = ['organization_name__istartswith']


@admin.register(DataCategory)
class DataCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'parent', 'organization']
    list_editable = ['category_name', 'organization']
    list_per_page = 50
    search_fields = ['category_name']


@admin.register(DataAccessCategory)
class DataAccessCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']
    list_editable = ['category_name']
    list_per_page = 50


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    #autocomplete_fields = ['article_category']
    list_display = ['id', 'parent_id', 'organization', 'data_category',
                    'title', 'author', 'access_category']
    list_editable = ['parent_id', 'organization', 'data_category']
    list_per_page = 50
    list_filter = ['organization', 'data_category', 'access_category']
    search_fields = ['title__istartswith']


@admin.register(ArticleDetail)
class ArticleDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'parent_id', 'organization', 'data_category',
                    'title', 'author', 'access_category']
    list_editable = ['parent_id', 'organization', 'data_category']
    list_per_page = 50
    list_filter = ['organization', 'data_category', 'access_category']
    search_fields = ['title__istartswith']


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
