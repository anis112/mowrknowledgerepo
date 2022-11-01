from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from knowledgebase.models import Organization

from .models import CustomUser
from datetime import date

# Register your models here.


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
            return CustomUser.objects.values_list('organization_id','organization__organization_name').order_by('organization_id').distinct()
        elif request.user.is_organization_admin:
            return CustomUser.objects.values_list('organization_id','organization__organization_name').filter(organization_id=request.user.organization_id).order_by('organization_id').distinct()
               
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
        return queryset.all()

class CustomUserAdmin(UserAdmin):
    
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'is_organization_admin', 'organization'
        )
    list_filter= (OrganizationWiseFilter,'is_organization_admin',)
    
    def get_readonly_fields(self, request, obj=None, **kwargs):     
        if request.user.is_superuser==False:           
            return ("is_organization_admin","is_superuser","is_staff","groups","user_permissions")
        return ("", )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):     
        if db_field.name == "organization": #courier is the foreignkey name
            if request.user.is_organization_admin:
                kwargs["queryset"] = Organization.objects.filter(id=request.user.organization_id) #role ='Courier' in choices
        return super().formfield_for_foreignkey(db_field, request, **kwargs)        
    
    
    #readonly_fields = ('is_organization_admin', )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('is_organization_admin', 'organization')
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('is_organization_admin', 'organization')
        })
    )


       
admin.site.register(CustomUser, CustomUserAdmin)


