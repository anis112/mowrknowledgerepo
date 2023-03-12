from django.contrib import admin

from .models import (Article, ArticleCategory, ArticleDetail,
                     ArticlePublishCategory, DataAccessCategory, DataCategory,
                     Document, Organization)


from .forms import DocumentForm

# Register your models here.


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['short_name','organization_name', 
                    'chief_designation', 'focal_person', 'email', 'phone_no']
    list_editable = ['organization_name', 'focal_person']
    list_per_page = 50
    list_filter = ['organization_name']
    search_fields = ['organization_name__istartswith']


@admin.register(DataCategory)
class DataCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'parent', 'organization']
    list_editable = ['category_name', 'organization']  
    list_per_page = 50
    list_filter = ['category_name','parent','organization']



@admin.register(DataAccessCategory)
class DataAccessCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name']
    list_editable = ['category_name']
    list_per_page = 50
    list_filter = ['category_name']



class OrganizationWiseFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ('Select Organization')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'organization_id'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        # return (
        #     ('80s', ('in the eighties')),
        #     ('90s', ('in the nineties')),
        # )
        if request.user.is_superuser:
            return Document.objects.values_list('organization_id','organization__organization_name').order_by('organization_id').distinct()
        elif request.user.is_organization_admin:
            return Document.objects.values_list('organization_id','organization__organization_name').filter(organization_id=request.user.organization_id).order_by('organization_id').distinct()
               
    def choices(self, cl):  # Overwrite this method to prevent the default "All"
            from django.utils.encoding import force_str
            for lookup, title in self.lookup_choices:
                yield {
                    'selected': self.value() == force_str(lookup),
                    'query_string': cl.get_query_string({
                        self.parameter_name: lookup,
                    }, []),
                    'display': title,
                }

    def queryset(self, request, queryset):  # Run the queryset based on your lookup values
        
    #     Returns the filtered queryset based on the value
    #     provided in the query string and retrievable via
    #     `self.value()`.
    #     """
    #     # Compare the requested value (either '80s' or '90s')
    #     # to organization how to filter the queryset.
    
        if request.user.is_superuser:
            if self.value() is not None:
                return queryset.filter(organization_id=self.value())
            else:    
                return queryset.all()
        elif request.user.is_organization_admin:
            return queryset.filter(organization_id=request.user.organization_id)
        #return queryset.all()
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    #form=DocumentForm
    #autocomplete_fields = ['article_category']
    list_display = ['title','organization','data_category', 'access_category']
    list_editable = ['data_category', 'access_category']
    list_per_page = 20
    list_filter = [OrganizationWiseFilter, 'data_category', 'access_category',]
    search_fields = ['title__istartswith']
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):     
        if db_field.name == "organization": #courier is the foreignkey name
            if request.user.is_organization_admin:
                kwargs["queryset"] = Organization.objects.filter(id=request.user.organization_id) #role ='Courier' in choices
        return super().formfield_for_foreignkey(db_field, request, **kwargs)     

# admin.site.register(Document)

@admin.register(ArticleDetail)
class ArticleDetailAdmin(admin.ModelAdmin):
    list_display = ['title','organization', 'data_category','parent_id']
    list_editable = ['organization', 'data_category']
    list_per_page = 20
    list_filter = ['organization', 'data_category']
    search_fields = ['title__istartswith']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    autocomplete_fields = ['article_category']
    #list_display = ['title', 'get_article_category_name', 'entry_date']
    list_display = ['id', 'title', 'parent_id', 'article_category','publish_category', 'entry_date', 'updated_date']
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
