from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import (Article, ArticleCategory, ArticleDetail,
                     ArticlePublishCategory, DataAccessCategory, DataCategory,
                     Document, Organization,OrganizationType, DocumentFile, DocumentApprovalStatus)


from .forms import DocumentForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, render
# Register your models here.


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['short_name','organization_name','organization_type', 
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
        else:
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
        else:
            return queryset.filter(organization_id=request.user.organization_id)
        #return queryset.all()

class CategoryWiseFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ('Select Data Category')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'data_category_id'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        if request.user.is_superuser:
            return Document.objects.values_list('data_category_id','data_category__category_name').order_by('data_category_id').distinct()
        elif request.user.is_organization_admin:
            return Document.objects.values_list('data_category_id','data_category__category_name').filter(organization_id=request.user.organization_id).order_by('data_category_id').distinct()
        else:
            return Document.objects.values_list('data_category_id','data_category__category_name').filter(organization_id=request.user.organization_id).order_by('data_category_id').distinct()     
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
        if request.user.is_superuser:
            if self.value() is not None:
                return queryset.filter(data_category_id=self.value())
            else:    
                return queryset.all()
        elif request.user.is_organization_admin:
            return queryset.filter(organization_id=request.user.organization_id)
        else:
            return queryset.filter(organization_id=request.user.organization_id)
        
class DocumentFileInline(admin.StackedInline):
    model = DocumentFile
    extra = 1
    fields = ('file',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    #form=DocumentForm
    #autocomplete_fields = ['article_category']
    inlines = [DocumentFileInline,]
    actions = ['preview_document']
    
    list_display = ['title','organization','data_category', 'access_category', 'document_approval_status', 'modified_date', 'modified_by']
    exclude = ('is_parent_available', 'file_name')
    list_per_page = 20
    list_filter = [OrganizationWiseFilter, CategoryWiseFilter , 'access_category', 'document_approval_status']
    search_fields = ['title__istartswith']
    #list_editable = ['data_category', 'access_category', 'document_approval_status']

    # def get_list_display(self, request):
    #     if request.user.is_superuser:
    #         return ['title', 'organization','data_category', 'access_category', 'document_approval_status', 'modified_date', 'modified_by']
    #     elif request.user.is_organization_admin:
    #         return ['title', 'organization','data_category', 'access_category', 'document_approval_status', 'modified_date', 'modified_by']
    #     else:
    #         return ['title', 'organization', 'data_category', 'access_category', 'modified_date', 'modified_by']

    # def preview_document():
    #     url = reverse('knowledgebase/preview/')
    #     return HttpResponseRedirect(url)
 
    def response_add(self, request, obj):
        if "preview_document" in request.POST:
            # do whatever you want the button to do
            obj.save()
            retirved_document = Document.objects.filter(id=obj.id)
            attached_files = DocumentFile.objects.filter(document__id=obj.id)
            organization_id = retirved_document.values_list('organization')[0][0]
            print(organization_id)
            # print(retirved_document)
            # print(attached_files)
            context = {'document':retirved_document, 'attached_files': attached_files, 'organization_id':organization_id}
            # return HttpResponse("hello")
            return render(request, 'document_preview.html', context)
        return super().response_add(request, obj)

    def response_change(self, request, obj):
        if "preview_document" in request.POST:
            # do whatever you want the button to do
            obj.save()
            retirved_document = Document.objects.filter(id=obj.id)
            attached_files = DocumentFile.objects.filter(document__id=obj.id)
            organization_id = retirved_document.values_list('organization')[0][0]
            # print(retirved_document)
            # print(attached_files)
            context = {'document':retirved_document, 'attached_files': attached_files, 'organization_id':organization_id}
            # return HttpResponse("hello")
            return render(request, 'document_preview.html', context)
        return super().response_change(request, obj)
    
    def get_changelist_instance(self, request):
        if request.user.is_superuser:
            self.list_editable = ('data_category', 'access_category', 'document_approval_status',)
        elif request.user.is_organization_admin:
            self.list_editable = ('data_category', 'access_category', 'document_approval_status',)
        else:
            self.list_editable = ()
        return super().get_changelist_instance(request)
        
    # def get_readonly_fields(self, request, obj=None, **kwargs):     
    #     if not request.user.is_superuser and not request.user.is_organization_admin:          
    #             return ("document_approval_status",)
    #     return ()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):     
        if db_field.name == "organization": #courier is the foreignkey name
            if request.user.is_organization_admin:
                kwargs["queryset"] = Organization.objects.filter(id=request.user.organization_id) #role ='Courier' in choices
            elif request.user.is_staff:
                kwargs["queryset"] = Organization.objects.filter(id=request.user.organization_id)
        elif db_field.name == "data_category":
            if request.user.is_organization_admin:
                kwargs["queryset"] = DataCategory.objects.filter(organization_id=request.user.organization_id)
            elif request.user.is_staff:
                kwargs["queryset"] = DataCategory.objects.filter(organization_id=request.user.organization_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, instance, obj=None, **kwargs,):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['organization'].initial = request.user.organization
            form.base_fields['entry_by'].initial = request.user.username
            form.base_fields['modified_by'].initial = request.user.username
            form.base_fields['document_approval_status'].initial = 1
            form.base_fields['entry_by'].widget = forms.HiddenInput()
            form.base_fields['modified_by'].widget = forms.HiddenInput()
            form.base_fields['document_approval_status'].widget = forms.HiddenInput()
            # form.base_fields['entry_by'].widget.attrs['disabled'] = True
        return form
    
    @transaction.atomic
    def save_model(self, request, obj, form, change): 
        obj.save()  # Save Document instance
        
        existing_files = DocumentFile.objects.filter(document__id=obj.id)
        if not existing_files:
            # Get the uploaded files from the request.FILES
            if request.FILES == {}:
                 raise ValidationError("Please Upload file.")
        
       
            
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


@admin.register(OrganizationType)
class OrganizationTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type_name']
    list_editable = ['type_name']
    list_per_page = 50

@admin.register(DocumentApprovalStatus)
class DocumentApprovalStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'approval_state_name']
    list_editable = ['approval_state_name']
    list_per_page = 20

#admin.site.register(Article, ArticleAdmin)
# admin.site.register(ArticleCategory)
# admin.site.register(ArticlePublishCategory)
